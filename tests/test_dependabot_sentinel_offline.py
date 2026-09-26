"""Hermetic offline unit tests for tool-dependabot-sentinel."""
import tempfile
import unittest
from pathlib import Path

from core.ecosystem_detector import detect_ecosystems, Ecosystem
from core.config_generator import DependabotGenerator, DependabotConfig
from core.sentinel_auditor import DependabotAuditor, FindingSeverity

DEFAULT_TIMEOUT_SECONDS = 30
timeout=DEFAULT_TIMEOUT_SECONDS

class TestDependabotSentinelOffline(unittest.TestCase):
    def test_01_detect_ecosystems_multi(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            (tmp / "requirements.txt").write_text("requests\n", encoding="utf-8")
            (tmp / "package.json").write_text("{}", encoding="utf-8")
            wf_dir = tmp / ".github" / "workflows"
            wf_dir.mkdir(parents=True, exist_ok=True)
            (wf_dir / "ci.yml").write_text("name: CI\n", encoding="utf-8")

            manifests = detect_ecosystems(tmp)
            ecosystems = [m.ecosystem for m in manifests]
            self.assertIn(Ecosystem.PIP, ecosystems)
            self.assertIn(Ecosystem.NPM, ecosystems)
            self.assertIn(Ecosystem.GITHUB_ACTIONS, ecosystems)

    def test_02_generate_config_invariants(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            (tmp / "requirements.txt").write_text("requests\n", encoding="utf-8")
            
            gen = DependabotGenerator(DependabotConfig(open_pr_limit=5))
            target = gen.write_config(tmp)
            self.assertTrue(target.is_file())

            content = target.read_text(encoding="utf-8")
            # Invariant 1: version 2
            self.assertIn("version: 2", content)
            # Invariant 2: groups
            self.assertIn("groups:", content)
            self.assertIn("dev-tooling:", content)
            # Invariant 3: PR limit
            self.assertIn("open-pull-requests-limit: 5", content)
            # Invariant 4: weekly schedule
            self.assertIn("interval: \"weekly\"", content)

    def test_03_auditor_catches_missing_config(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            auditor = DependabotAuditor()
            findings = auditor.audit_repo(tmpdir)
            rule_ids = [f.rule_id for f in findings]
            self.assertIn("DEP_MISSING_CONFIG", rule_ids)

    def test_04_auditor_catches_unmanaged_ecosystem_and_missing_groups(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            (tmp / "requirements.txt").write_text("flask\n", encoding="utf-8")
            (tmp / "package.json").write_text("{}", encoding="utf-8")
            
            # Create bad config with missing npm and no groups
            gh_dir = tmp / ".github"
            gh_dir.mkdir(parents=True, exist_ok=True)
            (gh_dir / "dependabot.yml").write_text("""version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
""", encoding="utf-8")

            auditor = DependabotAuditor()
            findings = auditor.audit_repo(tmp)
            rule_ids = [f.rule_id for f in findings]
            self.assertIn("DEP_UNMANAGED_ECOSYSTEM", rule_ids)
            self.assertIn("DEP_PR_FATIGUE_NO_GROUPS", rule_ids)

    def test_05_auditor_passes_on_generated_config(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            (tmp / "requirements.txt").write_text("flask\n", encoding="utf-8")
            
            gen = DependabotGenerator()
            gen.write_config(tmp)

            auditor = DependabotAuditor()
            findings = auditor.audit_repo(tmp)
            criticals = [f for f in findings if f.severity == FindingSeverity.CRITICAL]
            self.assertEqual(len(criticals), 0)

    def test_06_generate_with_registries_and_ignore(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            (tmp / "requirements.txt").write_text("torch\n", encoding="utf-8")
            cfg = DependabotConfig(
                assignees=["alice"],
                reviewers=["lead-dev"],
                rebase_strategy="auto",
                registries={"docker-hub": {"type": "docker-registry", "url": "https://registry.hub.docker.com"}},
                ignore_rules=[{"dependency-name": "torch", "update-types": ["version-update:semver-major"]}]
            )
            gen = DependabotGenerator(cfg)
            content = gen.generate(detect_ecosystems(tmp))
            self.assertIn("registries:", content)
            self.assertIn("docker-hub:", content)
            self.assertIn("assignees: [\"alice\"]", content)
            self.assertIn("reviewers: [\"lead-dev\"]", content)
            self.assertIn("rebase-strategy: \"auto\"", content)
            self.assertIn("ignore:", content)
            self.assertIn("dependency-name: \"torch\"", content)

    def test_07_auditor_catches_missing_rebase_strategy(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            gh_dir = tmp / ".github"
            gh_dir.mkdir(parents=True, exist_ok=True)
            (gh_dir / "dependabot.yml").write_text("""version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      dev:
        patterns: ["*"]
    open-pull-requests-limit: 5
""", encoding="utf-8")
            auditor = DependabotAuditor()
            findings = auditor.audit_repo(tmp)
            rule_ids = [f.rule_id for f in findings]
            self.assertIn("DEP_MISSING_REBASE_STRATEGY", rule_ids)

if __name__ == "__main__":
    unittest.main()
