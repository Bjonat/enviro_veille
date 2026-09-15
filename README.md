# Radar de veille stratégique environnementale (France)

Système de veille en **deux rôles opérationnels** : une collecte quotidienne, puis un orchestrateur stratégique qui transforme la matière brute en tendances, opportunités validées et offres actionnables pour un bureau d'études environnementales.

```text
Sources web
   ↓
1. Veille quotidienne
   → veille/
   → data/daily/
   ↓
2. Orchestrateur stratégique v2
   → tendances/
   → opportunites/
   → validation/
   → offres/
   → validation déterministe
   → une PR par cycle
```

Objectif final : détecter tôt ce que les professionnels de l'environnement vont devoir **faire, acheter, mesurer, produire ou maîtriser**, puis identifier parmi ces évolutions celles qui créent réellement une activité vendable par un bureau d'études environnementales.

## Structure

```text
.
├── veille/                  # Lecture quotidienne (Markdown)
├── data/daily/              # Matière machine (JSON)
├── tendances/               # Dynamiques multi-semaines / mois
├── opportunites/            # Hypothèses de nouveaux besoins professionnels
├── validation/              # Preuves économiques / signaux marché
├── offres/                  # Fiches d'offre BE
├── scripts/
│   └── validate_pipeline.py # Contrôle déterministe du pipeline
├── config/
│   ├── sources.yml
│   ├── themes.yml
│   ├── be-personas.yml      # Filtre métier bureau d'études
│   ├── scoring.yml          # Barèmes v2 communs
│   ├── pipeline.yml         # Pipeline de référence
│   ├── schemas/
│   └── automations/
└── README.md
```

## Automations / agents

| Rôle | Déclencheur | Fonction | Prompt |
|------|-------------|----------|--------|
| Veille quotidienne | Quotidien | Collecte, tri, déduplication, structuration | [`01`](config/automations/01-veille-quotidienne.md) |
| Orchestrateur stratégique v2 | Hebdo ou manuel | Tendances → opportunités → validation marché → offres BE + QA + PR unique | [`02-06 v2`](config/automations/02-06-orchestrateur-strategique-v2.md) |

Le prompt v2 applique le prompt orchestrateur de base puis ajoute la continuité longitudinale, les barèmes de score, la qualification de la demande économique et le contrôle déterministe.

Les anciens prompts séparés `02` à `06` restent présents dans `config/automations/` comme historique et référence méthodologique, mais ne constituent plus le workflow opérationnel recommandé.

Guide : [`config/automations/README.md`](config/automations/README.md).

## Contrats de données

- Quotidien : [`config/schemas/daily.schema.json`](config/schemas/daily.schema.json)
- Tendances : [`config/schemas/tendances.schema.json`](config/schemas/tendances.schema.json)
- Opportunités : [`config/schemas/opportunites.schema.json`](config/schemas/opportunites.schema.json)
- Validation : [`config/schemas/validation.schema.json`](config/schemas/validation.schema.json)
- Offres BE : [`config/schemas/offres.schema.json`](config/schemas/offres.schema.json)
- Barèmes : [`config/scoring.yml`](config/scoring.yml)

Les nouveaux artefacts stratégiques sont produits avec `schema_version: "2.0"`. Les historiques antérieurs restent lisibles et ne doivent pas être réécrits uniquement pour migration.

## Validation locale

```bash
pip install -r requirements-dev.txt
python scripts/validate_pipeline.py
```

La même validation est exécutée en CI sur les PR qui touchent le pipeline ou ses données.

Le validateur contrôle notamment les schémas, les IDs, les références croisées, la provenance des preuves, les deltas de score et le gate `pret_a_prototyper`.

## Chaîne de causalité

Le système ne doit pas produire quatre rapports indépendants. Il doit maintenir une chaîne traçable :

```text
SIGNAL DE VEILLE
→ DYNAMIQUE
→ NOUVEAU BESOIN PROFESSIONNEL
→ PREUVE DE DEMANDE
→ OFFRE BE ACTIONNABLE
```

Si un maillon manque, le pipeline ne doit pas sauter artificiellement au suivant.

## Principes v2

- Sources primaires d'abord ; médias secondaires = détection puis remontée à la source.
- La veille quotidienne produit de la donnée propre, pas de business.
- Une tendance est une dynamique, pas une reliste d'actualités.
- Une tendance ou opportunité déjà connue conserve un `canonical_id` stable et documente son évolution.
- Les scores 1–5 suivent `config/scoring.yml` et ne montent pas uniquement parce qu'un sujet est à nouveau mentionné.
- Une opportunité reste une hypothèse tant qu'elle n'a pas de preuve économique.
- Une absence de preuve peut conduire à `non_confirme` et doit être conservée comme information.
- Une obligation réglementaire n'est pas automatiquement une demande externalisée.
- Une offre `pret_a_prototyper` exige une preuve de demande directe/externalisable et un vrai fit BE.
- Aucun AO, recrutement, budget, montant, entreprise, date ou URL ne doit être inventé.
- Un signal marché fort n'est une offre BE que s'il entre dans [`config/be-personas.yml`](config/be-personas.yml).
- Les offres reprennent uniquement les preuves déjà établies dans `validation/`.
- Un cycle stratégique utilise une seule branche et une seule PR.
