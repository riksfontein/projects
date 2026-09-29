# diagnose-claude-hang.ps1
# Finds what makes every new Claude Code session hang on this laptop.
#
# Run it in a normal PowerShell window (not inside Claude Code):
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\diagnose-claude-hang.ps1
#
# It does not change, delete or install anything. Every check has a timeout,
# so a stuck drive or port shows up as "HUNG" instead of freezing the script.
# The last step starts three tiny "reply with ok" Claude runs (a few tokens each)
# to see WHERE the hang happens. Skip that with -SkipLiveTest.
#
# When it finishes, paste the whole output back into a Claude session.

param([switch]$SkipLiveTest)

$ErrorActionPreference = 'Continue'
$script:flags = @()
$drive   = 'G:\My Drive\_RXClaude'
$claudeH = Join-Path $HOME '.claude'

function Section($t) { Write-Host "`n=== $t ===" -ForegroundColor Cyan }
function Flag($t)    { $script:flags += $t; Write-Host "  [!] $t" -ForegroundColor Yellow }
function Ok($t)      { Write-Host "  [ok] $t" -ForegroundColor Green }
function Info($t)    { Write-Host "  $t" }

# Runs a script block in a background job with a hard timeout.
function Timed($label, [scriptblock]$sb, $timeoutSec = 20, [object[]]$argList = @()) {
  $sw  = [Diagnostics.Stopwatch]::StartNew()
  $job = Start-Job -ScriptBlock $sb -ArgumentList $argList
  $done = Wait-Job $job -Timeout $timeoutSec
  $ms = $sw.ElapsedMilliseconds
  $out = $null
  if ($done) { $out = Receive-Job $job 2>&1 } else { Stop-Job $job }
  Remove-Job $job -Force
  [pscustomobject]@{ Label = $label; TimedOut = -not $done; Ms = $ms; Output = $out }
}
function Report($r, $slowMs = 5000) {
  if ($r.TimedOut)          { Flag "$($r.Label): HUNG - no answer in $([int]($r.Ms / 1000))s" }
  elseif ($r.Ms -gt $slowMs) { Flag "$($r.Label): slow ($($r.Ms) ms)" }
  else                       { Ok   "$($r.Label): $($r.Ms) ms" }
}
function ReadJson($path) {
  if (-not (Test-Path $path)) { return $null }
  try { Get-Content $path -Raw | ConvertFrom-Json } catch { Flag "$path is not valid JSON: $($_.Exception.Message)"; $null }
}

# ---------------------------------------------------------------------------
Section 'Claude Code install and running processes'
$claudeCmd = (Get-Command claude -ErrorAction SilentlyContinue).Source
if (-not $claudeCmd) { Flag 'claude is not on PATH' } else {
  Info "claude = $claudeCmd"
  $r = Timed 'claude --version' { param($c) & $c --version } 30 @($claudeCmd)
  Report $r; if ($r.Output) { Info "version: $($r.Output)" }
}
$procs = @(Get-Process claude -ErrorAction SilentlyContinue)
Info "claude processes running now: $($procs.Count)"
$old = @($procs | Where-Object { $_.StartTime -lt (Get-Date).AddHours(-6) })
if ($old.Count -gt 0) {
  Flag "$($old.Count) claude process(es) older than 6h are still running (stuck sessions that never exited)"
  $old | ForEach-Object { Info ("    PID {0}  started {1}  RAM {2} MB" -f $_.Id, $_.StartTime, [int]($_.WorkingSet64 / 1MB)) }
}
$nodeCount = @(Get-Process node -ErrorAction SilentlyContinue).Count
Info "node processes running now: $nodeCount  (MCP servers, OmniRoute, etc.)"
if ($nodeCount -gt 40) { Flag "$nodeCount node processes - leftover MCP servers from old sessions are piling up" }

