"""Cleaners module 

Handles all the stuff related to delete patterns of iptv lists.
"""

# Readers
from readers import M3UFileReader


class BaseIptvFileCleaner:
	"""Base Iptv File Cleaner

	An Iptv file cleaner manages the cleaning of a list,
	it could be on different formats but this are the base
	things that you will ned to do.
	"""

	def __init__(self, patterns):
		"""Initialization of the class

		Parameters:
			patterns --> Since we are going to use it on multiple functions it's better put it on self.
		"""

		self.patterns = patterns


class M3UFileCleaner(BaseIptvFileCleaner):
	"""Manages the line filtering of a iptv list which type is M3U"""

	def delete_unneeded_lines(self, file):
		"""Deletes the lines that the user dont want"""

		segments, length = M3UFileReader.read(file)

		lines = list(
			filter(
				self.filter_lines,
				segments
			)
		)

		lines = M3UFileReader.expand_segments(lines)

		self.deleted_lines = abs(
			len(lines) - length
		)

		return lines

	def filter_lines(self, segment):
		"""Returns if a line matches with a pattern."""

		line = segment[1]
		patterns = self.patterns
		for pattern in patterns:
			if pattern in line:
				return False

		return True
