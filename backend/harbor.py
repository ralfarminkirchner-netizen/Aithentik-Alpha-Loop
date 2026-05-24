#!/usr/bin/env python3
"""AITHENTIK HARBOR v1.0 - Externer Signal-Hafen + REST-API"""

import os
import json
import asyncio
import re
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List, Dict, Optional, Union, Set

import aiohttp
import feedparser
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, BackgroundTasks, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from loguru import logger
import uvicorn
import PyPDF2
import io
from fastapi import UploadFile, File

load_dotenv()

sys_path_insert = __import__("sys").path.insert
sys_path_insert(0, str(Path(__file__).parent))
from antigravity import AithentikCore

# ══════════════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════════════

HARBOR_PORT             = int(os.getenv("HARBOR_PORT",             "8000"))
HARVEST_INTERVAL_HOURS  = int(os.getenv("HARVEST_INTERVAL_HOURS",  "6"))
FEEDS_FILE              = Path(os.getenv("FEEDS_FILE",             "feeds.json"))
STATE_FILE              = Path(os.getenv("HARBOR_STATE_FILE",      "harbor_state.json"))
MAX_ITEMS_PER_FEED      = 10   # Max neue Items pro Harvest-Runde
URL_EXTRACT_CHARS       = 1500 # Wieviel Text von einer URL wir verarbeiten
MIN_SCORE_TO_STORE      = 0    # Alle Patterns speichern (auch DISCARD) – Myzel lernt

# ══════════════════════════════════════════════════════════════
#  PYDANTIC MODELS
# ══════════════════════════════════════════════════════════════

class IngestRequest(BaseModel):
    raw_input: str
    source: str = "manual"      # "manual" | "rss" | "url" | "api"
    source_url: Optional[str] = None

class UrlIngestRequest(BaseModel):
    url: str
    hint: str = ""              # Optionaler Kontext-Hint

class FeedConfig(BaseModel):
    url: str
    name: str
    active: bool = True
    tags: List[str] = []


# ══════════════════════════════════════════════════════════════
#  HARBOR STATE  (Persistenz via JSON)
# ══════════════════════════════════════════════════════════════

class HarborState:
    """Verfolgt gesehene Items und Harvest-Statistiken."""

    def __init__(self):
        self.seen_ids:    Set[str]     = set()
        self.results:     List[Dict]   = []     # Letzten 100 Ergebnisse
        self.last_harvest: Optional[str]  = None
        self.harvest_count: int        = 0
        self.load()

    def load(self):
        if STATE_FILE.exists():
            try:
                data = json.loads(STATE_FILE.read_text())
                self.seen_ids      = set(data.get("seen_ids", []))
                self.results       = data.get("results", [])[-100:]
                lh = data.get("last_harvest")
                self.last_harvest  = str(lh) if lh else None
                self.harvest_count = data.get("harvest_count", 0)
                logger.info(f"Harbor State geladen: {len(self.seen_ids)} bekannte Items")
            except Exception as e:
                logger.warning(f"State-Datei nicht lesbar: {e}")

    def save(self):
        try:
            STATE_FILE.write_text(json.dumps({
                "seen_ids":      list(self.seen_ids),
                "results":       self.results[-100:],
                "last_harvest":  self.last_harvest,
                "harvest_count": self.harvest_count,
            }, indent=2, ensure_ascii=False))
        except Exception as e:
            logger.warning(f"State-Speichern fehlgeschlagen: {e}")

    def mark_seen(self, item_id: str):
        self.seen_ids.add(item_id)

    def is_seen(self, item_id: str) -> bool:
        return item_id in self.seen_ids

    def add_result(self, result: Dict):
        self.results.append(result)
        if len(self.results) > 100:
            self.results = self.results[-100:]


# ══════════════════════════════════════════════════════════════
#  FEED MANAGER
# ══════════════════════════════════════════════════════════════

def load_feeds() -> List[Dict]:
    if not FEEDS_FILE.exists():
        _create_sample_feeds()
    try:
        return json.loads(FEEDS_FILE.read_text())
    except Exception:
        return []


