# PTM Rules

Catalogue commun de signatures et règles de détection pour **Pixel Trackers Manager (PTM)**.

Ce dépôt est volontairement indépendant d’un CMS. Les adaptateurs WordPress, SPIP et futurs CMS embarquent une copie locale versionnée du catalogue : **aucun plugin PTM n’a besoin de contacter GitHub en production pour scanner un site**.

## Structure

- `VERSION` : version du catalogue ;
- `rules/services.json` : services, signatures et catégories ;
- `schema/services.schema.json` : schéma de validation ;
- `scripts/validate.py` : validation locale simple.

## Champs importants

- `id` : identifiant stable partagé entre CMS ;
- `patterns` : fragments observables dans le HTML/les URLs ;
- `category` : catégorie descriptive PTM ;
- `ptm_category` : famille du consentement natif PTM (`statistics`, `marketing`, `external`, `review`) ;
- `wp_consent_category` : catégorie WP Consent API lorsqu’une correspondance fiable existe ;
- `wordpress_plugin_slugs` : indices WordPress facultatifs, ignorés par SPIP.

## Principe

Une signature dit **ce que PTM a réellement reconnu**. Elle ne transforme pas automatiquement cette observation en conclusion juridique. Les cas ambigus restent `review` / vérification humaine.

## Synchronisation

Les plugins embarquent un snapshot du JSON. Les mises à jour du catalogue sont relues, testées puis copiées dans chaque adaptateur lors d’une release. Pas de dépendance réseau à l’exécution.

## Licence

GPL-2.0-or-later, comme PTM WordPress et PTM SPIP.
