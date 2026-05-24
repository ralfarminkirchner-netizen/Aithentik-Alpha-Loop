#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║          AITHENTIK ALPHA-LOOP DAEMON V3                      ║
║  Swarm Intelligence Architecture · Mission Ready             ║
║  Multi-Disciplinary Synthesis & Vector Storage               ║
╚══════════════════════════════════════════════════════════════╝

Dieses System ist ein gigantischer, interdisziplinärer Agenten-Swarm.
Rohe Ideen werden von verschiedenen Experten-Nodes debattiert:
- Psychology (Kognition, Verhalten, Emotion)
- Economics (Wirtschaftlichkeit, Cash-Score, Märkte)
- Biomimicry (Biologie, Evolution, Resilienz)
- Capital (Kapitalallokation, Risiko, ROI)

Danach werden die Synthese-Ergebnisse in Qdrant (Myzel-DB) archiviert.
"""

import os
import json
import asyncio
import uuid
import re
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

import aiohttp
from loguru import logger
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models
import ollama

# ══════════════════════════════════════════════════════════════
#  ENVIRONMENT & CONFIG
# ══════════════════════════════════════════════════════════════

load_dotenv()

QDRANT_URL      = os.getenv("QDRANT_URL", "http://localhost:6333")
OLLAMA_HOST     = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL           = os.getenv("MODEL", "deepseek-r1:latest")
EMBED_MODEL     = os.getenv("EMBED_MODEL", "nomic-embed-text")
COLLECTION_NAME = "alpha_loop_swarm_v3"

# ══════════════════════════════════════════════════════════════
#  NODE DEFINITIONS (SWARM)
# ══════════════════════════════════════════════════════════════

class ExpertNode:
    """Represents a single disciplinary expert in the swarm."""
    def __init__(self, name: str, discipline: str, role_prompt: str):
        self.name = name
        self.discipline = discipline
        self.role_prompt = role_prompt
        self.client = ollama.AsyncClient(host=OLLAMA_HOST)

    async def analyze(self, idea: str) -> str:
        prompt = f"""
        Idea to analyze: "{idea}"
        
        Provide a structured analysis focusing solely on your domain.
        Include pros, cons, and unique insights.
        """
        try:
            logger.info(f"[{self.discipline}] {self.name} is starting analysis...")
            t0 = time.time()
            res = await self.client.generate(
                model=MODEL,
                prompt=prompt,
                system=self.role_prompt
            )
            logger.info(f"[{self.discipline}] {self.name} finished in {time.time() - t0:.2f}s")
            return res.response
        except Exception as e:
            logger.error(f"[{self.discipline}] Error: {e}")
            return f"Error in {self.discipline} analysis."

class SynthesizerNode:
    """Consolidates expert opinions into a final structure."""
    def __init__(self):
        self.client = ollama.AsyncClient(host=OLLAMA_HOST)
        self.role_prompt = """
        You are the Master Synthesizer. Review the interdisciplinary expert analyses and extract the core DNA of the idea.
        You MUST output pure JSON, with no surrounding markdown or explanation.
        
        JSON Schema:
        {
          "pattern_name": "String",
          "core_mechanic": "String",
          "catalyst": "String",
          "synergies": ["String", "String"],
          "psychological_friction": "String",
          "economic_viability_score": 0-100,
          "biomimetic_resilience": "String",
          "capital_verdict": "GO | HOLD | DROP",
          "overall_cash_score": 0-150
        }
        """

    async def synthesize(self, idea: str, analyses: Dict[str, str]) -> Dict[str, Any]:
        context = "\\n\\n".join([f"=== {disc} ===\\n{text}" for disc, text in analyses.items()])
        prompt = f"Original Idea: {idea}\\n\\nExpert Analyses:\\n{context}\\n\\nSynthesize these into the required JSON."
        
        try:
            logger.info("[Synthesizer] Synthesizing final DNA...")
            res = await self.client.generate(
                model=MODEL,
                prompt=prompt,
                system=self.role_prompt,
                format="json"
            )
            
            # Try to parse
            text = res.response
            match = re.search(r"\\{.*\\}", text, re.DOTALL)
            if match:
                text = match.group()
            
            return json.loads(text)
        except Exception as e:
            logger.error(f"[Synthesizer] Error: {e}")
            return {"pattern_name": "Error", "error": str(e), "overall_cash_score": 0}

# ══════════════════════════════════════════════════════════════
#  ALPHA-LOOP CORE
# ══════════════════════════════════════════════════════════════

class AlphaLoopDaemon:
    def __init__(self):
        self.qdrant = QdrantClient(url=QDRANT_URL)
        self._ensure_collection()
        self.embed_client = ollama.AsyncClient(host=OLLAMA_HOST)
        
        self.experts = [
            ExpertNode(
                "Dr. Freud", "Psychology", 
                "You are an expert in behavioral psychology and cognitive science. Analyze ideas for user behavior patterns, cognitive load, dopamine loops, and emotional resonance. Identify psychological friction."
            ),
            ExpertNode(
                "Adam Smith", "Economics", 
                "You are a master economist. Analyze ideas for value creation, unit economics, supply/demand imbalances, pricing power, and market dynamics."
            ),
            ExpertNode(
                "Mother Nature", "Biomimicry", 
                "You are a biomimetic systems thinker. Analyze ideas using principles of biology and evolution. Look for organic growth, systemic resilience, symbiotic relationships, and resource efficiency."
            ),
            ExpertNode(
                "Warren Buffett", "Capital", 
                "You are a capital allocator. Analyze ideas for ROI, risk mitigation, defensibility (moats), compound interest effects, and scaling capital."
            )
        ]
        self.synthesizer = SynthesizerNode()

    def _ensure_collection(self):
        try:
            self.qdrant.get_collection(COLLECTION_NAME)
        except Exception:
            logger.info(f"Creating Qdrant Collection: {COLLECTION_NAME}")
            self.qdrant.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
            )

    async def ingest_idea(self, raw_idea: str) -> Dict[str, Any]:
        """Runs an idea through the Swarm and stores it in Qdrant."""
        logger.info(f"🚀 Alpha-Loop Swarm processing new idea: {raw_idea[:50]}...")
        
        # Round 1: Parallel processing by all experts
        tasks = [expert.analyze(raw_idea) for expert in self.experts]
        results = await asyncio.gather(*tasks)
        
        analyses = {expert.discipline: result for expert, result in zip(self.experts, results)}
        
        # Round 2: Synthesis
        synthesis = await self.synthesizer.synthesize(raw_idea, analyses)
        
        # Archiving in Myzel
        logger.info("Archiving in Myzel (Qdrant)...")
        pattern_name = synthesis.get("pattern_name", "Unknown Pattern")
        core_mechanic = synthesis.get("core_mechanic", "")
        
        try:
            emb_res = await self.embed_client.embeddings(model=EMBED_MODEL, prompt=f"{pattern_name}: {core_mechanic}")
            vector = emb_res.get("embedding", [])
        except Exception as e:
            logger.error(f"Embedding failed: {e}")
            vector = [0.0] * 768
            
        point_id = str(uuid.uuid4())
        
        payload = {
            "raw_idea": raw_idea,
            "synthesis": synthesis,
            "analyses": analyses,
            "timestamp": datetime.now().isoformat()
        }
        
        self.qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=[models.PointStruct(id=point_id, vector=vector, payload=payload)]
        )
        
        cash_score = synthesis.get("overall_cash_score", 0)
        logger.success(f"✅ Idea '{pattern_name}' archived! ID: {point_id} | Cash Score: {cash_score}")
        
        return {
            "id": point_id,
            "pattern_name": pattern_name,
            "synthesis": synthesis
        }

    async def daemon_loop(self):
        """Simulates a continuous daemon loop that could watch a queue/file/DB."""
        logger.info("Alpha-Loop Daemon V3 is running and listening for signals...")
        try:
            while True:
                # In a real system, this would pop from Redis/RabbitMQ or a polling directory
                await asyncio.sleep(5)
        except KeyboardInterrupt:
            logger.info("Shutting down daemon.")

# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) > 1:
        idea = " ".join(sys.argv[1:])
        asyncio.run(AlphaLoopDaemon().ingest_idea(idea))
    else:
        asyncio.run(AlphaLoopDaemon().daemon_loop())

