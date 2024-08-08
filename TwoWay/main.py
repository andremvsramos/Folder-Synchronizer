import os
import argparse
import sys
import signal
import time
from logger import Logger
from synchronizer import FolderSynchronizer

logger = None
sync = None

# Handles Ctrl+C input to exit the program
def signal_handler(signum, param):
	logger.get_logger().info(f"Total number of operations: {sync.counter}\n\n\n")
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
	signal.signal(signal.SIGINT, signal_handler)

	# Read from CLI
	parser = argparse.ArgumentParser()
	parser.add_argument('source', type=str, help='Path to the source directory that will be backed up and synchronized')
	parser.add_argument('backup', type=str, help='Path to the destination directory where the backup will be stored')
	parser.add_argument('--interval', type=int, default=3600, help='Synchronization interval in seconds (default: 3600)')
	parser.add_argument('--log', type=str, default="synchro.log", help='Path to the log file (default: synchro.log)')
	args = parser.parse_args()

	clear_terminal()

	source = args.source
	backup = args.backup
	timer = args.interval
	logger = Logger(args.log)

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

	sync.run()

if __name__ == "__main__":
	main()
