# Run as administrator
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Please run this script as Administrator!"
    Break
}

# Install Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install required dependencies using Chocolatey
$packages = @(
    "adb",
    "tesseract",
    "make",
    "pyenv-win"
)

foreach ($package in $packages) {
    Write-Host "Installing $package..."
    choco install $package -y
}

# Refresh environment variables
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Initialize pyenv and install Python
Write-Host "Installing Python 3.11.0b3 using pyenv..."
pyenv update
pyenv install 3.11.0b3
pyenv global 3.11.0b3

# Clone the repository
Write-Host "Cloning the repository..."
git clone https://github.com/brunocordioli072/stronghold-kingdoms-bot

# Navigate to the project directory
Set-Location stronghold-kingdoms-bot

# Install Python dependencies
Write-Host "Installing Python dependencies..."
pip install -r requirements.txt

Write-Host "`nInstallation complete! Please ensure you have:"
Write-Host "1. Enabled Android Debug Bridge in your emulator (Bluestacks recommended)"
Write-Host "2. Set Stronghold Kingdoms User Interface Size to minimum"
Write-Host "`nTo run the bot, use 'make run' in the project directory with Stronghold Kingdoms open in your emulator."