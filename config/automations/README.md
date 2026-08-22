# Automations Cursor — mode d'emploi

Les automations ne vivent pas *dans* Git comme des workflows GitHub Actions : elles sont créées dans l’UI Cursor, puis écrivent (ou commentent) dans ce repo via cloud agents.

Doc officielle : [Cursor Automations](https://cursor.com/docs/cloud-agent/automations).

## Statut

Les **5 automations** sont créées côté Cursor. Coller leurs URL/UUID dans le tableau en bas de ce fichier pour traçabilité.

## Pipeline

```text
#1 Veille quotidienne  ──PR──►  #5 Validation PR  ──merge──►  main
#2 Tendances           ──PR──►  #5
#3 Opportunités        ──PR──►  #5
#4 Validation marché   ──PR──►  #5
```

Ordre opérationnel :

```text
Maintenant     #1 tourne chaque jour ; #5 revue chaque PR
2–4 semaines   Historique data/daily suffisant
Ensuite        #2 → #3 → #4 sur schedule (ou manuel)
```

## Checklist commune (prod)

- [x] Automations créées dans Cursor
- [ ] URL / UUID renseignés ci-dessous
- [ ] #1 a produit au moins une PR de veille mergée
- [ ] #5 commente bien sur les PR du repo
- [ ] #2/#3/#4 activées seulement quand l’historique le justifie (ou laissées en pause)

## Cron / triggers suggérés (Europe/Paris)

| Automation | Trigger | Sens |
|------------|---------|------|
| 1 Veille | cron `0 6 * * *` | Tous les jours 06:00 |
| 2 Tendances | cron `0 7 * * 1` | Lundi 07:00 |
| 3 Opportunités | cron `0 8 * * 1` | Lundi 08:00 |
| 4 Validation marché | cron `0 9 * * 1` | Lundi 09:00 |
| 5 Validation PR | GitHub PR opened + pushed | À chaque PR |

## Modèles

- **#1** : Composer 2.5 Standard — collecte, tri, structuration.
- **#2 et #3** : modèles à fort raisonnement.
- **#4** : recherche web + synthèse.
- **#5** : modèle léger / Composer — checklist de conformité, pas de réécriture du fond.

## Fichiers de prompts

| Fichier | Automation |
|---------|------------|
| [`01-veille-quotidienne.md`](01-veille-quotidienne.md) | Collecte quotidienne |
| [`02-analyse-tendances.md`](02-analyse-tendances.md) | Tendances |
| [`03-detection-opportunites.md`](03-detection-opportunites.md) | Opportunités |
| [`04-validation-marche.md`](04-validation-marche.md) | Validation marché |
| [`05-validation-pr.md`](05-validation-pr.md) | Contrôle qualité des PR |

Si le prompt de ta #5 diffère, aligne-le sur `05-validation-pr.md` ou mets à jour ce fichier pour coller à la version live.

## Convention de PR

- `veille: YYYY-MM-DD (N items)`
- `tendances: 2026-W34 (N tendances)`
- `opportunites: 2026-W34 (N hypothèses)`
- `validation: 2026-W34`

Merger après feu vert de la #5 pour que le run suivant dispose de l’historique sur `main`.

## IDs d'automations

| Automation | URL / UUID |
|------------|------------|
| 1 Veille | _à coller_ |
| 2 Tendances | _à coller_ |
| 3 Opportunités | _à coller_ |
| 4 Validation marché | _à coller_ |
| 5 Validation PR | _à coller_ |
