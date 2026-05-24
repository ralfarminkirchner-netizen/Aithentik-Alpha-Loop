#!/usr/bin/env bash

cd /Users/ralfkirchner/.gemini/antigravity/scratch/Aithentik/alpha-loop

echo "Überprüfe Status der Docker Container..."
docker compose ps

echo "Starte Container neu..."
docker compose up -d

echo "Warte kurz auf den Start der Container..."
sleep 5

echo "Lade benötigte Ollama Modelle..."
docker exec alpha-loop-ollama-1 ollama pull deepseek-r1:latest
docker exec alpha-loop-ollama-1 ollama pull nomic-embed-text

echo "Backend Logs:"
docker logs alpha-loop-alpha-daemon-1 --tail 50

echo "Überprüfe Frontend auf Port 5173:"
curl -I http://localhost:5173
