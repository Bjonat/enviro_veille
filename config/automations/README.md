# Automations — mode d'emploi

Le système repose sur **deux rôles opérationnels** :

```text
#1 Veille quotidienne
        ↓
#2–6 Orchestrateur stratégique v2
        ↓
Tendances → Opportunités → Validation marché → Offres BE
        ↓
Validation déterministe → PR unique
```

La veille quotidienne reste séparée. L'orchestrateur inspecte l'état réel du dépôt et reprend le workflow là où il s'est arrêté, au lieu d'exécuter aveuglément plusieurs automations en cascade.

## Déclenchement recommandé

| Rôle | Trigger | Sens |
|------|---------|------|
| Veille quotidienne | cron `0 6 * * *` | Tous les jours à 06:00 |
| Orchestrateur stratégique | hebdomadaire ou manuel | Analyse l'état du repo et exécute uniquement les étapes nécessaires |

L'orchestrateur peut être lancé dans ChatGPT ou dans un agent disposant de l'accès GitHub et du Web.

## Prompts opérationnels

| Fichier | Rôle |
|---------|------|
| [`01-veille-quotidienne.md`](01-veille-quotidienne.md) | Collecte quotidienne |
| [`02-06-orchestrateur-strategique-v2.md`](02-06-orchestrateur-strategique-v2.md) | Point d'entrée v2 : applique le prompt de base + continuité + scoring + gate marché + validation déterministe |
| [`02-06-orchestrateur-strategique.md`](02-06-orchestrateur-strategique.md) | Prompt de base conservé et appelé par la v2 |

## Ce que change la v2

### Continuité

Les tendances et opportunités conservent un `canonical_id` stable d'une période à l'autre. Les nouveaux artefacts v2 documentent explicitement le score précédent, le delta et la raison du changement.

### Scores

`config/scoring.yml` définit les niveaux 1–5 pour :

- `acceleration_score` ;
- `confidence` ;
- `market_signal_strength`.

### Réglementation ≠ marché

Chaque preuve économique v2 qualifie son `demand_signal` : `none`, `indirect`, `direct` ou `externalisable`.

Une obligation réglementaire générale ne suffit plus à rendre une offre `pret_a_prototyper`. Il faut une demande directe/externalisable et un vrai fit BE.

### Validation déterministe

Avant PR :

```bash
python scripts/validate_pipeline.py
```

La CI GitHub exécute la même vérification.

Les historiques sans `schema_version` sont traités comme legacy et peuvent générer des warnings. Les nouveaux fichiers `schema_version: "2.0"` sont stricts.

## Anciens prompts séparés

Les fichiers suivants sont conservés comme **historique et référence méthodologique**, mais ne constituent plus le workflow recommandé :

- `02-analyse-tendances.md`
- `03-detection-opportunites.md`
- `04-validation-marche.md`
- `05-validation-pr.md`
- `06-fiches-offre-be.md`

Leur logique a été absorbée par l'orchestrateur.

## Principe de reprise d'état

À chaque run, l'orchestrateur doit d'abord comparer :

- les derniers `data/daily/` ;
- les dernières `tendances/` ;
- les dernières `opportunites/` ;
- les dernières `validation/` ;
- les dernières `offres/`.

Il ne recrée pas un étage déjà correctement produit.

Exemples :

- validation présente mais offres absentes → compléter seulement les offres ;
- nouvelles veilles depuis la dernière tendance → ouvrir un nouveau cycle ;
- aucun signal nouveau significatif → ne pas fabriquer artificiellement un nouveau rapport.

## Convention Git

Pour un cycle stratégique complet :

- branche : `chatgpt/radar-{P}`
- une seule PR vers `main`
- titre : `radar: {P} — tendances, opportunités, validation et offres`

La veille quotidienne conserve sa convention propre si elle continue à être livrée séparément.

## Contrôle qualité

Le contrôle combine désormais :

1. un contrôle sémantique par l'orchestrateur ;
2. `scripts/validate_pipeline.py` pour les invariants déterministes ;
3. la CI GitHub sur la PR.

La chaîne attendue est :

```text
SIGNAL DE VEILLE
→ DYNAMIQUE
→ NOUVEAU BESOIN PROFESSIONNEL
→ PREUVE DE DEMANDE
→ OFFRE BE ACTIONNABLE
```
