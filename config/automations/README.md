# Automations Cursor — mode d'emploi

Les automations ne vivent pas *dans* Git comme des workflows GitHub Actions : elles sont créées dans l’UI Cursor, puis écrivent dans ce repo via cloud agents + PR.

Doc officielle : [Cursor Automations](https://cursor.com/docs/cloud-agent/automations).

## Ordre de mise en service

```text
Semaine 0     Créer automation 1 (quotidienne) + laisser tourner
Semaines 2–4  Historique data/daily suffisant
Ensuite       Créer automation 2 (tendances)
              Créer automation 3 (opportunités) — idéalement 1 h après #2
              Créer automation 4 (validation) — idéalement 1 h après #3
```

## Checklist commune (chaque automation)

- [ ] Trigger schedule (cron) configuré
- [ ] Repository : `Bjonat/enviro_veille` (single repo) — **obligatoire** pour écrire des fichiers / ouvrir des PR
- [ ] Branche de base : `main`
- [ ] Prompt collé depuis le fichier `0N-….md` (section « Prompt à coller »)
- [ ] Modèle choisi selon le tableau du README racine
- [ ] Outil **Pull request creation** activé
- [ ] Memories activées (apprentissage inter-runs)
- [ ] Computer use activé pour #1 et #4 si la navigation web aide
- [ ] Automation activée (enabled)

## Cron suggérés (Europe/Paris)

| Automation | Cron | Sens |
|------------|------|------|
| 1 Veille | `0 6 * * *` | Tous les jours 06:00 |
| 2 Tendances | `0 7 * * 1` | Lundi 07:00 |
| 3 Opportunités | `0 8 * * 1` | Lundi 08:00 |
| 4 Validation | `0 9 * * 1` | Lundi 09:00 |

Alternative : #2/#3/#4 en mensuel (`0 7 1 * *`, etc.) si le volume quotidien est encore faible.

## Modèles

- **Automation 1** : Composer 2.5 Standard — collecte, tri, structuration, écriture de fichiers.
- **Automations 2 et 3** : modèles à fort raisonnement (coût plus élevé justifié).
- **Automation 4** : modèle capable en recherche web + synthèse ; éviter le modèle le plus léger.

## Fichiers

| Fichier | Automation |
|---------|------------|
| [`01-veille-quotidienne.md`](01-veille-quotidienne.md) | Collecte quotidienne |
| [`02-analyse-tendances.md`](02-analyse-tendances.md) | Tendances |
| [`03-detection-opportunites.md`](03-detection-opportunites.md) | Opportunités |
| [`04-validation-marche.md`](04-validation-marche.md) | Validation marché |

## Convention de PR

Les agents ouvrent des PR du type :

- `veille: YYYY-MM-DD (N items)`
- `tendances: 2026-W34 (N tendances)`
- `opportunites: 2026-W34 (N hypothèses)`
- `validation: 2026-W34`

Merger régulièrement vers `main` pour que le run suivant dispose de l’historique.

## IDs d'automations (à renseigner après création)

| Automation | URL / UUID |
|------------|------------|
| 1 Veille | _à coller_ |
| 2 Tendances | _à coller_ |
| 3 Opportunités | _à coller_ |
| 4 Validation | _à coller_ |
