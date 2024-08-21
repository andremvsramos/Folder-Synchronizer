# Folder Synchronizer Project

A Python application for synchronizing the contents of a source directory with a backup directory. This repository contains two versions of the project: One-Way synchronization and Two-Way synchronization with an integrated recovery system.

1. [Overview](#overview)
2. [Versions](#versions)
3. [Features](#features)
4. [SHA-256](#sha-256)
   - [File Checksum Calculation](#file-checksum-calculation)
   - [Directory Checksum Calculation](#directory-checksum-calculation)
5. [Usage](#usage)
   - [Running the Script](#running-the-script)
   - [Checking Logs](#checking-logs)
   - [Stopping the Application](#stopping-the-application)
   - [Debugging](#debugging)
   - [Recovery System (Two-Way Version Only)](#recovery-system-two-way-version-only)
     - [Configuration](#configuration)
     - [Using the Recovery System](#using-the-recovery-system)
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

## SHA-256

- **SHA-256 Check**: The system uses SHA-256 hashing to determine if the contents of files have changed. SHA-256 (Secure Hash Algorithm 256-bit) generates a 256-bit hash value that uniquely represents the contents of a file. If the SHA-256 hash of a file changes, it indicates that the file contents have been modified, prompting the synchronization process to update the backup.
  Additionally, to maintain the versioned-backup mode effectively, the system occasionally computes the SHA-256 hash of the entire directory. This ensures that even if changes occur across multiple files, the integrity and versioning of the entire directory are accurately tracked and managed.

- **One-Way Synchronization**: By itself, the One-Way synchronization is a straightforward process that syncs files from the source directory to the backup directory. It does not track historical versions of files.

- **Running One-Way Program in Versioned Backup Mode**: The One-Way synchronization program can be run with versioned backup mode activated. This mode will create version directories and maintain different versions of the source and backup directories, as described in the Two-Way version.

- **One-Way with Versioned Backup Mode**: When activated, the One-Way version will create a `__versions__` directory. For each synchronized directory (source and backup), it maintains two versions: `_0` (previous) and `_1` (latest). When synchronizing, if the incoming file's SHA-256 hash differs from `_1`, the current `_1` is copied to `_0`, and the incoming sync becomes the new `_1`. The program also calculates the SHA-256 hash of the entire directory by considering the checksums of all files and their relative paths. This combined approach ensures that both individual file changes and the overall directory state are accurately tracked and versioned.

### File Checksum Calculation

To calculate the SHA-256 hash of a file, the following function is used:

```python
import hashlib

def file_checksum(file):
    file_hash = hashlib.sha256()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            file_hash.update(chunk)
    return file_hash.hexdigest()
```
- **Explanation**: The `file_checksum` function calculates the SHA-256 hash of a file by reading it in chunks and updating the hash with each chunk. The resulting hash uniquely represents the file contents and is used to determine if the file has changed.

### Directory Checksum Calculation

To calculate the SHA-256 hash of an entire directory, the following function is used:

```python
import os
import hashlib

def directory_checksum(directory):
    hasher = hashlib.sha256()
    for root, _, files in os.walk(directory):
        for file in sorted(files):
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)
            hasher.update(relative_path.encode())
            hasher.update(file_checksum(file_path).encode())
    return hasher.hexdigest()
```
- **Explanation**: The `directory_checksum` function computes the SHA-256 hash for the entire directory by hashing the relative file paths and their contents. This approach ensures that changes to both file contents and the directory structure are detected.

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

#### Configuration

The recovery system uses a `config.json` file to configure certain settings, such as the script path and synchronization interval.

- **If no `config.json` file is provided**, the program will automatically generate one with default settings. These defaults include a script path pointing to the One-Way program (`../OneWay/main.py`) and a synchronization interval of 60 seconds.

- **If you wish to customize the recovery behavior**, you can create and provide your own `config.json` file. You can specify a different script path and synchronization interval according to your needs. **You'll only need to change the `script` if you move the OneWay directory to a different location.**

Here’s an example of what the `config.json` might look like:

```json
{
    "script": "../OneWay/main.py",
    "interval": ["--interval", "60"]
}
```
- `script`: Path to the script that manages the versioning. It needs to point to the `OneWay/main.py` script. Only change this if you move the `OneWay` directory.
- `interval`: Synchronization interval in seconds. For demonstration purposes, the default configuration sets this to 60 seconds.

#### Using the Recovery System

To use the recovery system from the CLI:

- **To restore the latest version of a directory**:
  ```bash
  python3 main.py <directory_to_recover> --restore [--version latest]
  ```

- **To restore a previous version of a directory:**
  ```bash
  python3 main.py <directory_to_recover> --restore --version previous
  ```

Replace `directory_to_recover` with the path to the directory you want to restore. By default, the system restores the **latest** version of the directory. The `--version previous` flag refers to the version immediately before the latest one.

## License

This project is provided as-is. Feel free to modify and use it according to your needs.
