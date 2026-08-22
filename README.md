# Radar de veille stratégique environnementale (France)

Petit système en **5 automations Cursor** : 4 pour le pipeline de veille → opportunités, plus 1 garde-fou sur les PR.

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
                                    ↑
5. Validation PR  ←───────────────┘  (contrôle qualité à chaque PR)
```

Objectif : détecter suffisamment tôt ce que les professionnels de l’environnement vont devoir **faire, acheter, mesurer, produire ou maîtriser** — et vérifier ensuite si le marché le confirme (AO, recrutements, AAP, budgets, concurrents, obligations).

## Structure

```text
.
├── veille/                  # Lecture quotidienne (Markdown)
├── data/daily/              # Matière machine (JSON)
├── tendances/               # Synthèses multi-semaines / mois
├── opportunites/            # Hypothèses professionnelles
├── validation/              # Preuves économiques
├── config/
│   ├── sources.yml          # Sources primaires, secondaires, marché
│   ├── themes.yml           # Thématiques surveillées
│   ├── schemas/             # Contrats JSON
│   └── automations/         # Prompts + réglages des automations
└── README.md
```

## Automatisations

Statut : **créées** dans Cursor (IDs à coller dans [`config/automations/README.md`](config/automations/README.md)).

| # | Rôle | Déclencheur | Modèle | Prompt |
|---|------|-------------|--------|--------|
| 1 | Collecte / tri / structuration | Quotidien (`0 6 * * *`) | **Composer 2.5 Standard** | [`01-veille-quotidienne.md`](config/automations/01-veille-quotidienne.md) |
| 2 | Tendances | Hebdo / mensuel | Raisonnement fort | [`02-analyse-tendances.md`](config/automations/02-analyse-tendances.md) |
| 3 | Opportunités | Après #2 | Raisonnement fort | [`03-detection-opportunites.md`](config/automations/03-detection-opportunites.md) |
| 4 | Validation marché | Après #3 | Raisonnement / recherche | [`04-validation-marche.md`](config/automations/04-validation-marche.md) |
| 5 | Contrôle qualité des PR | PR opened / pushed | Léger / Composer | [`05-validation-pr.md`](config/automations/05-validation-pr.md) |

Les automations Cursor vivent sur [cursor.com/automations](https://cursor.com/automations). Ce repo versionne les **prompts**, la **config** et les **données produites**.

### Suite opérationnelle

1. Laisser tourner l’automation **#1** pour constituer `data/daily/`.
2. Merger régulièrement les PR de veille vers `main` (après passage de la **#5**).
3. Après 2–4 semaines d’historique, laisser #2 → #3 → #4.

Guide : [`config/automations/README.md`](config/automations/README.md).

## Contrats de données

- Quotidien : [`config/schemas/daily.schema.json`](config/schemas/daily.schema.json)  
  → `veille/YYYY/MM/YYYY-MM-DD.md` + `data/daily/YYYY/MM/YYYY-MM-DD.json`
- Tendances : [`config/schemas/tendances.schema.json`](config/schemas/tendances.schema.json)
- Opportunités : [`config/schemas/opportunites.schema.json`](config/schemas/opportunites.schema.json)
- Validation : [`config/schemas/validation.schema.json`](config/schemas/validation.schema.json)

## Principes

- **Sources primaires d’abord** (OFB, INPN, PatriNat, MNHN, DREAL, ADEME, Cerema, SDES, IGEDD, BRGM, agences de l’eau, Légifrance, Sénat, Commission européenne…).
- Les médias (Actu-Environnement, Localtis, Reporterre, etc.) détectent ; on remonte à la source quand c’est possible.
- L’automation 1 produit de la **donnée propre**, pas du business.
- Les automations 2–4 raisonnent sur l’historique pour bâtir le radar professionnel.
- L’automation 5 empêche de merger du bruit ou des hallucinations.

## Exemple de chemins

```text
veille/2026/08/2026-08-22.md
data/daily/2026/08/2026-08-22.json
tendances/2026/2026-W34.md
opportunites/2026/2026-W34.md
validation/2026/2026-W34.md
```
