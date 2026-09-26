"""Core modules for tool-dependabot-sentinel."""
from .ecosystem_detector import Ecosystem, detect_ecosystems
from .config_generator import DependabotGenerator, DependabotConfig
from .sentinel_auditor import DependabotAuditor, AuditFinding

__all__ = [
    "Ecosystem",
    "detect_ecosystems",
    "DependabotGenerator",
    "DependabotConfig",
    "DependabotAuditor",
    "AuditFinding",
]
