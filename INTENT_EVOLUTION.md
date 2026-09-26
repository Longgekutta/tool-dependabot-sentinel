# INTENT EVOLUTION: tool-dependabot-sentinel

## Initial State
- Projects either have no Dependabot configuration or generate excessive un-grouped PRs that fatigue maintainers.

## Transduced Invariants
1. Automatic grouping of minor/patch and dev dependencies to consolidate PR volume.
2. Mandatory inclusion of GitHub Actions version tracking.
3. Strict PR throttling (`open-pull-requests-limit: 5`).
4. Standalone audit engine to verify existing dependabot.yml quality.
