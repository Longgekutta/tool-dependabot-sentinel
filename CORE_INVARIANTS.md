# CORE INVARIANTS: tool-dependabot-sentinel

1. Anti-Spam Invariance (PR Fatigueless):
   - Generated configuration MUST enforce semantic dependency grouping (`groups`) and PR limits (`open-pull-requests-limit <= 10`).

2. Ecosystem Exhaustiveness Invariance:
   - If `.github/workflows/` exists, `package-ecosystem: "github-actions"` MUST be included.
   - All detected root package manifests (pip, npm, cargo, gomod, docker) MUST be mapped.

3. Hermetic Generation Invariance:
   - Operates 100% offline with zero external network or GitHub API queries.
