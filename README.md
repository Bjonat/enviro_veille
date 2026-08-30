# Radar de veille stratégique environnementale (France)

Petit système en **6 automations Cursor** : 4 pour le pipeline de veille → marché, 1 garde-fou PR, 1 pour les **fiches d'offre d'un bureau d'études**.

```text
Sources web
   ↓
1. Veille quotidienne          →  veille/ + data/daily/
   ↓
2. Analyse de tendances        →  tendances/
   ↓
3. Détection d'opportunités    →  opportunites/
   ↓
4. Validation marché           →  validation/
   ↓
6. Fiches offre BE             →  offres/
                                    ↑
5. Validation PR  ←───────────────�. Fiches offre BE             →  offres/
                                    ↑
5. Validation PR  ←───────────────┘
```

Objectif final : détecter tôt ce qu'un **bureau d'études environnementale** pourra proposer (prestation, donnée, expertise, méthode) — pas seulement faire de la veille.

## Structure

```text
.
├── veille/                  # Lecture quotidienne (Markdown)
├── data/daily/              # Matière machine (JSON)
├── tendances/               # Synthèses multi-semaines / mois
├── opportunites/            # Hypothèses professionnelles
├── validation/              # Preuves économiques
├── offres/                  # Fiches d'offre BE
├── config/
│   ├── sources.yml
│   ├── themes.yml
│   ├── be-personas.yml      # Filtre métier bureau d'études
│   ├── schemas/
│   └── automations/
└── README.md
```

## Automatisations

| # | Rôle | Déclencheur | Modèle | Prompt |
|---|------|-------------|--------|--------|
| 1 | Collecte / tri / structuration | Quotidien | Composer 2.5 | [`01`](config/automations/01-veille-quotidienne.md) |
| 2 | Tendances | Hebdo | Raisonnement fort | [`02`](config/automations/02-analyse-tendances.md) |
| 3 | Opportunités (filtre BE) | Après #2 | Raisonnement fort | [`03`](config/automations/03-detection-opportunites.md) |
| 4 | Validation marché | Après #3 | Recherche | [`04`](config/automations/04-validation-marche.md) |
| 5 | Contrôle qualité des PR | PR opened / pushed | Léger | [`05`](config/automations/05-validation-pr.md) |
| 6 | Fiches offre BE | Après #4 | Raisonnement fort | [`06`](config/automations/06-fiches-offre-be.md) |

Guide : [`config/automations/README.md`](config/automations/README.md).

## Contrats de données

- Quotidien : [`config/schemas/daily.schema.json`](config/schemas/daily.schema.json)
- Tendances : [`config/schemas/tendances.schema.json`](config/schemas/tendances.schema.json)
- Opportunités : [`config/schemas/opportunites.schema.json`](config/schemas/opportunites.schema.json)
- Validation : [`config/schemas/validation.schema.json`](config/schemas/validation.schema.json)
- Offres BE : [`config/schemas/offres.schema.json`](config/schemas/offres.schema.json)

## Principes

- Sources primaires d'abord ; médias = détection puis remontée à la source.
- Automation 1 = donnée propre, pas de business.
- Automations 2–4 = radar professionnel.
- Automation 6 = brief commercial interne (livrables, acheteur, action du mois). Ne pas inventer d'AO ni de montants.
- Un signal marché fort n'est une offre BE que s'il entre dans [`config/be-personas.yml`](config/be-personas.yml).
