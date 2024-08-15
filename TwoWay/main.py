import os
import argparse
import sys
import signal
import time
import subprocess
from logger import Logger
from synchronizer import FolderSynchronizer
from recovery import RestoreSystem

logger = None
sync = None
restore_manager = None

# Handles Ctrl+C input to exit the program
def signal_handler(signum, param):
	logger.get_logger().info(f"Total number of operations: {sync.counter}\n\n\n")
	if restore_manager:
		restore_manager.cleanup()
	sys.exit(0)

# Simply clears the terminal on startup -- checks the if the system is UNIX-based or Windows
def clear_terminal():
	if os.name == "nt":
		os.system('cls')
	else:
		os.system('clear')

# Checks if the provided folders are valid and logs the response
def does_path_exist(path, type):
	if not os.path.exists(path):
		logger.get_logger().error(f"{type.capitalize()} not found: {os.path.basename(path)}")
		return False
	if not os.path.isdir(path):
		logger.get_logger().error(f"{type.capitalize()} is not a directory: {os.path.basename(path)}")
		return False
	logger.get_logger().info(f"{type.capitalize()} found: \"{os.path.basename(path)}\"")
	return True

# Verifies that the backup will not be located inside the source directory.
# If it were, the backup process would inadvertently include the backup itself in the backup.
# This creates a recursive loop of nested backups, which can lead to severe system instability
# including potential hardware crashes or significant performance degradation.
def is_subdirectory_of_source(source, backup):
	source = os.path.abspath(source)
	backup = os.path.abspath(backup)

	common_path = os.path.commonpath([source, backup])
	return common_path == source

def main():
	global logger
	global sync
	global restore_manager
	signal.signal(signal.SIGINT, signal_handler)

	# Read from CLI
	parser = argparse.ArgumentParser()
	parser.add_argument('source', type=str, help='Path to the source directory that will be backed up and synchronized')
	parser.add_argument('backup', type=str, nargs='?', help='Path to the destination directory where the backup will be stored')
	parser.add_argument('--restore', action="store_true", help="Restore the selected directory to it's previous state")
	parser.add_argument('--version', type=str, choices=['latest', 'previous'], default='none', help="Specify which version to restore (latest or previous)")
	parser.add_argument('--interval', type=int, default=3600, help='Synchronization interval in seconds (default: 3600)')
	parser.add_argument('--log', type=str, default="twoway.log", help='Path to the log file (default: synchro.log)')
	parser.add_argument('--config', type=str, default="config.json", help="Path to the recovery system configuration file")
	args = parser.parse_args()

	clear_terminal()

	source = args.source
	backup = args.backup
	timer = args.interval
	logger = Logger(args.log)
	config = args.config
	restore_manager = RestoreSystem(source, logger, config=config)
	version = args.version

	if args.restore:
		if args.backup:
			logger.get_logger().error("The --restore option requires only one directory argument.")
			sys.exit(1)

		# If user didn't define version in recovery mode
		# We don't set the arg latest by default to not allow the user to use version option on non-recovery mode
		if version == 'none':
			version = 'latest'

		path_to_restore = os.path.abspath(args.source)
		recorded_path = restore_manager.get_recorded_path(path_to_restore)

		if recorded_path:
			if not os.path.exists(recorded_path):
				os.makedirs(recorded_path)
			restore_manager.restore_version(recorded_path, version=version)
			logger.get_logger().info(f"Restored from backup to {recorded_path}")

	elif not args.backup:
		logger.get_logger().error("The program requires a backup directory.")
		sys.exit(1)

	# If user used version option in non-recovery mode
	elif args.version != 'none':
		logger.get_logger().error("Version option not supported for normal use")
		sys.exit(1)

	else:
		# Check if paths exist
		source_exists = does_path_exist(source, "source")
		backup_exists = does_path_exist(backup, "backup")

		if not source_exists or not backup_exists:
			logger.get_logger().error("Folders aren't valid")
			sys.exit(1)

		sync = FolderSynchronizer(logger, source, backup, timer)


		if is_subdirectory_of_source(source, backup):
			logger.get_logger().error("The backup folder is inside the source folder or its subdirectories.")
			sys.exit(1)
		else:
			# Create the backup first
			logger.get_logger().info("Synching...")
			sync.sync_by_source()

		restore_manager.run_versioned_backups()
		sync.run()

if __name__ == "__main__":
	main()
