# PTM Rules

Catalogue commun de signatures et règles de détection pour **Pixel Trackers Manager (PTM)**.

Ce dépôt est volontairement indépendant d’un CMS. Les adaptateurs WordPress, SPIP et futurs CMS embarquent une copie locale versionnée du catalogue : **aucun plugin PTM n’a besoin de contacter GitHub en production pour scanner un site**.

## Structure

- `VERSION` : version du catalogue ;
- `rules/services.json` : services externes, traceurs, médias, paiements et signatures techniques ;
- `rules/spip-plugins.json` : profils de plugins SPIP pertinents pour la vie privée ;
- `schema/` : schémas de validation ;
- `scripts/validate.py` : validation des catalogues et de leurs références croisées.

## Deux niveaux différents

Une **signature de service** représente une preuve observable dans le HTML ou une URL : Google Analytics, YouTube, Stripe.js, Gravatar, etc.

Un **profil de plugin SPIP** représente une capacité ou un traitement potentiel : Formidable peut collecter des réponses, Facteur peut utiliser un SMTP tiers, GIS peut appeler plusieurs fournisseurs de cartes. La présence du plugin seule n'est jamais transformée en preuve de traceur.

## Champs importants des services

- `id` : identifiant stable partagé entre CMS ;
- `patterns` : fragments observables dans le HTML/les URLs ;
- `category` : catégorie technique ;
- `privacy_kind` : nature du risque ou du traitement ;
- `ptm_category` : famille du consentement natif PTM ;
- `wp_consent_category` : catégorie WP Consent API lorsqu'une correspondance fiable existe ;
- `wordpress_plugin_slugs` : indices WordPress ;
- `spip_plugin_prefixes` : préfixes SPIP associés au service.

## Couverture SPIP

Le catalogue SPIP 0.2.0 couvre en priorité les familles pertinentes de l'écosystème SPIP 4.4 : statistiques, formulaires, newsletters/e-mail, anti-spam, médias/oEmbed, cartographie, réseaux sociaux, avatars, CMP, paiements, pages légales et import/export.

PTM-SPIP doit en plus inventorier **tous** les plugins actifs. Un plugin non catalogué ne disparaît donc pas : s'il semble lié aux données, à un formulaire, au tracking ou à un service externe, il est envoyé en vérification humaine.

## Principe

Une signature dit **ce que PTM a réellement reconnu**. Elle ne transforme pas automatiquement cette observation en conclusion juridique. Les cas ambigus restent en vérification humaine.

## Synchronisation

Les plugins embarquent un snapshot du JSON. Les mises à jour du catalogue sont relues, testées puis copiées dans chaque adaptateur lors d'une release. Pas de dépendance réseau à l'exécution.

## Licence

GPL-2.0-or-later, comme PTM WordPress et PTM SPIP.
