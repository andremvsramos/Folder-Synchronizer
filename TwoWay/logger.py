import logging
import json
import os
from datetime import datetime
from synchronizer import FolderSynchronizer
from threading import Lock

class Logger:

	def __init__(self, log_file):
		self.log_file = log_file
		self.logger = logging.getLogger(__name__)
		if self.logger.hasHandlers():
			for handler in self.logger.handlers:
				self.logger.removeHandler(handler)
		self.file_handler = None
		self.console_handler = None
		self.format = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s] - %(message)s')
		self.metadata_lock = Lock()
		self.setup()

	def setup(self):

		# Set log level
		self.logger.setLevel(logging.DEBUG)

		# Create a handler for the logger file
		self.file_handler = logging.FileHandler(self.log_file)
		self.file_handler.setLevel(logging.DEBUG)

		# Create a handler for console logs
		self.console_handler = logging.StreamHandler()
		self.console_handler.setLevel(logging.DEBUG)

		# Define a format for the logger
		self.file_handler.setFormatter(self.format)
		self.console_handler.setFormatter(self.format)

		# Make logger use both handlers
		self.logger.addHandler(self.file_handler)
		self.logger.addHandler(self.console_handler)

	def get_logger(self):
		return self.logger

	def log_metadata(self, file_path, change_type, root):
		logger = self.get_logger()
		file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
		file_checksum = FolderSynchronizer.file_checksum(None, file_path)
		log_entry = {
			'path': os.path.relpath(file_path, root),
			'timestamp': file_mod_time,
			'checksum': file_checksum,
			'change_type': change_type
		}
		self.write_metadata(log_entry)

	def write_metadata(self, log_entry):
		metadata_file = "updates.json"
		with self.metadata_lock:
			if os.path.exists(metadata_file):
				with open(metadata_file, 'r') as f:
					data = json.load(f)
			else:
				data = []
			data.append(log_entry)
			with open(metadata_file, 'w') as f:
				json.dump(data, f, indent=4)
