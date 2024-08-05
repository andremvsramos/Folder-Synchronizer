import logging

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
