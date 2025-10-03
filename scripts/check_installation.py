#!/usr/bin/env python3
"""
Script pour vérifier que l'installation est correcte
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} (requis: 3.10+)")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required = [
        'fastapi',
        'uvicorn',
        'langchain',
        'chromadb',
        'openai',
        'beautifulsoup4',
        'aiohttp'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (manquant)")
            missing.append(package)
    
    return len(missing) == 0

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path(__file__).parent.parent / 'backend' / '.env'
    
    if not env_path.exists():
        print("❌ Fichier .env manquant")
        return False
    
    print("✅ Fichier .env existe")
    
    # Check for API key
    with open(env_path) as f:
        content = f.read()
        if 'OPENAI_API_KEY=' in content and 'sk-' in content:
            print("✅ Clé API OpenAI configurée")
            return True
        else:
            print("⚠️  Clé API OpenAI non configurée")
            return False

def check_data():
    """Check if data has been scraped"""
    data_path = Path(__file__).parent.parent / 'backend' / 'data' / 'chroma_db'
    
    if data_path.exists() and any(data_path.iterdir()):
        print("✅ Base de données ChromaDB existe")
        return True
    else:
        print("⚠️  Aucune donnée indexée (lancez: python scripts/scrape_data.py)")
        return False

def check_frontend():
    """Check if frontend is configured"""
    package_json = Path(__file__).parent.parent / 'frontend' / 'package.json'
    node_modules = Path(__file__).parent.parent / 'frontend' / 'node_modules'
    
    if not package_json.exists():
        print("❌ package.json manquant")
        return False
    
    print("✅ package.json existe")
    
    if node_modules.exists():
        print("✅ node_modules installé")
        return True
    else:
        print("⚠️  Dépendances npm non installées (lancez: npm install)")
        return False

def main():
    print("🔍 Vérification de l'installation PharmaBot")
    print("=" * 50)
    
    checks = [
        ("Version Python", check_python_version()),
        ("Dépendances Python", check_dependencies()),
        ("Configuration .env", check_env_file()),
        ("Données indexées", check_data()),
        ("Frontend", check_frontend()),
    ]
    
    print("\n" + "=" * 50)
    print("📊 Résumé:")
    
    all_passed = all(result for _, result in checks)
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    print(f"   {passed}/{total} vérifications passées")
    
    if all_passed:
        print("\n✅ Installation complète! Vous pouvez démarrer l'application.")
        print("\nCommandes:")
        print("  Backend:  cd backend && uvicorn app.main:app --reload")
        print("  Frontend: cd frontend && npm run dev")
    else:
        print("\n⚠️  Installation incomplète. Consultez SETUP.md")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
