# Radar de veille stratégique environnementale (France)

Petit système en **4 automations Cursor** pour transformer la veille environnementale en radar d’opportunités professionnelles.

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
│   └── automations/         # Prompts + réglages des 4 automations
└── README.md
```

## Automatisations

| # | Rôle | Fréquence suggérée | Modèle | Prompt |
|---|------|--------------------|--------|--------|
| 1 | Collecte / tri / structuration | Quotidien (`0 6 * * *`) | **Composer 2.5 Standard** | [`config/automations/01-veille-quotidienne.md`](config/automations/01-veille-quotidienne.md) |
| 2 | Tendances | Hebdo ou mensuel | Raisonnement fort | [`config/automations/02-analyse-tendances.md`](config/automations/02-analyse-tendances.md) |
| 3 | Opportunités | Après #2 | Raisonnement fort | [`config/automations/03-detection-opportunites.md`](config/automations/03-detection-opportunites.md) |
| 4 | Validation marché | Après #3 | Raisonnement / recherche | [`config/automations/04-validation-marche.md`](config/automations/04-validation-marche.md) |

Les automations Cursor se créent sur [cursor.com/automations](https://cursor.com/automations) (compte-level). Ce repo versionne les **prompts**, la **config** et les **données produites**.

### Mise en place rapide

1. Ouvre [cursor.com/automations/new](https://cursor.com/automations/new).
2. Pour chaque fichier de `config/automations/` :
   - copie le **prompt** (bloc `text`) ;
   - applique le **trigger**, le **modèle** et le **repo** indiqués en tête de fichier ;
   - active la création de PR ;
   - pointe vers ce repository `Bjonat/enviro_veille`, branche `main`.
3. Lance d’abord l’automation 1 pendant 2–4 semaines pour constituer l’historique.
4. Active ensuite 2 → 3 → 4.

Guide détaillé : [`config/automations/README.md`](config/automations/README.md).

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

## Exemple de chemins

```text
veille/2026/08/2026-08-22.md
data/daily/2026/08/2026-08-22.json
tendances/2026/2026-W34.md
opportunites/2026/2026-W34.md
validation/2026/2026-W34.md
```
