# Folder Synchronizer Project

A Python application for synchronizing the contents of a source directory with a backup directory. This repository contains two versions of the project: One-Way synchronization and Two-Way synchronization with an integrated recovery system.

1. [Overview](#overview)
2. [Versions](#versions)
3. [Features](#features)
4. [Notes](#notes)
5. [Usage](#usage)
   - [Running the Script](#running-the-script)
   - [Checking Logs](#checking-logs)
   - [Stopping the Application](#stopping-the-application)
   - [Debugging](#debugging)
   - [Recovery System (Two-Way Version Only)](#recovery-system-two-way-version-only)
6. [License](#license)

## Overview

This project is a Python application designed to synchronize the contents of a source directory with a backup directory. It supports both one-way and two-way synchronization, periodically checks for updates, and logs all operations. The two-way version includes a recovery system that maintains historical versions of directories using One-Way synchronization logic.

## Versions

- **One-Way Version**: Synchronizes files from the source directory to the backup directory only.
- **Two-Way Version**: Synchronizes files between the source and backup directories in both directions. This version also includes a recovery system that leverages One-Way synchronization to maintain the latest and previous versions of the directories.

Each version can be run independently from its respective folder:

- **One-Way Version**: Run from the `OneWay` directory.
- **Two-Way Version**: Run from the `TwoWay` directory.

## Features

- **One-Way Synchronization (One-Way Version)**: Ensures that the backup directory matches the source directory.
- **Two-Way Synchronization (Two-Way Version)**: Ensures that both the source directory and the backup directory are kept in sync, based on the latest modifications.
- **Periodic Sync**: Automatically syncs at regular intervals.
- **Logging**: Logs all operations to a file and the console.
- **Command Line Arguments**: Configure source and backup paths, synchronization interval, and log file location via command line.
- **Recovery System (Two-Way Version)**: The recovery system utilizes One-Way synchronization to maintain and restore historical versions of directories. It supports:
  - **Version Tracking**: Maintains the latest and previous versions of the source and backup directories.
  - **Restoration**: Allows restoration of directories to previous states.

## Notes

- Ensure that the source and backup directories are valid and not subdirectories of each other.
- The log file will be created and updated automatically.
- **One-Way Version**: Synchronization is one-directional from the source to the backup directory.
- **Two-Way Version**: Synchronization is bi-directional, keeping both the source and backup directories in sync. Additionally, the recovery system provides version tracking and restoration capabilities.

## Usage

### Running the Script

For either version, navigate to the respective folder (`OneWay` or `TwoWay`) and run:

```bash
python3 main.py <source_directory> <backup_directory> [--interval <seconds>] [--log <log_file>]
```

Replace source_directory and backup_directory with your actual directory paths. Optionally, specify synchronization interval and log file path. Please note that the backup directory cannot be a subdirectory of the source directory or any of its subdirectories to avoid recursive loops, which could lead to severe system instability.

### Checking Logs

Logs are output to both the console and the specified log file. To view the logs:

- **Console Output**: The logs will be displayed in the terminal where you ran the script.
- **Log File**: Check the specified log file (default: `oneway.log` and `twoway.log`) for a detailed history of operations, including any errors and sync actions.

### Stopping the Application

To stop the application:
- Use `Ctrl+C` in the terminal where the script is running. This will gracefully terminate the process and log the total number of operations performed.

### Debugging

- If you encounter issues, check the logs for detailed error messages.
- If the log file is deleted during runtime, you will need to restart the program to recreate it.

### Recovery System - Two Way Version Only

The recovery system is now supported in the Two-Way version. It maintains the latest and previous versions of the folders being synchronized. The recovery system does not use JSON hashing but relies on the One-Way version to handle versioning.

When restoring:
- The system will recover the latest or previous versions of the folders.
- The JSON file `.info.json` records folder locations for recovery.
- If the target directory is deleted, the system checks if the path exists in the JSON and restores it from the appropriate backup version.

To use the recovery system from the CLI:

- **To restore the latest version of a directory**:
  ```bash
  python3 main.py <source_directory> <backup_directory> --restore --version latest
  ```

- **To restore a previous version of a directory**:
  ```bash
  python3 main.py <directory_to_recover> --restore [--interval [<latest>/<previous>]]
  ```

## License

This project is provided as-is. Feel free to modify and use it according to your needs.
