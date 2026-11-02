<#
.SYNOPSIS
  Static checks for TLRA: Lua syntax (luac -p), luacheck, XML well-formedness.
.DESCRIPTION
  Findings are normalised to one line each and diffed against tools/baseline.txt.
  Exit 0 = no findings beyond the baseline; exit 1 = new problems; exit 2 = tooling error.
  luacheck is located via $env:LUACHECK, PATH, or tools/.bin/luacheck.exe. If absent it is skipped with a warning.
  luac is located via $env:LUAC or PATH (Lua 5.1 / LuaJIT-compatible syntax).
.PARAMETER UpdateBaseline
  Rewrite tools/baseline.txt with the current findings.
#>
param([switch]$UpdateBaseline)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$baselineFile = Join-Path $PSScriptRoot 'baseline.txt'
$skip = '^(\.git|\.claude|tools)/'

function Find-Tool($envName, $names, $extra) {
    $e = [Environment]::GetEnvironmentVariable($envName)
    if ($e -and (Test-Path $e)) { return $e }
    foreach ($n in $names) { $c = Get-Command $n -ErrorAction SilentlyContinue; if ($c) { return $c.Source } }
    foreach ($p in $extra) { if (Test-Path $p) { return $p } }
    return $null
}
function Rel($p) { ($p.Substring($root.Length + 1)) -replace '\\', '/' }

$findings = New-Object System.Collections.Generic.List[string]
$scripts = Get-ChildItem -Recurse -File -Filter *.script | Where-Object { (Rel $_.FullName) -notmatch $skip }
$xmls = Get-ChildItem -Recurse -File -Include *.xml | Where-Object { (Rel $_.FullName) -notmatch $skip }

# 1. Lua syntax
$luac = Find-Tool 'LUAC' @('luac', 'luac5.1') @()
if (-not $luac) { Write-Error 'luac not found (set $env:LUAC or add to PATH)'; exit 2 }
foreach ($s in $scripts) {
    $out = & $luac -p (Rel $s.FullName) 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) {
        foreach ($l in ($out -split "`r?`n" | Where-Object { $_.Trim() })) {
            # "luac: path:LINE: msg" -> strip line numbers so baseline survives unrelated edits
            $m = $l -replace '^.*?luac[^:]*:\s*', '' -replace ':\d+:', ':'
            $findings.Add("SYNTAX $m")
        }
    }
}

# 2. luacheck
$lcheck = Find-Tool 'LUACHECK' @('luacheck') @((Join-Path $PSScriptRoot '.bin\luacheck.exe'))
if ($lcheck) {
    $out = & $lcheck --no-color --codes --formatter plain --config .luacheckrc -- @($scripts | ForEach-Object { Rel $_.FullName }) 2>&1
    foreach ($l in $out) {
        if ($l -match '^(.+?):(\d+):(\d+): (.*)$') {
            $findings.Add("LUACHECK $($Matches[1]):$($Matches[4])")
        }
    }
} else { Write-Warning 'luacheck not found; skipping lint (set `$env:LUACHECK or place luacheck.exe in tools/.bin)' }

# 3. XML well-formedness
foreach ($x in $xmls) {
    try { $d = New-Object System.Xml.XmlDocument; $d.XmlResolver = $null; $d.Load($x.FullName) }
    catch { $findings.Add("XML $(Rel $x.FullName): $($_.Exception.InnerException.Message -replace '\s+', ' ')") }
}

$current = @($findings | Sort-Object -Unique)
Write-Host ("Checked {0} scripts, {1} XML files; {2} finding(s)." -f $scripts.Count, $xmls.Count, $current.Count)
if ($UpdateBaseline) { Set-Content $baselineFile $current -Encoding utf8; Write-Host "Baseline updated: $baselineFile"; exit 0 }
$base = if (Test-Path $baselineFile) { @(Get-Content $baselineFile | Where-Object { $_.Trim() }) } else { @() }
$new = @($current | Where-Object { $_ -notin $base })
$fixed = @($base | Where-Object { $_ -notin $current })
if ($fixed) { Write-Host "Resolved since baseline ($($fixed.Count)); consider -UpdateBaseline." }
if ($new) { Write-Host "NEW problems:"; $new | ForEach-Object { Write-Host "  $_" }; exit 1 }
Write-Host 'OK: nothing new beyond baseline.'; exit 0
