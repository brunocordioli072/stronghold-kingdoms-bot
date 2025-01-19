# Get the current directory and scripts directory
$currentDir = (Get-Item (Get-Location)).FullName
$scriptsDir = Join-Path $currentDir "scripts"

# Start python main.py as a job 
$job = Start-Job -ScriptBlock { 
    param($workDir)
    Set-Location -Path $workDir
    Write-Host "Current directory is now: $(Get-Location)"
    python main.py
} -ArgumentList $currentDir

# Store job ID in scripts directory
$job.Id | Out-File (Join-Path $scriptsDir "job_id.txt")

Write-Host "Started python job with ID: $($job.Id)"
Write-Host "To see logs use: Receive-Job -Id $($job.Id) -Keep"