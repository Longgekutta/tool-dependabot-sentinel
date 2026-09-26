# PowerShell runner for tool-dependabot-sentinel
param(
    [string]$Command = "health",
    [string]$Target = "."
)

switch ($Command) {
    "setup"    { python main.py setup }
    "run"      { python main.py run --target $Target }
    "test"     { python main.py test }
    "health"   { python main.py health }
    "clean"    { python main.py clean }
    "generate" { python main.py generate --target $Target }
    "audit"    { python main.py audit --target $Target }
    Default    { python main.py $Command }
}