# ---------------------------------------------------------------------------
Section 'Where Claude sends its requests (API routing)'
$settings      = ReadJson (Join-Path $claudeH 'settings.json')
$settingsLocal = ReadJson (Join-Path $claudeH 'settings.local.json')
$names = 'ANTHROPIC_BASE_URL','ANTHROPIC_API_KEY','ANTHROPIC_AUTH_TOKEN','ANTHROPIC_MODEL','HTTPS_PROXY','HTTP_PROXY','NO_PROXY','CLAUDE_CODE_USE_BEDROCK','CLAUDE_CODE_USE_VERTEX'
$baseUrl = $null
foreach ($n in $names) {
  foreach ($scope in 'Process','User','Machine') {
    $v = [Environment]::GetEnvironmentVariable($n, $scope)
    if ($v) {
      $shown = if ($n -match 'KEY|TOKEN') { '<set>' } else { $v }
      Info "$n ($scope env) = $shown"
      if ($n -eq 'ANTHROPIC_BASE_URL' -and -not $baseUrl) { $baseUrl = $v }
    }
  }
}
foreach ($s in @($settings, $settingsLocal)) {
  if ($s -and $s.env) {
    foreach ($p in $s.env.PSObject.Properties) {
      $shown = if ($p.Name -match 'KEY|TOKEN|SECRET') { '<set>' } else { $p.Value }
      Info "$($p.Name) (settings.json env) = $shown"
      if ($p.Name -eq 'ANTHROPIC_BASE_URL') { $baseUrl = $p.Value }
    }
  }
}
if (-not $baseUrl) { Ok 'No ANTHROPIC_BASE_URL - Claude talks to Anthropic directly' }
else {
  Info "Claude requests go to: $baseUrl"
  if ($baseUrl -match 'localhost|127\.0\.0\.1') {
    $port = ([uri]$baseUrl).Port
    $listening = $false
    try { $listening = [bool](Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction Stop) } catch {}
    if (-not $listening) {
      Flag "Nothing is listening on port $port - the local gateway (OmniRoute) is NOT running, so every session waits forever for its first reply"
    } else {
      Ok "Something is listening on port $port"
      $r = Timed "Gateway GET /v1/models" { param($u) (Invoke-WebRequest "$u/v1/models" -UseBasicParsing -TimeoutSec 25).StatusCode } 30 @($baseUrl.TrimEnd('/'))
      Report $r 3000; if ($r.Output) { Info "    -> $($r.Output)" }
      $keyLine = $null
      $omniEnv = Join-Path $HOME '.omniroute\.env'
      if (Test-Path $omniEnv) { $keyLine = (Select-String $omniEnv -Pattern '^OMNIROUTE_API_KEY=' | Select-Object -First 1).Line }
      if ($keyLine) {
        $k = ($keyLine -split '=', 2)[1]
        $r = Timed "Gateway test message (claude-sonnet-5, 8 tokens)" {
          param($u, $k)
          $h = @{ 'x-api-key' = $k; 'anthropic-version' = '2023-06-01'; 'content-type' = 'application/json' }
          $b = '{"model":"claude-sonnet-5","max_tokens":8,"messages":[{"role":"user","content":"ok"}]}'
          try { (Invoke-WebRequest "$u/v1/messages" -Method POST -Headers $h -Body $b -UseBasicParsing -TimeoutSec 55).StatusCode }
          catch { "ERROR: $($_.Exception.Message)" }
        } 60 @($baseUrl.TrimEnd('/'), $k)
        Report $r 10000; if ($r.Output) { Info "    -> $($r.Output)" }
        if ("$($r.Output)" -match 'ERROR') { Flag "Gateway answered with an error: $($r.Output)" }
      } else { Info '    (no OMNIROUTE_API_KEY in ~\.omniroute\.env - skipped the test message)' }
    }
    $log = Join-Path $HOME '.omniroute\autostart.log'
    if (Test-Path $log) { Info "    last OmniRoute autostart: $((Get-Content $log -Tail 1))" }
    $task = Get-ScheduledTask -TaskName 'OmniRoute Gateway (autostart)' -ErrorAction SilentlyContinue
    if ($task) { Info "    autostart task state: $($task.State)" } else { Flag 'OmniRoute autostart task is not registered - the gateway will be down after every reboot' }
  }
}
$r = Timed 'Direct reach of api.anthropic.com' { try { (Invoke-WebRequest 'https://api.anthropic.com' -UseBasicParsing -TimeoutSec 15).StatusCode } catch { if ($_.Exception.Response) { [int]$_.Exception.Response.StatusCode } else { "ERROR: $($_.Exception.Message)" } } } 20
Report $r 4000; if ($r.Output) { Info "    -> $($r.Output) (any number, even 404, means reachable)" }

