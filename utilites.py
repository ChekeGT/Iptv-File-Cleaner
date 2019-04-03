"""All the stuff that i dont know how to name ends here."""

# Parsers
from parsers import SimpleTextParser

# Writers
from writers import BaseFileWriter

def ParseAndWriteM3UToSimpleText(output_file, decoder_type, segment_list):
	"""Manages parsing and writing depending on the decoder_type"""

	if decoder_type == 'OpenBox':
		OpenBoxParser = SimpleTextParser.M3U(" ")
		parsed_lines = OpenBoxParser.parse(segment_list)

	elif decoder_type == 'Freesat | GT Media':
		FreesatGtMediaparser = SimpleTextParser.M3U(",")
		parsed_lines = FreesatGtMediaparser.parse(segment_list)

	BaseFileWriter.write_lines(parsed_lines, output_file)
