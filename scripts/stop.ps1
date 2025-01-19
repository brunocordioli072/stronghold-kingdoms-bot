# Get scripts directory path
$currentDir = (Get-Item (Get-Location)).FullName
$scriptsDir = Join-Path $currentDir "scripts"

# Read job ID from scripts directory
$jobId = Get-Content (Join-Path $scriptsDir "job_id.txt")
Write-Host "Stopping job ID: $jobId"

# Save final logs before stopping
Receive-Job -Id $jobId > (Join-Path $scriptsDir "final_log.txt")

# Stop and remove the job
Stop-Job -Id $jobId
Remove-Job -Id $jobId

# Clean up the ID file
Remove-Item (Join-Path $scriptsDir "job_id.txt")

Write-Host "Job stopped and logs saved to final_log.txt"