# ---------------------------------------------------------------------------
Section 'Hooks, status line and plugins (these run at every session start)'
foreach ($pair in @(@('settings.json', $settings), @('settings.local.json', $settingsLocal))) {
  $name = $pair[0]; $s = $pair[1]
  if (-not $s) { continue }
  if ($s.hooks) {
    foreach ($ev in $s.hooks.PSObject.Properties) {
      foreach ($m in @($ev.Value)) { foreach ($h in @($m.hooks)) {
        Info "hook [$name] $($ev.Name): $($h.command)"
        if ($h.command -match 'G:\\|My Drive') { Flag "Hook $($ev.Name) runs a file on Google Drive: $($h.command)" }
        if ($ev.Name -eq 'SessionStart') { Flag "SessionStart hook runs before your first message - if it hangs, the whole session hangs: $($h.command)" }
      } }
    }
  }
  if ($s.statusLine) { Info "statusLine [$name]: $($s.statusLine.command)" }
  if ($s.apiKeyHelper) { Flag "apiKeyHelper is set - it runs before every request: $($s.apiKeyHelper)" }
  if ($s.enabledPlugins) { Info "plugins [$name]: $(($s.enabledPlugins.PSObject.Properties | Where-Object Value | ForEach-Object Name) -join ', ')" }
}
$statusScript = 'C:\ProgramData\rxclaude\caveman-statusline.ps1'
if (Test-Path $statusScript) {
  $r = Timed 'Status line script' { param($p) & powershell -NoProfile -ExecutionPolicy Bypass -File $p } 20 @($statusScript)
  Report $r 3000
}

# ---------------------------------------------------------------------------
Section 'MCP servers Claude starts at launch'
$cj = ReadJson (Join-Path $HOME '.claude.json')
$servers = @()
if ($cj) {
  if ($cj.mcpServers) { foreach ($p in $cj.mcpServers.PSObject.Properties) { $servers += [pscustomobject]@{ Scope = 'global'; Name = $p.Name; Def = $p.Value } } }
  if ($cj.projects) {
    foreach ($proj in $cj.projects.PSObject.Properties) {
      if ($proj.Value.mcpServers) { foreach ($p in $proj.Value.mcpServers.PSObject.Properties) { $servers += [pscustomobject]@{ Scope = $proj.Name; Name = $p.Name; Def = $p.Value } } }
    }
  }
}
if ($servers.Count -eq 0) { Info '(no local MCP servers in ~\.claude.json)' }
foreach ($sv in $servers) {
  $d = $sv.Def
  $what = if ($d.url) { $d.url } else { "$($d.command) $(@($d.args) -join ' ')" }
  Info "[$($sv.Scope)] $($sv.Name): $what"
  if ($what -match 'G:\\|My Drive') { Flag "MCP server '$($sv.Name)' starts from Google Drive" }
  if ($d.command -match '^npx' -and ($what -notmatch '@\d')) { Flag "MCP server '$($sv.Name)' uses npx without a pinned version - it can re-download and stall at startup" }
}

# ---------------------------------------------------------------------------
Section 'Google Drive (where your sessions start and your skills read from)'
$gd = @(Get-Process GoogleDriveFS -ErrorAction SilentlyContinue)
if ($gd.Count -eq 0) { Flag 'Google Drive for desktop (GoogleDriveFS) is NOT running - anything on G:\ will hang or fail' } else { Ok "Google Drive for desktop running ($($gd.Count) processes)" }
$r = Timed "Open $drive" { param($p) Test-Path $p } 20 @($drive); Report $r 2000
if (-not $r.TimedOut -and $r.Output -ne $true) { Flag "$drive does not exist on this machine (Drive not mounted, or a different letter)" }
if (-not $r.TimedOut -and $r.Output -eq $true) {
  $r = Timed 'List _RXClaude top level' { param($p) (Get-ChildItem $p -Force | Measure-Object).Count } 30 @($drive); Report $r 3000
  $r = Timed 'Read rx-pickup skill from Drive' { param($p) (Get-Content "$p\_shared\skills\rx-pickup\SKILL.md" -Raw).Length } 30 @($drive); Report $r 3000
  $r = Timed 'Read YouTube Pipeline LAST_HANDOVER.md' { param($p) (Get-Content "$p\Youtube Pipeline\_sessions\LAST_HANDOVER.md" -Raw).Length } 30 @($drive); Report $r 3000
  if ($r.Output) { Info "    LAST_HANDOVER.md size: $([int]($r.Output / 1KB)) KB$(if ($r.Output -gt 200KB) { '  <-- very large, and rx-pickup reads it in full' })" }
  if (Test-Path "$drive\.git") {
    $r = Timed 'git status in _RXClaude (Claude runs this at startup)' { param($p) Set-Location $p; git status --porcelain | Measure-Object | ForEach-Object Count } 60 @($drive)
    Report $r 5000; if ($r.Output) { Info "    changed/untracked files: $($r.Output)" }
  }
}
foreach ($l in 'C','G') {
  $d = Get-PSDrive $l -ErrorAction SilentlyContinue
  if ($d -and $d.Free -ne $null) {
    $gb = [math]::Round($d.Free / 1GB, 1); Info "Free space on ${l}: $gb GB"
    if ($l -eq 'C' -and $gb -lt 5) { Flag "C: has only $gb GB free - Drive cache and Claude can stall when the disk is full" }
  }
}