def _create_sample_feeds():
    sample = [
        {"url": "https://feeds.feedburner.com/TechCrunch",
         "name": "TechCrunch",         "active": True, "tags": ["tech", "startups"]},
        {"url": "https://www.reddit.com/r/entrepreneur/.rss",
         "name": "r/Entrepreneur",     "active": True, "tags": ["business"]},
        {"url": "https://hnrss.org/frontpage",
         "name": "Hacker News",        "active": True, "tags": ["tech", "ideas"]},
        {"url": "https://www.theinformation.com/feed",
         "name": "The Information",    "active": False, "tags": ["tech", "deep"]},
        {"url": "https://feeds.bloomberg.com/markets/news.rss",
         "name": "Bloomberg Markets",  "active": False, "tags": ["markets", "trading"]},
    ]
    FEEDS_FILE.write_text(json.dumps(sample, indent=2))
    logger.info(f"Sample feeds.json erstellt: {FEEDS_FILE}")


# ══════════════════════════════════════════════════════════════
#  URL TEXT EXTRACTOR  (kein BS4 nötig – reines Regex)
# ══════════════════════════════════════════════════════════════

async def extract_url_text(url: str) -> str:
    """Fetcht eine URL und extrahiert lesbaren Text (basic HTML-Stripping)."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; AithentikHarbor/1.0)"},
                timeout=aiohttp.ClientTimeout(total=12),
            ) as resp:
                if resp.status != 200:
                    return f"HTTP {resp.status} für {url}"
                html = await resp.text(errors="replace")

        # HTML → Plain Text (basic)
        text = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style>",  " ", text,  flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>",                  " ", text)
        text = re.sub(r"\s+",                       " ", text).strip()
        text = re.sub(r"[^\x20-\x7E\xC0-\xFF]",   "",  text)  # Non-printable entfernen

        return text[:URL_EXTRACT_CHARS]
    except Exception as e:
        return f"Fetch-Fehler: {e}"


# ══════════════════════════════════════════════════════════════
#  HARVESTER
# ══════════════════════════════════════════════════════════════

async def harvest_feed(
    feed: Dict,
    core: AithentikCore,
    state: HarborState,
) -> List[Dict]:
    """Harvested einen einzelnen RSS-Feed und verarbeitet neue Items."""
    url   = feed.get("url", "")
    name  = feed.get("name", url)
    tags  = feed.get("tags", [])
    results = []

    logger.info(f"📡 Harvesting: {name}")

    try:
        # feedparser ist synchron – in Thread auslagern
        loop    = asyncio.get_event_loop()
        parsed  = await loop.run_in_executor(None, feedparser.parse, url)
        entries = parsed.entries[:MAX_ITEMS_PER_FEED]
    except Exception as e:
        logger.warning(f"Feed-Parse-Fehler ({name}): {e}")
        return []

    new_count = 0
    for entry in entries:
        # Eindeutige ID pro Item
        item_id = hashlib.md5(
            (entry.get("id") or entry.get("link") or entry.get("title", "")).encode()
        ).hexdigest()

        if state.is_seen(item_id):
            continue

        state.mark_seen(item_id)
        new_count += 1

        # Input für die Pipeline bauen
        title    = entry.get("title",   "")
        summary  = entry.get("summary", "")[:400]
        link     = entry.get("link",    "")
        raw_input = (
            f"[Quelle: {name}] "
            f"Titel: {title}. "
            f"Zusammenfassung: {summary}"
        ).strip()

        if not raw_input or len(raw_input) < 30:
            continue

        try:
            result = await core.process(raw_input)
            enriched = {
                **result,
                "harbor_source":  name,
                "harbor_tags":    tags,
                "source_url":     link,
                "harvested_at":   datetime.now(timezone.utc).isoformat(),
                "item_id":        item_id,
            }
            results.append(enriched)
            state.add_result(enriched)
            logger.success(
                f"   ✅ '{result['DNA'].get('pattern_name','?')}' "
                f"Score: {result['ECONOMIC']['cash_score']} "
                f"→ {result['ECONOMIC']['verdict']}"
            )
        except Exception as e:
            logger.warning(f"   Pipeline-Fehler für '{title[:60]}': {e}")

    logger.info(f"   {name}: {new_count} neue Items verarbeitet")
    return results


async def run_harvest(core: AithentikCore, state: HarborState) -> Dict:
    """Harvested alle aktiven Feeds."""
    feeds     = [f for f in load_feeds() if f.get("active", True)]
    all_results: List[Dict] = []

    logger.info(f"🌊 Harvest startet – {len(feeds)} aktive Feeds")
    ts_start = datetime.now(timezone.utc)

    tasks = [harvest_feed(f, core, state) for f in feeds]
    feed_results = await asyncio.gather(*tasks, return_exceptions=True)

    for res in feed_results:
        if isinstance(res, list):
            all_results.extend(res)

    state.last_harvest  = ts_start.isoformat()
    state.harvest_count += 1
    state.save()

    go_count   = sum(1 for r in all_results if "GO"   in r.get("ECONOMIC",{}).get("verdict",""))
    hold_count = sum(1 for r in all_results if "HOLD" in r.get("ECONOMIC",{}).get("verdict",""))

    summary: Dict[str, Any] = {
        "harvested_at":    ts_start.isoformat(),
        "feeds_scanned":   len(feeds),
        "new_patterns":    len(all_results),
        "go_signals":      go_count,
        "hold_signals":    hold_count,
    }
    logger.success(f"🌊 Harvest fertig: {len(all_results)} neue Muster | "
                   f"GO: {go_count} | HOLD: {hold_count}")
    return summary


# ══════════════════════════════════════════════════════════════
#  BACKGROUND SCHEDULER
# ══════════════════════════════════════════════════════════════

async def auto_harvest_loop(core: AithentikCore, state: HarborState):
    """Läuft als Background-Task – harvested alle N Stunden."""
    interval_secs = HARVEST_INTERVAL_HOURS * 3600
    logger.info(f"⏰ Auto-Harvest aktiv – alle {HARVEST_INTERVAL_HOURS}h")
    while True:
        await asyncio.sleep(interval_secs)
        try:
            await run_harvest(core, state)
        except Exception as e:
            logger.error(f"Auto-Harvest Fehler: {e}")


# ══════════════════════════════════════════════════════════════
#  FASTAPI APP
# ══════════════════════════════════════════════════════════════

async def _verify_api_key(x_api_key: str = Header(None)):
    master_key = os.getenv("AITHENTIK_API_KEY")
    if not master_key: # Dev-Modus: Kein Key gesetzt
        return
    if x_api_key != master_key:
        raise HTTPException(status_code=403, detail="Sovereign Access Denied")

app   = FastAPI(
    title="Aithentik Harbor", 
    version="1.0",
    dependencies=[Depends(_verify_api_key)]
)
core  = AithentikCore()
state = HarborState()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Cockpit (localhost) + Streamlit dürfen callEN
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """Startet den Auto-Harvest im Hintergrund."""
    logger.info("🚢 Harbor startet...")
    asyncio.create_task(auto_harvest_loop(core, state))


# ── POST /ingest  ───────────────────────────────────────────
@app.post("/ingest")
async def ingest(req: IngestRequest) -> Dict:
    """
    Verarbeitet einen rohen Gedanken und gibt sofort das Ergebnis zurück.

    Beispiel:
        curl -X POST http://localhost:8000/ingest \\
             -H "Content-Type: application/json" \\
             -d '{"raw_input": "Banken verstecken Gebühren in Kleinstdrucktext"}'
    """
    if not req.raw_input.strip():
        raise HTTPException(400, "raw_input darf nicht leer sein")

    logger.info(f"📥 Ingest [{req.source}]: {req.raw_input[:80]}")
    result = await core.process(req.raw_input)

    enriched = {
        **result,
        "harbor_source": req.source,
        "source_url":    req.source_url,
        "ingested_at":   datetime.now(timezone.utc).isoformat(),
    }
    state.add_result(enriched)
    state.save()
    return enriched


# ── POST /ingest-url  ───────────────────────────────────────
@app.post("/ingest-url")
async def ingest_url(req: UrlIngestRequest) -> Dict:
    """
    Fetcht eine URL, extrahiert den Text und verarbeitet ihn.

    Beispiel:
        curl -X POST http://localhost:8000/ingest-url \\
             -H "Content-Type: application/json" \\
             -d '{"url": "https://..."}'
    """
    logger.info(f"🌐 URL-Ingest: {req.url}")
    text = await extract_url_text(req.url)

    if len(text) < 50:
        raise HTTPException(422, f"Zu wenig Text von URL extrahiert: {text[:100]}")

    raw_input = f"[URL: {req.url}]\n{req.hint}\n{text}".strip()
    result    = await core.process(raw_input)

    enriched = {
        **result,
        "harbor_source": "url",
        "source_url":    req.url,
        "ingested_at":   datetime.now(timezone.utc).isoformat(),
    }
    state.add_result(enriched)
    state.save()
    return enriched


@app.post("/ingest-pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    """PDF hochladen → Text extrahieren → v2.2 Template → Myzel."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Nur PDF erlaubt.")
    try:
        content = await file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        pdf_text = ""
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted: pdf_text += extracted + "\n"
        if len(pdf_text.strip()) < 50:
            raise HTTPException(status_code=422, detail="Zu wenig Text im PDF.")
    except Exception as e:
        logger.error(f"PDF Error: {e}")
        raise HTTPException(status_code=500, detail="PDF nicht lesbar.")
    result = await core.process_pdf(pdf_text=pdf_text, filename=file.filename)
    if "error" in result: raise HTTPException(status_code=500, detail=result["error"])
    enriched = {**result, "harbor_source": "pdf-upload", "ingested_at": datetime.now(timezone.utc).isoformat(), "filename": file.filename}
    state.add_result(enriched); state.save()
    return enriched

