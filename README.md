# Folder Synchronization Project

A Python application for synchronizing the contents of a source directory to a backup directory.

1. [Overview](#overview)
2. [Features](#features)
3. [Notes](#notes)
4. [Usage](#usage)
   - [Running the Application](#running-the-application)
   - [Checking Logs](#checking-logs)
   - [Stopping the Application](#stopping-the-application)
5. [Debugging](#debugging)
6. [License](#license)

## Overview

This project is a Python application designed to synchronize the contents of a source directory with a backup directory. It supports one-way synchronization, periodically checks for updates, and logs all operations. It is implemented using standard Python libraries and does not rely on third-party synchronization libraries.

## Features

- **One-Way Synchronization**: Ensures that the backup directory matches the source directory.
- **Periodic Sync**: Automatically syncs at regular intervals.
- **Logging**: Logs all operations to a file and the console.
- **Command Line Arguments**: Configure source and backup paths, synchronization interval, and log file location via command line.

## Notes

- Ensure that the source and backup directories are valid and not subdirectories of each other.
- The log file will be created and updated automatically.

## Usage

### Running the Application

1. **Run the Script**:
   ```bash
   python3 your_script_name.py <source_directory> <backup_directory> [--interval <seconds>] [--log <log_file>]
   ```
Replace `source_directory` and `backup_directory` with your actual directory paths. Optionally, specify synchronization interval and log file path. Please take into account that the backup directory is where the program will store the <source_backup> folder. You cannot place the backup inside the source directory - or any of it's subdirectories - to avoid a recursive loop of nested backups, which can lead to severe system instability including potential hardware crashes or significant performance degradation.

2. **Checking Logs**

   Logs are output to both the console and the specified log file. To view the logs:
   - **Console Output**: The logs will be displayed in the terminal where you ran the script.
   - **Log File**: Check the specified log file (default: `synchro.log`) for a detailed history of operations, including any errors and sync actions.

3. **Stopping the Application**

   To stop the application:
   - Use `Ctrl+C` in the terminal where the script is running. This will gracefully terminate the process and log the total number of operations performed.

4. **Debugging**

   - If you encounter issues, check the logs for detailed error messages.
   - If the log file is deleted during runtime you will need to restart the program to recreate it.

5. **License**

   This project is provided as-is. Feel free to modify and use it according to your needs.
