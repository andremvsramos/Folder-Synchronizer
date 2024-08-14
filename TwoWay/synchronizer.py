import os
import shutil
import hashlib
import time

ORIGIN = {
	1: "SOURCE",
	2: "BACKUP"
}

class FolderSynchronizer:

	def __init__(self, logger, source, backup, timer):
		self.logger = logger
		self.log = self.logger.get_logger()
		self.source = source
		self.backup = backup
		self.timer = timer
		self.counter = 0

	def get_logger(self):
		return self.logger

	def get_json_logger(self):
		return self.log

	def get_source(self):
		return self.source

	def get_backup(self):
		return self.backup

	def get_timer(self):
		return self.timer

	def get_counter(self):
		return self.counter

	def sync_by_source(self):
		file = self.source
		self.sync_directories(file, self.backup, origin=ORIGIN[1])

	def sync_by_backup(self):
		file = self.source+"_backup"
		self.sync_directories(file, self.source, origin=ORIGIN[2])

	def get_lastest_mtime(self, directory):
		return os.path.getmtime(directory)

	# Using the MD5 algorithm, we create a 128-bit hash.
	# We use the has as checksum, or 'key', that'll be used to compare the backup to the source file.
	# If the hash has changed, then it means we need we need to re-sync it on the next time interval.
	def file_checksum(self, file):
		file_hash = hashlib.md5()
		with open(file, "rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				file_hash.update(chunk)
		return file_hash.hexdigest()

	def count_operations(self):
		self.counter += 1

	def sync_directories(self, source, backup, origin):

		# Get the absolute paths
		source = os.path.abspath(source)

		# Only change backup to include "_backup" if we're synching from the source folder
		if origin == ORIGIN[1]:
			backup = os.path.join(os.path.abspath(backup), f"{os.path.basename(source)}_backup")
		else:
			backup = os.path.abspath(backup)

		# Create or update existing files
		for root, dirs, files in os.walk(source):
			# Create the backup folder
			relative_path = os.path.relpath(root, source)
			backup_dir = os.path.join(backup, relative_path)

			# Only create the _backup folder if it doesn't exist and we're synching from the source folder
			if not os.path.exists(backup_dir) and not origin == ORIGIN[2]:
				os.makedirs(backup_dir)
				self.count_operations()
				#self.logger.log_metadata(file_path=backup_dir, change_type="CREATE")
				self.log.info(f"Created backup directory: {os.path.basename(backup_dir)}")

			for file in files:
				source_file = os.path.join(root, file)
				backup_file = os.path.join(backup_dir, file)
				# If a file is missing or has changed, sync it
				if not os.path.exists(backup_file) or self.file_checksum(source_file) != self.file_checksum(backup_file):
					shutil.copy2(source_file, backup_file)
					self.count_operations()
					self.logger.log_metadata(file_path=source_file, change_type="UPDATE", root=source)
					self.log.info(f"Created backup of {os.path.basename(source_file)}")

		# Remove obsolete files and directories
		for root, dirs, files in os.walk(backup, topdown=False):
			relative_path = os.path.relpath(root, backup)
			source_dir = os.path.join(source, relative_path)

			for file in files:
				backup_file = os.path.join(root, file)
				source_file = os.path.join(source_dir, file)

				# If a file is missing from source, remove it
				if not os.path.exists(source_file):
					self.logger.log_metadata(file_path=backup_file, change_type="DELETE", root=source)
					os.remove(backup_file)
					self.count_operations()
					self.log.info(f"Removed: {os.path.relpath(backup_file, root)}")

			for dir in dirs:
				backup_subdir = os.path.join(root, dir)
				source_subdir = os.path.join(source_dir, dir)

				# If a directory is missing from source, remove it
				if not os.path.exists(source_subdir):
					self.logger.log_metadata(file_path=backup_subdir, change_type="UPDATE", root=source)
					shutil.rmtree(backup_subdir)
					self.count_operations()
					self.log.info(f"Removed directory: {os.path.relpath(backup_subdir, root)}")

	def run(self):
		while True:

			# Check if we're synching from source or backup, depending on the directories last modification time
			# Instead of checking each individual file and dir, we check the root.
			# This allows to identify mtime for file deletions and remove files/dirs of the correct directory
			source_mtime = self.get_lastest_mtime(self.source)
			backup = self.source+"_backup"
			backup_mtime = self.get_lastest_mtime(backup)
			if source_mtime > backup_mtime:
				self.sync_by_source()
			else:
				self.sync_by_backup()
			time.sleep(self.timer)
