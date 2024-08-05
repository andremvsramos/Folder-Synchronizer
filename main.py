import os
import argparse
import shutil
import hashlib
import time
import sys
import termios
import signal
from logger import Logger

logger = None
counter = 0

# Handles Ctrl+C input to exit the program
def signal_handler(signum, frame):
	logger.info(f"Total number of operations: {counter}\n\n\n")
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
		logger.error(f"{type.capitalize()} not found: {path}")
		return False
	if not os.path.isdir(path):
		logger.error(f"{type.capitalize()} is not a directory: {path}")
		return False
	logger.info(f"{type.capitalize()} found: \"{os.path.abspath(path)}\"")
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



def sync_directories(source, backup):

	# Get the absolute paths
	source = os.path.abspath(source)
	backup = os.path.join(os.path.abspath(backup), f"{os.path.basename(source)}_backup")

	# Create or update existing files
	for root, dirs, files in os.walk(source):
		# Create the backup folder
		relative_path = os.path.relpath(root, source)
		backup_dir = os.path.join(backup, relative_path)

		if not os.path.exists(backup_dir):
			os.makedirs(backup_dir)
			count_operations()
			logger.info(f"Created backup directory: {backup_dir}")

		for file in files:
			source_file = os.path.join(root, file)
			backup_file = os.path.join(backup_dir, file)
			# If a file is missing or has changed, sync it
			if not os.path.exists(backup_file) or file_checksum(source_file) != file_checksum(backup_file):
				shutil.copy2(source_file, backup_file)
				count_operations()
				logger.info(f"Created backup of {file}")

	# Remove obsolete files and directories
	for root, dirs, files in os.walk(backup, topdown=False):
		relative_path = os.path.relpath(root, backup)
		source_dir = os.path.join(source, relative_path)

		for file in files:
			backup_file = os.path.join(root, file)
			source_file = os.path.join(source_dir, file)

			# If a file is missing from source, remove it
			if not os.path.exists(source_file):
				os.remove(backup_file)
				count_operations()
				logger.info(f"Removed: {backup_file}")

		for dir in dirs:
			backup_subdir = os.path.join(root, dir)
			source_subdir = os.path.join(source_dir, dir)

			# If a directory is missing from source, remove it
			if not os.path.exists(source_subdir):
				shutil.rmtree(backup_subdir)
				count_operations()
				logger.info(f"Removed directory: {backup_subdir}")

# Using the MD5 algorithm, we create a 128-bit hash.
# We use the has as checksum, or 'key', that'll be used to compare the backup to the source file.
# If the hash has changed, then it means we need we need to re-sync it on the next time interval.
def	file_checksum(file):
	file_hash = hashlib.md5()
	with open(file, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			file_hash.update(chunk)
	return file_hash.hexdigest()

def count_operations():
	counter += 1

def main():
	global logger
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
	logger = Logger(args.log).get_logger()

	# Check if paths exist
	source_exists = does_path_exist(source, "source")
	backup_exists = does_path_exist(backup, "backup")

	if not source_exists or not backup_exists:
		logger.error("Folders aren't valid")
		sys.exit(1)

	if is_subdirectory_of_source(source, backup):
		logger.error("The backup folder is inside the source folder or its subdirectories.")
		sys.exit(1)
	else:
		logger.info("Synching...")
		sync_directories(source, backup)

	while True:
		sync_directories(source, backup)
		time.sleep(timer)

if __name__ == "__main__":
	main()
