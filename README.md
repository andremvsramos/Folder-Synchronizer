# Folder Synchronizer Project

A Python application for synchronizing the contents of a source directory with a backup directory. This repository contains two versions of the project: One-Way synchronization and Two-Way synchronization with a planned recovery system.

1. [Overview](#overview)
2. [Versions](#versions)
3. [Features](#features)
4. [Notes](#notes)
5. [Usage](#usage)
   - [Running the Script](#running-the-script)
   - [Checking Logs](#checking-logs)
   - [Stopping the Application](#stopping-the-application)
   - [Debugging](#debugging)
   - [Recovery System (WIP) - Two Way Version Only](#recovery-system-wip---two-way-version-only)
6. [License](#license)

## Overview

This project is a Python application designed to synchronize the contents of a source directory with a backup directory. It supports both one-way and two-way synchronization, periodically checks for updates, and logs all operations. The two-way version also includes a planned recovery system that will record a history of changes.

## Versions

- **One-Way Version**: Synchronizes files from the source directory to the backup directory only.
- **Two-Way Version**: Synchronizes files between the source and backup directories in both directions. This version also includes a planned recovery system (WIP).

Each version can be run independently from its respective folder:

- **One-Way Version**: Run from the `OneWay` directory.
- **Two-Way Version**: Run from the `TwoWay` directory.

## Features

- **One-Way Synchronization (One-Way Version)**: Ensures that the backup directory matches the source directory.
- **Two-Way Synchronization (Two-Way Version)**: Ensures that both the source directory and the backup directory are kept in sync, based on the latest one that was modified.
- **Periodic Sync**: Automatically syncs at regular intervals.
- **Logging**: Logs all operations to a file and the console.
- **Command Line Arguments**: Configure source and backup paths, synchronization interval, and log file location via command line.
- **Planned Recovery System (Two-Way Version)**: The recovery system will record a history of changes, including file hashes and modifications, using JSON dumps.

## Notes

- Ensure that the source and backup directories are valid and not subdirectories of each other.
- The log file will be created and updated automatically.
- **One-Way Version**: Synchronization is one-directional from the source to the backup directory.
- **Two-Way Version**: Synchronization is bi-directional, keeping both the source and backup directories in sync.

## Usage

### Running the Script

For either version, navigate to the respective folder (`OneWay` or `TwoWay`) and run:

```bash
python3 main.py <source_directory> <backup_directory> [--interval <seconds>] [--log <log_file>]
```

Replace `source_directory` and `backup_directory` with your actual directory paths. Optionally, specify synchronization interval and log file path. Please note that the backup directory cannot be a subdirectory of the source directory or any of its subdirectories to avoid recursive loops, which would lead to severe system instability including potential hardware crashes or significant performance degradation.

### Checking Logs

Logs are output to both the console and the specified log file. To view the logs:
- **Console Output**: The logs will be displayed in the terminal where you ran the script.
- **Log File**: Check the specified log file (default: `synchro.log`) for a detailed history of operations, including any errors and sync actions.

### Stopping the Application

To stop the application:
- Use `Ctrl+C` in the terminal where the script is running. This will gracefully terminate the process and log the total number of operations performed.

### Debugging

- If you encounter issues, check the logs for detailed error messages.
- If the log file is deleted during runtime, you will need to restart the program to recreate it.

### Recovery System (WIP) - Two Way Version Only

The recovery system is in progress and will be implemented in a future update. The planned recovery system will use JSON dumps to record a history of changes, including file hashes, timestamps, and types of operations performed. This will allow for effective tracking and restoration of previous states in case of data loss or corruption.

## License

This project is provided as-is. Feel free to modify and use it according to your needs.
