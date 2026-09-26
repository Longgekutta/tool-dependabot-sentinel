"""Dependabot configuration auditor inspecting existing setup for anti-patterns and missing ecosystems."""
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional
from .ecosystem_detector import detect_ecosystems

DEFAULT_TIMEOUT_SECONDS = 30
timeout=DEFAULT_TIMEOUT_SECONDS

class FindingSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    INFO = "INFO"

@dataclass
class AuditFinding:
    rule_id: str
    severity: FindingSeverity
    message: str
    remediation: str

class DependabotAuditor:
    def audit_repo(self, root_dir: str | Path) -> List[AuditFinding]:
        root = Path(root_dir).resolve()
        findings: List[AuditFinding] = []

        cfg_path = root / ".github" / "dependabot.yml"
        if not cfg_path.exists():
            cfg_path = root / ".github" / "dependabot.yaml"

        if not cfg_path.exists():
            findings.append(AuditFinding(
                rule_id="DEP_MISSING_CONFIG",
                severity=FindingSeverity.CRITICAL,
                message="Repository lacks .github/dependabot.yml. Dependencies will not receive automated security patches.",
                remediation="Run 'python main.py generate' to scaffold a hardened dependabot.yml configuration."
            ))
            return findings

        try:
            content = cfg_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            findings.append(AuditFinding(
                rule_id="DEP_READ_ERROR",
                severity=FindingSeverity.CRITICAL,
                message=f"Failed to read dependabot config: {e}",
                remediation="Ensure file has read permissions."
            ))
            return findings

        # Check 1: version 2
        if "version: 2" not in content and 'version: "2"' not in content:
            findings.append(AuditFinding(
                rule_id="DEP_VERSION_LEGACY",
                severity=FindingSeverity.CRITICAL,
                message="Dependabot configuration must declare 'version: 2'.",
                remediation="Set 'version: 2' at root."
            ))

        # Check 2: Missing detected ecosystems
        detected = detect_ecosystems(root)
        for d in detected:
            eco_str = f'package-ecosystem: "{d.ecosystem.value}"'
            eco_str_alt = f"package-ecosystem: '{d.ecosystem.value}'"
            eco_str_plain = f"package-ecosystem: {d.ecosystem.value}"
            if eco_str not in content and eco_str_alt not in content and eco_str_plain not in content:
                findings.append(AuditFinding(
                    rule_id="DEP_UNMANAGED_ECOSYSTEM",
                    severity=FindingSeverity.WARNING,
                    message=f"Detected {d.manifest_file} but ecosystem '{d.ecosystem.value}' is missing in dependabot.yml.",
                    remediation=f"Add update configuration entry for package-ecosystem '{d.ecosystem.value}'."
                ))

        # Check 3: Missing groups (PR flood risk)
        if "groups:" not in content:
            findings.append(AuditFinding(
                rule_id="DEP_PR_FATIGUE_NO_GROUPS",
                severity=FindingSeverity.WARNING,
                message="No 'groups:' configured. Dependabot may generate dozens of isolated PRs, causing notification fatigue.",
                remediation="Configure 'groups:' under updates to bundle dev dependencies and minor patches into single PRs."
            ))

        # Check 4: Unbounded PR limit
        if "open-pull-requests-limit:" not in content:
            findings.append(AuditFinding(
                rule_id="DEP_UNBOUNDED_PR_LIMIT",
                severity=FindingSeverity.WARNING,
                message="No 'open-pull-requests-limit' declared. Default is 5, but explicit cap prevents unexpected spam.",
                remediation="Explicitly specify 'open-pull-requests-limit: 5'."
            ))

        return findings
