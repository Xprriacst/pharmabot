#!/usr/bin/env python3
"""
Script pour charger des données de démonstration pharmaceutiques
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.rag_service import RAGService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Données de démonstration basées sur des informations pharmaceutiques publiques
DEMO_DATA = [
    {
        "title": "Paracétamol - Indications thérapeutiques",
        "content": """Le paracétamol est indiqué dans le traitement symptomatique des douleurs d'intensité légère à modérée et/ou des états fébriles.
        
        Indications principales:
        - Traitement symptomatique de la fièvre
        - Traitement des douleurs légères à modérées (maux de tête, états grippaux, douleurs dentaires, courbatures)
        - Alternative aux AINS en cas de contre-indication
        
        Posologie adulte:
        - 500 mg à 1 g par prise, à renouveler si besoin au bout de 4 à 6 heures minimum
        - Dose maximale: 4 g par jour
        - Ne pas dépasser 3 g/jour en cas d'insuffisance hépatique ou rénale
        
        Contre-indications:
        - Hypersensibilité au paracétamol
        - Insuffisance hépatocellulaire sévère
        
        Précautions d'emploi:
        - Risque d'hépatotoxicité en cas de surdosage
        - Prudence chez l'alcoolique chronique
        - Attention aux associations contenant du paracétamol (risque de surdosage)""",
        "url": "https://www.vidal.fr/medicaments/substances/paracetamol.html",
        "source_type": "vidal",
        "category": "medicament"
    },
    {
        "title": "Amoxicilline - Antibiotique à large spectre",
        "content": """L'amoxicilline est un antibiotique de la famille des bêta-lactamines, du groupe des aminopénicillines.
        
        Indications:
        - Infections ORL: angines, otites, sinusites
        - Infections broncho-pulmonaires
        - Infections urinaires
        - Infections digestives (Helicobacter pylori)
        - Prophylaxie de l'endocardite bactérienne
        
        Posologie adulte:
        - 1 g à 3 g par jour en 2 à 3 prises
        - Infections sévères: jusqu'à 6 g/jour en milieu hospitalier
        
        Contre-indications:
        - Allergie aux pénicillines ou aux bêta-lactamines
        - Mononucléose infectieuse (risque d'éruption cutanée)
        
        Effets indésirables fréquents:
        - Troubles digestifs (diarrhée, nausées)
        - Réactions cutanées
        - Candidoses
        
        Interactions:
        - Méthotrexate: majoration de la toxicité
        - Contraceptifs oraux: diminution possible de l'efficacité""",
        "url": "https://www.vidal.fr/medicaments/substances/amoxicilline.html",
        "source_type": "vidal",
        "category": "medicament"
    },
    {
        "title": "Aspirine (Acide acétylsalicylique) - Anti-inflammatoire et antiagrégant",
        "content": """L'aspirine est un anti-inflammatoire non stéroïdien (AINS) aux propriétés antalgiques, antipyrétiques et antiagrégantes plaquettaires.
        
        Indications selon la dose:
        - Faible dose (75-160 mg): prévention cardiovasculaire (antiagrégant plaquettaire)
        - Dose moyenne (500 mg-1g): traitement symptomatique de la douleur et de la fièvre
        - Forte dose (>3g/jour): action anti-inflammatoire
        
        Posologie antalgique/antipyrétique adulte:
        - 500 mg à 1 g par prise
        - Intervalles de 4 heures minimum
        - Maximum 3 g par jour
        
        Contre-indications:
        - Ulcère gastroduodénal évolutif
        - Syndrome hémorragique
        - Grossesse (3ème trimestre: contre-indication absolue)
        - Allergie aux AINS
        - Enfant de moins de 6 ans (syndrome de Reye)
        - Insuffisance hépatique ou rénale sévère
        
        Interactions majeures:
        - Anticoagulants: majoration du risque hémorragique
        - Méthotrexate: augmentation de la toxicité
        - Autres AINS: majoration des effets indésirables digestifs
        
        Précautions:
        - Risque d'hémorragie digestive
        - À prendre au cours des repas
        - Prudence chez les sujets âgés""",
        "url": "https://www.vidal.fr/medicaments/substances/acide-acetylsalicylique.html",
        "source_type": "vidal",
        "category": "medicament"
    },
    {
        "title": "Ibuprofène - AINS antipyrétique et antalgique",
        "content": """L'ibuprofène est un anti-inflammatoire non stéroïdien (AINS) dérivé de l'acide propionique.
        
        Indications:
        - Traitement symptomatique de la fièvre et de la douleur
        - Traitement de courte durée des rhumatismes inflammatoires
        - Dysménorrhées
        
        Posologie adulte:
        - Antalgique/antipyrétique: 200 à 400 mg par prise, 3 à 4 fois par jour (max 1200 mg/jour)
        - Anti-inflammatoire: 400 à 800 mg, 3 fois par jour (max 2400 mg/jour)
        
        Contre-indications:
        - Ulcère gastroduodénal évolutif
        - Insuffisance cardiaque sévère
        - Grossesse (3ème trimestre)
        - Allergie aux AINS
        - Insuffisance hépatique ou rénale sévère
        
        Effets indésirables:
        - Troubles digestifs (dyspepsie, douleurs abdominales)
        - Risque d'ulcère et d'hémorragie digestive
        - Réactions cutanées
        - Atteinte rénale (rare)
        
        Interactions:
        - Anticoagulants, antiagrégants plaquettaires
        - Lithium: augmentation de la lithémie
        - Méthotrexate: majoration de la toxicité
        - IEC, ARA II: risque d'insuffisance rénale aiguë""",
        "url": "https://www.vidal.fr/medicaments/substances/ibuprofene.html",
        "source_type": "vidal",
        "category": "medicament"
    },
    {
        "title": "Oméprazole - Inhibiteur de la pompe à protons",
        "content": """L'oméprazole est un inhibiteur de la pompe à protons (IPP) utilisé dans le traitement de l'ulcère et du reflux gastro-œsophagien.
        
        Indications:
        - Ulcère gastroduodénal
        - Reflux gastro-œsophagien (RGO)
        - Syndrome de Zollinger-Ellison
        - Éradication d'Helicobacter pylori (en association)
        - Prévention des lésions gastroduodénales induites par les AINS
        
        Posologie:
        - Ulcère duodénal: 20 mg une fois par jour pendant 2 à 4 semaines
        - RGO: 20 mg une fois par jour
        - Ulcère gastrique: 20 mg une fois par jour pendant 4 à 8 semaines
        
        Mode d'administration:
        - À prendre le matin avant le petit-déjeuner
        - Gélule à avaler entière (ne pas ouvrir ni croquer)
        
        Effets indésirables fréquents:
        - Céphalées
        - Troubles digestifs (diarrhée, constipation, nausées)
        - Augmentation des enzymes hépatiques
        
        Interactions:
        - Clopidogrel: diminution de l'effet antiagrégant
        - Méthotrexate: augmentation de la toxicité
        - Digoxine: augmentation de la digoxinémie
        
        Précautions:
        - Traitement prolongé: risque de carence en vitamine B12, magnésium
        - Masque les symptômes du cancer gastrique
        - Augmentation du risque de fractures osseuses en cas de traitement prolongé""",
        "url": "https://www.vidal.fr/medicaments/substances/omeprazole.html",
        "source_type": "vidal",
        "category": "medicament"
    },
    {
        "title": "Métronidazole - Antibiotique et antiparasitaire",
        "content": """Le métronidazole est un antibiotique de la famille des nitro-imidazolés, actif sur les bactéries anaérobies et certains parasites.
        
        Indications:
        - Infections à germes anaérobies
        - Amibiase intestinale et hépatique
        - Giardiase
        - Trichomonase urogénitale
        - Vaginoses bactériennes
        - Éradication d'Helicobacter pylori (en association)
        
        Posologie adulte:
        - Infections anaérobies: 500 mg 3 fois par jour
        - Amibiase: 1500 mg par jour en 3 prises pendant 7 à 10 jours
        - Trichomonase: 2 g en dose unique ou 500 mg 2 fois par jour pendant 7 jours
        
        Contre-indications:
        - Premier trimestre de grossesse
        - Allaitement
        - Antécédent de neuropathie périphérique
        
        Effet antabuse:
        - Interaction avec l'alcool: réaction type disulfirame (nausées, vomissements, flush)
        - Éviter l'alcool pendant le traitement et 48h après l'arrêt
        
        Effets indésirables:
        - Troubles digestifs (nausées, goût métallique)
        - Neuropathie périphérique (traitement prolongé)
        - Coloration foncée des urines (sans gravité)
        
        Interactions:
        - Anticoagulants oraux: majoration de l'effet
        - Lithium: augmentation de la lithémie
        - Disulfirame: risque de troubles psychiatriques""",
        "url": "https://www.meddispar.fr/medicaments/metronidazole.html",
        "source_type": "meddispar",
        "category": "medicament"
    },
    {
        "title": "Lévothyroxine - Hormone thyroïdienne",
        "content": """La lévothyroxine (L-thyroxine, T4) est une hormone thyroïdienne de synthèse utilisée dans le traitement de l'hypothyroïdie.
        
        Indications:
        - Hypothyroïdie de toute origine
        - Traitement substitutif après thyroïdectomie
        - Prévention de la récidive du goitre après thyroïdectomie
        - Traitement de certains goitres euthyroïdiens
        
        Posologie:
        - Dose initiale: 25 à 50 µg par jour
        - Augmentation progressive par paliers de 12,5 à 25 µg toutes les 2 à 4 semaines
        - Dose d'entretien: 100 à 200 µg par jour
        - Sujet âgé ou coronarien: débuter à 12,5 µg/jour
        
        Mode d'administration:
        - À jeun, 30 minutes avant le petit-déjeuner
        - Horaire régulier quotidien
        - Comprimé à avaler avec de l'eau
        
        Surveillance:
        - TSH (hormone thyréostimulante): contrôle à 6-8 semaines après changement de dose
        - Objectif: TSH normale (0,4 à 4 mUI/L)
        
        Interactions importantes:
        - Anticoagulants oraux: majoration de l'effet anticoagulant
        - Antidiabétiques: augmentation des besoins
        - Colestyramine, fer, calcium: diminution de l'absorption (espacer les prises de 2h)
        - Amiodarone: peut induire dysthyroïdie
        
        Effets indésirables (surdosage):
        - Signes d'hyperthyroïdie: tachycardie, palpitations, insomnie, tremblements
        - Amaigrissement
        - Sueurs
        
        Précautions:
        - Insuffisance coronarienne: introduction très progressive
        - Grossesse: poursuivre le traitement, adapter la dose
        - Ostéoporose: surveillance en cas de traitement prolongé à forte dose""",
        "url": "https://www.meddispar.fr/medicaments/levothyroxine.html",
        "source_type": "meddispar",
        "category": "medicament"
    },
    {
        "title": "Hypertension artérielle - Prise en charge",
        "content": """L'hypertension artérielle (HTA) est définie par une pression artérielle systolique ≥ 140 mmHg et/ou une pression artérielle diastolique ≥ 90 mmHg.
        
        Classification:
        - HTA légère (grade 1): 140-159/90-99 mmHg
        - HTA modérée (grade 2): 160-179/100-109 mmHg
        - HTA sévère (grade 3): ≥ 180/110 mmHg
        
        Mesures hygiéno-diététiques (systématiques):
        - Réduction de la consommation de sel (< 6 g/jour)
        - Activité physique régulière (30 min/jour)
        - Réduction pondérale si surpoids
        - Limitation de la consommation d'alcool
        - Arrêt du tabac
        
        Classes thérapeutiques principales:
        1. Diurétiques thiazidiques (hydrochlorothiazide, indapamide)
        2. Inhibiteurs de l'enzyme de conversion (IEC): énalapril, ramipril
        3. Antagonistes des récepteurs de l'angiotensine II (ARA II): losartan, valsartan
        4. Inhibiteurs calciques: amlodipine, diltiazem
        5. Bêtabloquants: aténolol, bisoprolol
        
        Stratégie thérapeutique:
        - Monothérapie initiale dans l'HTA légère
        - Bithérapie d'emblée dans l'HTA modérée à sévère
        - Associations privilégiées: IEC ou ARA II + diurétique ou inhibiteur calcique
        
        Objectifs tensionnels:
        - < 140/90 mmHg en général
        - < 130/80 mmHg si diabète ou haut risque cardiovasculaire
        - Chez le sujet âgé: < 150/90 mmHg initialement
        
        Complications de l'HTA non contrôlée:
        - AVC, insuffisance cardiaque, infarctus du myocarde
        - Insuffisance rénale chronique
        - Rétinopathie hypertensive
        - Artériopathie périphérique""",
        "url": "https://www.vidal.fr/maladies/coeur-circulation-veines/hypertension-arterielle.html",
        "source_type": "vidal",
        "category": "maladie"
    }
]

def main():
    logger.info("🚀 Chargement des données de démonstration...")
    
    try:
        rag_service = RAGService()
        rag_service.add_documents(DEMO_DATA)
        
        logger.info(f"✅ {len(DEMO_DATA)} documents chargés avec succès")
        
        # Test de recherche
        import asyncio
        async def test_search():
            results = await rag_service.search_documents("paracétamol", limit=3)
            logger.info(f"\n📊 Test de recherche 'paracétamol': {len(results)} résultats")
            if results:
                logger.info(f"   Premier résultat: {results[0]['title']}")
        
        asyncio.run(test_search())
        
        logger.info("\n✅ Base de données de démonstration prête !")
        logger.info("   Vous pouvez maintenant tester le chatbot avec des questions sur:")
        logger.info("   - Paracétamol, Amoxicilline, Aspirine, Ibuprofène")
        logger.info("   - Oméprazole, Métronidazole, Lévothyroxine")
        logger.info("   - Hypertension artérielle")
        
    except Exception as e:
        logger.error(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
