param([string]$CheckoutPath)
$ErrorActionPreference = 'Stop'
$sourceRoot = Split-Path $PSScriptRoot -Parent
$remote = 'https://github.com/CWO4PapaBear/More-Minions.git'
$gitCommand = Get-Command git -ErrorAction SilentlyContinue
if ($gitCommand) { $gitExe = $gitCommand.Source }
else { $gitExe = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe' }
if (-not (Test-Path -LiteralPath $gitExe)) { throw 'Git was not found. Install Git for Windows and reopen PowerShell.' }
if (-not $CheckoutPath) { $CheckoutPath = Join-Path (Split-Path $sourceRoot -Parent) 'More-Minions-publish' }
$CheckoutPath = [IO.Path]::GetFullPath($CheckoutPath)
if ($CheckoutPath -eq [IO.Path]::GetFullPath($sourceRoot)) { throw 'Use a separate publishing checkout to preserve the existing GitHub history.' }

# Clone the existing repository; never force-push or replace its history.
if (-not (Test-Path -LiteralPath $CheckoutPath)) {
    & $gitExe --no-pager clone $remote $CheckoutPath
    if ($LASTEXITCODE -ne 0) { throw 'Clone failed. Complete GitHub authentication, then rerun this script.' }
} else {
    $actualRemote = & $gitExe --no-pager -C $CheckoutPath remote get-url origin
    if ($LASTEXITCODE -ne 0 -or $actualRemote -ne $remote) { throw 'Existing publishing directory is not the expected repository.' }
    $dirty = & $gitExe --no-pager -C $CheckoutPath status --porcelain
    if ($LASTEXITCODE -ne 0) { throw 'Could not inspect publishing checkout.' }
    if ($dirty) {
        # Resume a failed copy/stage only when every changed file still matches our records.
        foreach ($line in $dirty) {
            $relative = $line.Substring(3)
            $sourceFile = Join-Path $sourceRoot $relative
            $targetFile = Join-Path $CheckoutPath $relative
            if (-not (Test-Path -LiteralPath $sourceFile -PathType Leaf) -or -not (Test-Path -LiteralPath $targetFile -PathType Leaf)) { throw "Unexpected pending file: $relative" }
            $expected = [IO.File]::ReadAllText($sourceFile).Replace("`r`n","`n")
            $actual = [IO.File]::ReadAllText($targetFile).Replace("`r`n","`n")
            if ($actual -cne $expected) { throw "Pending file differs from prepared records: $relative" }
        }
    }
    & $gitExe --no-pager -C $CheckoutPath fetch origin
    if ($LASTEXITCODE -ne 0) { throw 'Could not fetch the publishing repository.' }
    $currentBranch = & $gitExe --no-pager -C $CheckoutPath symbolic-ref --short HEAD
    if ($LASTEXITCODE -ne 0) { throw 'Publishing checkout must be on a branch.' }
    & $gitExe --no-pager -C $CheckoutPath show-ref --verify --quiet "refs/remotes/origin/$currentBranch"
    if ($LASTEXITCODE -eq 0) {
        & $gitExe --no-pager -C $CheckoutPath merge --ff-only "origin/$currentBranch"
        if ($LASTEXITCODE -ne 0) { throw 'Could not fast-forward. Existing changes were preserved.' }
    } elseif ($LASTEXITCODE -ne 1) { throw 'Could not inspect remote branch.' }
}
$branch = & $gitExe --no-pager -C $CheckoutPath symbolic-ref --short HEAD
if ($LASTEXITCODE -ne 0) { throw 'Publishing checkout must be on a branch.' }
foreach ($key in @('user.name','user.email')) {
    $identity = & $gitExe --no-pager -C $sourceRoot config --get $key
    if ($LASTEXITCODE -ne 0 -or -not $identity) { throw "Configure $key in the local records repository before publishing." }
    & $gitExe --no-pager -C $CheckoutPath config --local $key $identity
    if ($LASTEXITCODE -ne 0) { throw "Could not set local $key in publishing checkout." }
}
$files = @(& $gitExe --no-pager -C $sourceRoot ls-files)
if ($LASTEXITCODE -ne 0 -or -not $files.Count) { throw 'The local records repository has no tracked files.' }
foreach ($relative in $files) {
    $target = [IO.Path]::GetFullPath((Join-Path $CheckoutPath $relative))
    if (-not $target.StartsWith($CheckoutPath.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'File escaped publishing checkout.' }
    [IO.Directory]::CreateDirectory((Split-Path $target -Parent)) | Out-Null
    Copy-Item -LiteralPath (Join-Path $sourceRoot $relative) -Destination $target -Force
    & $gitExe --no-pager -C $CheckoutPath add -- $relative
    if ($LASTEXITCODE -ne 0) { throw "Could not stage $relative" }
}
& $gitExe --no-pager -C $CheckoutPath diff --cached --check
if ($LASTEXITCODE -ne 0) { throw 'Staged whitespace validation failed.' }
& $gitExe --no-pager -C $CheckoutPath diff --cached --quiet
if ($LASTEXITCODE -eq 1) {
    & $gitExe --no-pager -C $CheckoutPath commit -m 'Document More Minions companion interface work and server roadmap'
    if ($LASTEXITCODE -ne 0) { throw 'Commit failed. Review the publishing checkout.' }
} elseif ($LASTEXITCODE -ne 0) { throw 'Could not inspect staged changes.' }
& $gitExe --no-pager -C $CheckoutPath push origin $branch
if ($LASTEXITCODE -ne 0) { throw 'Push failed. Changes remain committed in the publishing checkout; authenticate and rerun.' }
Write-Output "Published records to $remote on $branch. Working checkout: $CheckoutPath"
