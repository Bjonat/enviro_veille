# Automations — mode d'emploi

Le système repose désormais sur **deux rôles opérationnels** :

```text
#1 Veille quotidienne
        ↓
#2–6 Orchestrateur stratégique
        ↓
Tendances → Opportunités → Validation marché → Offres BE
```

La veille quotidienne reste séparée. L'orchestrateur inspecte ensuite l'état réel du dépôt et reprend le workflow là où il s'est arrêté, au lieu d'exécuter aveuglément plusieurs automations en cascade.

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
| [`02-06-orchestrateur-strategique.md`](02-06-orchestrateur-strategique.md) | Tendances → opportunités → validation marché → offres BE + contrôle qualité + PR unique |

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

Le contrôle PR auparavant séparé est intégré à l'orchestrateur avant livraison :

- conformité aux schémas ;
- traçabilité des IDs ;
- vérification des preuves et URLs ;
- aucun AO, montant ou signal marché inventé ;
- aucune offre BE produite sans maillon économique suffisant.

La chaîne attendue est :

```text
SIGNAL DE VEILLE
→ DYNAMIQUE
→ NOUVEAU BESOIN PROFESSIONNEL
→ PREUVE DE DEMANDE
→ OFFRE BE ACTIONNABLE
```
