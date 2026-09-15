# Orchestrateur d'analyse stratégique v2

Ce document est le point d'entrée opérationnel de l'orchestrateur stratégique.

Il faut d'abord lire et appliquer intégralement :

- `config/automations/02-06-orchestrateur-strategique.md`

Puis appliquer les règles v2 ci-dessous. En cas de conflit, **les règles v2 priment**.

---

## 0. CONTRATS V2 OBLIGATOIRES

Avant tout nouveau cycle, lis également :

- `config/scoring.yml`
- `scripts/validate_pipeline.py`

Tout nouveau fichier JSON produit dans `tendances/`, `opportunites/`, `validation/` ou `offres/` doit contenir :

```json
"schema_version": "2.0"
```

Les anciens fichiers sans `schema_version` constituent l'historique legacy. Ne les réécris pas uniquement pour les migrer.

---

## 1. CONTINUITÉ LONGITUDINALE : NE PAS RECRÉER LES SUJETS

Le pipeline doit suivre des **objets stratégiques dans le temps**, pas seulement produire des photographies hebdomadaires.

### Tendances

Chaque tendance v2 doit contenir :

- `canonical_id` : identifiant stable du sujet, indépendant de la période ;
- `first_seen` : première période connue ;
- `last_seen` : période courante ;
- `previous_period_id` : `id` de la tendance correspondante lors de la période précédente, ou `null` si réellement nouvelle ;
- `previous_status` : statut précédent, ou `null` ;
- `previous_acceleration_score` : score précédent, ou `null` ;
- `score_delta` : `acceleration_score - previous_acceleration_score`, ou `null` si nouvelle ;
- `evolution_note` : ce qui justifie la continuité, l'accélération, la décélération, la requalification ou la disparition.

Le `canonical_id` ne doit pas contenir le numéro de semaine ou la période.

Exemple :

`pfas-eau-boues`

et non :

`2026-W38-pfas-eau-boues`

L'`id` reste spécifique au fichier/période afin de préserver la traçabilité historique.

### Opportunités

Chaque opportunité v2 doit contenir :

- `canonical_id` ;
- `first_seen` ;
- `last_seen` ;
- `previous_period_id` ;
- `previous_confidence` ;
- `confidence_delta` ;
- `evolution_note`.

Une opportunité déjà observée ne doit pas être recréée artificiellement parce que son titre change légèrement.

Avant de créer un nouveau `canonical_id`, compare le besoin avec les 2 ou 3 périodes précédentes : acheteur, job-to-be-done, déclencheur et livrable attendu.

---

## 2. SCORING CALIBRÉ

Les trois scores ne sont pas des impressions libres.

Utilise strictement les définitions de :

`config/scoring.yml`

Cela concerne :

- `acceleration_score` des tendances ;
- `confidence` des opportunités ;
- `market_signal_strength` des validations.

Pour chaque changement de score d'un sujet existant, l'`evolution_note` doit expliquer quel nouveau signal justifie la hausse ou la baisse.

Ne hausse jamais un score uniquement parce que le même sujet est mentionné à nouveau.

---

## 3. DISTINGUER OBLIGATION ET DEMANDE ÉCONOMIQUE

Une réglementation peut créer du travail sans créer un marché externalisé.

Pour chaque preuve de `validation/`, renseigne obligatoirement `demand_signal` avec l'une des valeurs :

- `none` : information contextuelle, aucune demande économique démontrée ;
- `indirect` : besoin plausible mais pas d'achat, budget ou livrable externalisable démontré ;
- `direct` : un acteur cherche, finance, budgète ou demande effectivement une capacité, un service ou un livrable ;
- `externalisable` : preuve qu'un livrable compatible avec un prestataire externe / BE peut effectivement être acheté ou confié.

Utilise les définitions complètes de `config/scoring.yml`.

### Règle renforcée pour `pret_a_prototyper`

Une offre ne peut être `pret_a_prototyper` que si toutes les conditions suivantes sont remplies :

1. verdict marché = `signale_fort` ou `signale_modere` ;
2. `be_fit >= 4` ;
3. le besoin appartient réellement au périmètre BE défini dans `config/be-personas.yml` ;
4. au moins une preuve de validation qualifie une demande directe/externalisable parmi :
   - `appel_offres` ;
   - `financement` ;
   - `budget` ;
   - `demande_explicite` ;
5. une preuve de type `obligation` ne suffit que si `demand_signal = externalisable` et que le texte impose ou déclenche un livrable concret qu'un BE peut produire.

Un recrutement, un concurrent, un appel à projets ou une obligation générale peuvent renforcer le radar mais ne suffisent pas seuls à rendre une offre `pret_a_prototyper`.

Conséquence importante :

> « Il existe une nouvelle obligation » n'est pas équivalent à « il existe déjà une prestation vendable ».

---

## 4. PREUVES D'OFFRE STRICTEMENT HÉRITÉES DE LA VALIDATION

Une fiche `offres/` ne peut utiliser aucune nouvelle preuve trouvée directement au stade offre.

Chaque élément de `evidence_refs` doit correspondre exactement à une preuve existante dans la validation liée :

- même `title` ;
- même `url` ;
- même `type`.

Si `price_signal != "non chiffré"`, au moins une preuve de validation doit contenir le montant correspondant dans `amount_or_scale`.

Les offres BE actionnables doivent contenir au moins deux livrables concrets.

Une fiche `hors_metier_be` peut n'avoir qu'un livrable de clôture indiquant explicitement pourquoi rien ne doit être industrialisé.

---

## 5. CONTRÔLE DÉTERMINISTE AVANT PR

Le contrôle sémantique de l'orchestrateur reste nécessaire, mais il n'est plus suffisant.

Avant d'ouvrir une PR, exécute :

```bash
python scripts/validate_pipeline.py
```

Le validateur contrôle notamment :

- conformité JSON Schema ;
- unicité des IDs ;
- champs de continuité v2 ;
- cohérence des deltas de score ;
- existence des `daily_item_id` ;
- correspondance des URL de preuve avec les items de veille ;
- liens tendances → opportunités → validations → offres ;
- reprise exacte des preuves de validation dans les offres ;
- respect du gate `pret_a_prototyper` ;
- présence d'un montant de validation lorsqu'une offre utilise un `price_signal` chiffré.

Les artefacts legacy peuvent produire des warnings. Ils ne doivent pas être réécrits simplement pour les faire disparaître.

Tout **error** sur un artefact v2 est bloquant : corrige avant la PR.

La CI GitHub exécute le même validateur.

---

## 6. RESTITUTION : MONTRER LES TRAJECTOIRES

Dans la synthèse finale, ne te contente pas de classer les sujets du moment.

Pour les dynamiques principales, indique lorsque cela est utile :

- score précédent → score actuel ;
- confiance précédente → confiance actuelle ;
- ce qui a réellement provoqué le changement ;
- ce qui n'a pas évolué malgré de nouvelles mentions.

La priorité décisionnelle est donnée aux **changements d'état**, pas au volume d'actualités.

---

## PRINCIPE V2

La chaîne reste :

**SIGNAL DE VEILLE**
→ **DYNAMIQUE**
→ **NOUVEAU BESOIN PROFESSIONNEL**
→ **PREUVE DE DEMANDE**
→ **OFFRE BE ACTIONNABLE**

Mais désormais chaque objet doit aussi répondre à :

> Est-ce réellement nouveau, ou est-ce la maturation d'un sujet déjà connu ?

et chaque offre :

> Avons-nous une preuve de demande externalisable, ou seulement la preuve qu'un problème existe ?
