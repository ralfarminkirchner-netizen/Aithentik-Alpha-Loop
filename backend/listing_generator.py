import json
from loguru import logger
from ollama import AsyncClient
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL = "deepseek-r1:latest"
ollama = AsyncClient(host=OLLAMA_HOST)

class ListingGenerator:
    """
    Generates AEO-optimized Etsy listings based on artistic DNA and market resonance.
    """
    async def generate_listing(self, dna: dict, resonance_score: float, trend: str) -> dict:
        logger.info(f"✨ Synthesizing listing for pattern: {dna['pattern_name']} (Resonance: {resonance_score}%)")
        
        prompt = f"""
        Du bist ein Experte für AI Marketing und Etsy AEO (Answer Engine Optimization).
        Erstelle ein verkaufsstarkes Listing für ein Kunstprodukt basierend auf dieser DNA:
        
        DNA: {json.dumps(dna)}
        Markt-Resonanz: {resonance_score}%
        Trend-Übereinstimmung: {trend}
        
        JSON ONLY OUTPUT:
        {{
            "aeo_title": "Ein Titel, der von KI-Antwortmaschinen (wie Perplexity) bevorzugt wird",
            "etsy_tags": ["Tag1", "Tag2", "... genaue 13 Tags"],
            "description": "Eine fesselnde Beschreibung, die die Geschichte der 'Vaterkunst' mit modernem Wohndesign verbindet.",
            "aeo_score": 95,
            "target_audience": "Zielgruppen-Definition"
        }}
        """
        
        try:
            resp = await ollama.generate(model=MODEL, prompt=prompt, format="json")
            return json.loads(resp['response'])
        except Exception as e:
            logger.error(f"Synthesis Error: {e}")
            return {
                "aeo_title": f"Original {dna['pattern_name']} Art Print",
                "etsy_tags": ["Art", "Wall Decor", "Handmade"],
                "description": dna['core_mechanic'],
                "aeo_score": 50,
                "target_audience": "Art Lovers"
            }

if __name__ == "__main__":
    import asyncio
    generator = ListingGenerator()
    async def test():
        listing = await generator.generate_listing(
            {"pattern_name": "Lasur-Mesh", "core_mechanic": "Layering of translucent oil colors"},
            85.0,
            "Minimalist Line Art"
        )
        print(json.dumps(listing, indent=4))
    asyncio.run(test())
