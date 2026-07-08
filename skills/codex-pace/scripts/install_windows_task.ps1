param(
    [Parameter(Mandatory=$true)]
    [ValidatePattern('^\d{2}:\d{2}$')]
    [string]$At,

    [string]$TaskName = "CodexPacePing",
    [string]$PythonPath,
    [string]$SkillDir
)

$ErrorActionPreference = "Stop"

if (-not $SkillDir) {
    $SkillDir = Join-Path $HOME ".codex\skills\codex-pace"
}

if (-not $PythonPath) {
    $BundledPython = Join-Path $HOME ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
    if (Test-Path $BundledPython) {
        $PythonPath = $BundledPython
    } else {
        $PythonPath = "python"
    }
}

$PingScript = Join-Path $SkillDir "scripts\ping_codex.py"
if (-not (Test-Path $PingScript)) {
    throw "ping_codex.py not found at $PingScript"
}

$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument "`"$PingScript`""
$Trigger = New-ScheduledTaskTrigger -Daily -At $At
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -StartWhenAvailable
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Force | Out-Null

[PSCustomObject]@{
    task_name = $TaskName
    daily_time = $At
    python = $PythonPath
    script = $PingScript
    log = (Join-Path $HOME ".codex\codex-pace\logs\anchor.log")
} | ConvertTo-Json -Depth 3
