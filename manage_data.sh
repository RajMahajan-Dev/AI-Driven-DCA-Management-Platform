#!/bin/bash
# Data Management Helper Script
# Run this from the project root directory

echo "======================================"
echo "FedEx DCA Management - Data Manager"
echo "======================================"
echo ""
echo "Select an option:"
echo "1) Delete all data"
echo "2) Initialize fresh data"
echo "3) Full reset (delete + initialize)"
echo "4) Exit"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo "Deleting all data..."
        docker-compose exec backend python reset_and_init_data.py --delete-all
        ;;
    2)
        echo "Initializing fresh data..."
        docker-compose exec backend python reset_and_init_data.py --init
        ;;
    3)
        echo "Performing full reset..."
        docker-compose exec backend python reset_and_init_data.py --reset
        ;;
    4)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid option"
        exit 1
        ;;
esac

echo ""
echo "✅ Operation completed!"
