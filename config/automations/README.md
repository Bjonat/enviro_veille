# Automations Cursor — mode d'emploi

Les automations se créent dans l’UI Cursor, puis écrivent (ou commentent) dans ce repo.

## Pipeline

```text
#1 Veille  →  #2 Tendances  →  #3 Opportunités  →  #4 Validation  →  #6 Offres BE
                 toutes les PR passent par #5
```

## Cron / triggers suggérés (Europe/Paris)

| Automation | Trigger | Sens |
|------------|---------|------|
| 1 Veille | cron `0 6 * * *` | Tous les jours 06:00 |
| 2 Tendances | cron `0 7 * * 1` | Lundi 07:00 |
| 3 Opportunités | cron `0 8 * * 1` | Lundi 08:00 |
| 4 Validation marché | cron `0 9 * * 1` | Lundi 09:00 |
| 6 Fiches offre BE | cron `0 10 * * 1` | Lundi 10:00 |
| 5 Validation PR | GitHub PR opened + pushed | À chaque PR |

## Modèles

- **#1** : Composer 2.5 — collecte.
- **#2, #3, #6** : raisonnement fort.
- **#4** : recherche web + synthèse.
- **#5** : checklist, pas de réécriture du fond.

## Fichiers de prompts

| Fichier | Automation |
|---------|------------|
| [`01-veille-quotidienne.md`](01-veille-quotidienne.md) | Collecte quotidienne |
| [`02-analyse-tendances.md`](02-analyse-tendances.md) | Tendances |
| [`03-detection-opportunites.md`](03-detection-opportunites.md) | Opportunités (filtre BE) |
| [`04-validation-marche.md`](04-validation-marche.md) | Validation marché |
| [`05-validation-pr.md`](05-validation-pr.md) | Contrôle qualité des PR |
| [`06-fiches-offre-be.md`](06-fiches-offre-be.md) | Fiches offre bureau d'études |

## Convention de PR

- `veille: YYYY-MM-DD (N items)`
- `tendances: 2026-W36 (N tendances)`
- `opportunites: 2026-W36 (N hypothèses)`
- `validation: 2026-W36`
- `offres: 2026-W36 (N fiches)`

## IDs d'automations

| Automation | URL / UUID |
|------------|------------|
| 1 Veille | _à coller_ |
| 2 Tendances | _à coller_ |
| 3 Opportunités | _à coller_ |
| 4 Validation marché | _à coller_ |
| 5 Validation PR | _à coller_ |
| 6 Fiches offre BE | _à créer dans Cursor à partir de `06-fiches-offre-be.md`_ |