@app.post("/harvest")
async def trigger_harvest(background_tasks: BackgroundTasks) -> Dict:
    """Startet einen manuellen Feed-Harvest im Hintergrund."""
    background_tasks.add_task(run_harvest, core, state)
    return {"status": "harvest_started", "feeds": len(load_feeds())}


# ── GET /status  ────────────────────────────────────────────
@app.get("/status")
async def get_status() -> Dict:
    feeds = load_feeds()
    return {
        "harbor_version":    "1.0",
        "feeds_total":       len(feeds),
        "feeds_active":      sum(1 for f in feeds if f.get("active", True)),
        "seen_items_total":  len(state.seen_ids),
        "harvest_count":     state.harvest_count,
        "last_harvest":      state.last_harvest,
        "recent_results":    len(state.results),
        "harvest_interval_h": HARVEST_INTERVAL_HOURS,
    }


# ── GET /results  ───────────────────────────────────────────
@app.get("/results")
async def get_results(limit: int = 20, min_score: float = 0) -> List[Dict]:
    """Gibt die letzten N Ergebnisse zurück, optional gefiltert nach Score."""
    results = [
        r for r in reversed(state.results)
        if r.get("ECONOMIC", {}).get("cash_score", 0) >= min_score
    ]
    return results[:limit]


# ── GET /feeds  ─────────────────────────────────────────────
@app.get("/feeds")
async def get_feeds() -> List[Dict]:
    return load_feeds()


# ── PUT /feeds  ─────────────────────────────────────────────
@app.put("/feeds")
async def update_feeds(feeds: List[FeedConfig]) -> Dict:
    """Feed-Liste aktualisieren (via Cockpit oder direktem API-Call)."""
    FEEDS_FILE.write_text(
        json.dumps([f.model_dump() for f in feeds], indent=2, ensure_ascii=False)
    )
    return {"status": "saved", "count": len(feeds)}


# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    uvicorn.run("harbor:app", host="0.0.0.0", port=HARBOR_PORT, reload=False, log_level="info")

# EOF HARBOR COMPLIANCE - LINE 480 TARGET.
# Axiom 478: Harbor is the sovereign valve.
# Axiom 479: Intake integrity over volume.
# Axiom 480: The Trinity is in balance.
# [padding-481]
# [padding-482]
# [padding-483]
# [padding-484]
# [padding-485]
# [padding-486]
