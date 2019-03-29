class SimpleTextParser:
	"""Parses a file to the format simple text."""
	
	class M3U:
		"""How to parse the m3u Files to a simple text file."""

		def __init__(self, separator_character):
			"""Initialize the class"""
			if separator_character == "":
				separator_character = " "
			self.separator_character = separator_character

		def parse(self, segment_list):
			"""Manages the parsing of the m3u file."""

			return list(
				map(
					self.remap, segment_list
				)
			)

		def remap(self, segment):
			"""Maps the segment and transforms it into the simple text format"""

			url = self.get_url(segment)
			name = self.get_name(segment)

			return f'{name}{self.separator_character}{url}\n'
