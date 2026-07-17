$ErrorActionPreference = "Stop"
$RepoUrl = if ($env:REPO_URL) { $env:REPO_URL } else { "https://github.com/learning-kai/claude-obsidian-hermes.git" }
$Target = if ($env:TARGET) { $env:TARGET } else { Join-Path $HOME "claude-obsidian-hermes" }
$Vault = if ($env:CLAUDE_OBSIDIAN_VAULT) { $env:CLAUDE_OBSIDIAN_VAULT } else { Join-Path $HOME "claude-obsidian-vault" }
if (-not (Test-Path (Join-Path $Target ".git"))) { git clone $RepoUrl $Target } else { try { git -C $Target pull --ff-only } catch {} }
if (-not (Test-Path (Join-Path $Vault "wiki"))) { Copy-Item -Recurse -Force (Join-Path $Target "vault-template") $Vault }
$skills = Join-Path $HOME ".hermes/skills/note-taking"
New-Item -ItemType Directory -Force -Path $skills | Out-Null
Get-ChildItem (Join-Path $Target "adapted/skills") -Directory | ForEach-Object {
  $dest = Join-Path $skills ("claude-obsidian-" + $_.Name)
  if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
  Copy-Item -Recurse -Force $_.FullName $dest
}
Write-Host "Installed repo: $Target"
Write-Host "Vault: $Vault"
