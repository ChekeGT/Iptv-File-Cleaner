class BaseFileWriter:
	"""Manages writing of files."""

	def write_lines(lines, output_file):
		"""Write the lines on the output file."""
		
		for line in lines:
			output_file.write(line)