# ---------------------------------------------------------------------------
Section 'Latest Claude debug log (if any)'
$dbg = Get-ChildItem (Join-Path $claudeH 'debug') -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($dbg) { Info "$($dbg.FullName)  ($($dbg.LastWriteTime))"; Get-Content $dbg.FullName -Tail 25 | ForEach-Object { Info "    $_" } }
else { Info '(none - see "claude --debug" in the next steps)' }

# ---------------------------------------------------------------------------
if (-not $SkipLiveTest -and $claudeCmd) {
  Section 'Live test: where does a brand-new session hang?'
  Info 'Three one-line Claude runs, 120s limit each. This takes up to 6 minutes.'
  $test = {
    param($c, $dir, $clearBase)
    if ($clearBase) { $env:ANTHROPIC_BASE_URL = $null }
    Set-Location $dir
    & $c -p 'Reply with exactly: ok' 2>&1 | Select-Object -Last 3
  }
  $tmp = Join-Path $env:TEMP 'claude-hang-test'; New-Item -ItemType Directory -Force $tmp | Out-Null
  $runs = @(@('A: from a local temp folder', $tmp, $false))
  if ($baseUrl) { $runs += ,@('B: local folder, gateway bypassed (straight to Anthropic)', $tmp, $true) }
  if (Test-Path $drive) { $runs += ,@('C: from G:\My Drive\_RXClaude (your normal start folder)', $drive, $false) }
  $results = @{}
  foreach ($run in $runs) {
    $before = @(Get-Process claude -ErrorAction SilentlyContinue | ForEach-Object Id)
    $r = Timed $run[0] $test 120 @($claudeCmd, $run[1], $run[2])
    Report $r 30000; if ($r.Output) { Info "    -> $(($r.Output | Out-String).Trim())" }
    $results[$run[0].Substring(0, 1)] = -not $r.TimedOut
    if ($r.TimedOut) {
      Get-Process claude -ErrorAction SilentlyContinue | Where-Object { $before -notcontains $_.Id } | Stop-Process -Force -ErrorAction SilentlyContinue
    }
  }
  Info ''
  if ($results['A'] -eq $false -and $results['B'] -eq $true) { Flag 'VERDICT: hangs through the gateway, works without it -> OmniRoute is the problem' }
  elseif ($results['A'] -eq $true -and $results['C'] -eq $false) { Flag 'VERDICT: works from a local folder, hangs from G:\My Drive\_RXClaude -> the Google Drive folder is the problem' }
  elseif ($results['A'] -eq $false -and ($results['B'] -ne $true)) { Flag 'VERDICT: hangs even from a local folder without the gateway -> a hook, plugin or MCP server is the problem (see sections above; next step: claude --debug)' }
  elseif ($results['A'] -eq $true -and $results['C'] -ne $false) { Ok 'VERDICT: one-shot runs work. The hang is in the interactive start (Remote Control, a SessionStart hook, or the /rx-pickup skill itself) - run "claude --debug" and note the last line before it freezes' }
}

# ---------------------------------------------------------------------------
Section 'SUMMARY - likely culprits'
if ($script:flags.Count -eq 0) { Ok 'Nothing flagged.' } else { $script:flags | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow } }
Write-Host "`nPaste everything above into a Claude session. Do not factory reset - none of these need it." -ForegroundColor Cyan
