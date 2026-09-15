# Radar de veille stratégique environnementale (France)

Système de veille en **deux rôles opérationnels** : une collecte quotidienne, puis un orchestrateur stratégique qui transforme la matière brute en tendances, opportunités validées et offres actionnables pour un bureau d'études environnementales.

```text
Sources web
   ↓
1. Veille quotidienne
   → veille/
   → data/daily/
   ↓
2. Orchestrateur stratégique
   → tendances/
   → opportunites/
   → validation/
   → offres/
   → contrôle qualité transversal
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
├── config/
│   ├── sources.yml
│   ├── themes.yml
│   ├── be-personas.yml      # Filtre métier bureau d'études
│   ├── pipeline.yml         # Pipeline de référence
│   ├── schemas/
│   └── automations/
└── README.md
```

## Automations / agents

| Rôle | Déclencheur | Fonction | Prompt |
|------|-------------|----------|--------|
| Veille quotidienne | Quotidien | Collecte, tri, déduplication, structuration | [`01`](config/automations/01-veille-quotidienne.md) |
| Orchestrateur stratégique | Hebdo ou manuel | Tendances → opportunités → validation marché → offres BE + QA + PR unique | [`02-06`](config/automations/02-06-orchestrateur-strategique.md) |

Les anciens prompts séparés `02` à `06` restent présents dans `config/automations/` comme historique et référence méthodologique, mais ne constituent plus le workflow opérationnel recommandé.

Guide : [`config/automations/README.md`](config/automations/README.md).

## Contrats de données

- Quotidien : [`config/schemas/daily.schema.json`](config/schemas/daily.schema.json)
- Tendances : [`config/schemas/tendances.schema.json`](config/schemas/tendances.schema.json)
- Opportunités : [`config/schemas/opportunites.schema.json`](config/schemas/opportunites.schema.json)
- Validation : [`config/schemas/validation.schema.json`](config/schemas/validation.schema.json)
- Offres BE : [`config/schemas/offres.schema.json`](config/schemas/offres.schema.json)

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

## Principes

- Sources primaires d'abord ; médias secondaires = détection puis remontée à la source.
- La veille quotidienne produit de la donnée propre, pas de business.
- Une tendance est une dynamique, pas une reliste d'actualités.
- Une opportunité reste une hypothèse tant qu'elle n'a pas de preuve économique.
- Une absence de preuve peut conduire à `non_confirme` et doit être conservée comme information.
- Aucun AO, recrutement, budget, montant, entreprise, date ou URL ne doit être inventé.
- Un signal marché fort n'est une offre BE que s'il entre dans [`config/be-personas.yml`](config/be-personas.yml).
- Les offres reprennent uniquement les preuves déjà établies dans `validation/`.
- Un cycle stratégique utilise une seule branche et une seule PR.
