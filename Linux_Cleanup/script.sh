#!/bin/bash

# Function to confirm file deletion
confirm_deletion() {
    read -p "Are you sure you want to delete system temporary files? (Y/N): " response
    case "$response" in
        [yY]|[sS])
            return 0 ;;
        *)
            return 1 ;;
    esac
}

# Cache cleanup
sudo apt clean

# Old logs cleanup
sudo journalctl --vacuum-time=7d

# Confirmation for system temporary files deletion
if confirm_deletion; then
    # Cleanup of browser temporary files
    if [ -d ~/.cache/google-chrome/ ]; then
        rm -rf ~/.cache/google-chrome/*
        echo "Google Chrome cache cleaned."
    fi

    if [ -d ~/.mozilla/firefox/*.default/cache/ ]; then
        rm -rf ~/.mozilla/firefox/*.default/cache/*
        echo "Firefox cache cleaned."
    fi
else
    echo "Operation canceled. No temporary files were deleted."
fi

echo "Cleanup completed successfully!"
