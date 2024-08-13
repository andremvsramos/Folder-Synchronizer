import os
import subprocess
import json
import sys
import shutil
from synchronizer import FolderSynchronizer

class RestoreSystem:

	DEFAULT = {
		"script": "../OneWay/main.py",
		"flags": ["--interval", "5", "--versioned-backup"],
	}

	def __init__(self, origin, logger, config="config.json"):
		self.origin = origin
		self.logger = logger
		self.log = logger.get_logger()
		self.compiler = "python3"
		self.info_file = ".info.json"
		self.versions = "./__versions__"
		self.versions_source = f"./__versions__/{self.origin}"
		self.versions_source_latest = f"./__versions__/{self.origin}/_1"
		self.versions_source_previous = f"./__versions__/{self.origin}/_0"
		self.versions_backup = f"./__versions__/{self.origin}_backup"
		self.versions_backup_latest = f"./__versions__/{self.origin}_backup/_1"
		self.versions_backup_previous = f"./__versions__/{self.origin}_backup/_0"
		self.source_logs = ["--log", f"./__versions__/{self.origin}/versionlogs.log"]
		self.backup_logs = ["--log", f"./__versions__/{self.origin}_backup/versionlogs.log"]
		#DEFAULT
		self.config = config
		self.script = self.DEFAULT["script"]
		self.flags = self.DEFAULT["flags"]
		self.restore_source_process = None
		self.restore_backup_process = None
		#LOAD CONFIG
		self.load_config()
		self.record_paths()

	def get_versions(self):
		return self.versions

	def get_config(self):
		return self.config

	def create_default_config(self):
		with open(self.config, 'w') as f:
			json.dump(self.DEFAULT, f, indent=4)

	def load_config(self):
		if not os.path.exists(self.config):
			self.log.warning(f"Config file {self.config} not found. Creating with default values.")
			self.create_default_config()

		with open(self.config, 'r') as f:
			config = json.load(f)

		self.script = config.get("script", self.DEFAULT["script"])
		self.flags = config.get("flags", self.DEFAULT["flags"])

	def record_paths(self):
		data = {}

		if os.path.exists(self.info_file):
			with open(self.info_file, 'r') as f:
				data = json.load(f)

		data[f"{self.origin}"] = os.path.abspath(self.origin)
		backup_path = f"{self.origin}_backup"
		if os.path.exists(backup_path):
			data[f"{self.origin}_backup"] = os.path.abspath(backup_path)

		with open(self.info_file, 'w') as f:
			json.dump(data, f, indent=4, ensure_ascii=False)

	def get_recorded_path(self, path):
		if os.path.exists(self.info_file):
			with open(self.info_file, 'r', encoding='utf-8') as f:
				data = json.load(f)
				for key, value in data.items():
					if value == path:
						return key
		return None

	def run_versioned_backups(self):
		if not os.path.exists(self.versions):
			os.makedirs(self.versions)
		if not os.path.exists(self.versions_source):
			os.makedirs(self.versions_source)
		if not os.path.exists(self.versions_backup):
			os.makedirs(self.versions_backup)
		command = [self.compiler, self.script, self.origin, self.versions_source] + self.flags + self.source_logs
		self.log.info(f"Running versioned backup: {command}")
		global source_process
		source_process = subprocess.Popen(command)
		command = [self.compiler, self.script, self.origin, self.versions_backup] + self.flags + self.backup_logs
		self.log.info(f"Running versioned backup: {command}")
		global backup_process
		backup_process = subprocess.Popen(command)

	def get_backup_path(self, version, type):
		if type == 'source':
			if version == 'latest':
				return self.versions_source_latest
			else:
				return self.versions_source_previous
		elif type == 'backup':
			if version == 'latest':
				return self.versions_backup_latest
			else:
				return self.versions_backup_previous
		self.log.error(f"Invalid type specified: {type}")
		sys.exit(1)

	def restore_version(self, target, version):
		if target == self.origin:
			backup_path = self.get_backup_path(version, 'source')
		elif target == f"{self.origin}_backup":
			backup_path = self.get_backup_path(version, 'backup')
		else:
			self.log.error(f"Invalid target specified: {target}")
			sys.exit(1)

		self.perform_restoration(target, backup_path)

	def perform_restoration(self, target, backup_path):
		if not os.path.exists(backup_path):
			self.log.error(f"Backup not found for target: {target}")
			sys.exit(1)

		if os.path.exists(target):
			shutil.rmtree(target)

		#os.makedirs(target)
		shutil.copytree(backup_path, target)
