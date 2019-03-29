# Utilities
from functools import reduce


class M3UFileReader:
	"""Manages the reading of a m3u file."""

	def read(self, file):
		"""Manages the reading of a m3u file 
		
		Returns a tuple with the lines in format of segments and its length.
		"""

		lines = file.readlines()
		lines.pop(0)

		return (
			M3UFileReader.cut_lines(
				lines
			),
			len(lines)
		)

	def cut_lines(lines):
		"""Cut all the lines in segments of 2."""
		
		new_lines = [
			[
				lines[lines.index(line) - 1],
				line
			] 
			for line in lines
			if not line.startswith('#') and 
			not line.startswith('-') and
			not line.startswith(' ') and
			not line == '\n'
		]
		return new_lines

	def expand_segments(segments):
		"""Sum all the segments and creates one only list."""

		return reduce(
			lambda x,y: x + y,
			segments
		)

	def get_url(segment):
		"""Gets an url of a segment."""

		# Segment 1 contains the url (it is coded on line 79)
		# We delete line jumps cause we want these two values to be together
		return segment[1].replace("\n", "")

	def get_name(segment):
		"""Gets the name of a segment."""
		line = segment[0]

		# Where tvg-name tag starts + 10 is exactly where
		# the channel television name starts.
		tvg_name_start = line.index('tvg-name="') + 10
		# Where tvg-logo starts is exactly where
		# the channel television name ends.
		tvg_name_end = line.index('tvg-logo')

		# We delete all the quotes and spaces cause we just want the name.
		name = line[tvg_name_start:tvg_name_end].replace('"', "")
		name = name.replace(" ", "")

		return name
