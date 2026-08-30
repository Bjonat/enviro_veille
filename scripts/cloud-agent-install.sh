#!/usr/bin/env bash
# Idempotent bootstrap for enviro_veille cloud agents / automations.
# No language runtime deps — validates layout + JSON schemas only.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

required_paths=(
  README.md
  config/sources.yml
  config/themes.yml
  config/pipeline.yml
  config/schemas/daily.schema.json
  config/schemas/tendances.schema.json
  config/schemas/opportunites.schema.json
  config/schemas/validation.schema.json
  config/schemas/offres.schema.json
  config/be-personas.yml
  config/automations/01-veille-quotidienne.md
  config/automations/02-analyse-tendances.md
  config/automations/03-detection-opportunites.md
  config/automations/04-validation-marche.md
  config/automations/05-validation-pr.md
  config/automations/06-fiches-offre-be.md
  veille
  data/daily
  tendances
  opportunites
  validation
  offres
)

for path in "${required_paths[@]}"; do
  if [[ ! -e "$path" ]]; then
    echo "missing required path: $path" >&2
    exit 1
  fi
done

for schema in config/schemas/*.json config/examples/*.json; do
  python3 -m json.tool "$schema" > /dev/null
done

echo "enviro_veille install OK ($(date -u +%Y-%m-%dT%H:%M:%SZ))"
