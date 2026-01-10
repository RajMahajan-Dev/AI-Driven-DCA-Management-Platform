# Data Management Helper Script for Windows
# Run this from the project root directory using PowerShell

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "FedEx DCA Management - Data Manager" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Select an option:" -ForegroundColor Yellow
Write-Host "1) Delete all data"
Write-Host "2) Initialize fresh data"
Write-Host "3) Full reset (delete + initialize)" -ForegroundColor Green
Write-Host "4) Exit"
Write-Host ""

$choice = Read-Host "Enter choice [1-4]"

switch ($choice) {
    "1" {
        Write-Host "`nDeleting all data..." -ForegroundColor Yellow
        docker-compose exec backend python reset_and_init_data.py --delete-all
    }
    "2" {
        Write-Host "`nInitializing fresh data..." -ForegroundColor Yellow
        docker-compose exec backend python reset_and_init_data.py --init
    }
    "3" {
        Write-Host "`nPerforming full reset..." -ForegroundColor Yellow
        docker-compose exec backend python reset_and_init_data.py --reset
    }
    "4" {
        Write-Host "`nExiting..." -ForegroundColor Gray
        exit 0
    }
    default {
        Write-Host "`nInvalid option" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "✅ Operation completed!" -ForegroundColor Green
