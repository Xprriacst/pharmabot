#!/usr/bin/env python3
"""Check ChromaDB status"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import chromadb
from app.config import settings

client = chromadb.PersistentClient(path=str(settings.CHROMA_DB_PATH))
collections = client.list_collections()

print(f"📊 ChromaDB Status:")
print(f"   Collections: {len(collections)}")

for collection in collections:
    count = collection.count()
    print(f"   - {collection.name}: {count} documents")
