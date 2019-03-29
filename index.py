# Utilities
from io import open
from sys import exit
from time import sleep
from utilites import cls

# Cleaners
from cleaners import M3UFileCleaner

# Readers
from readers import M3UFileReader

# Parsers
from parsers import SimpleTextParser

# Writers
from writers import BaseFileWriter


class Menu:

	def pick_an_option():
		"""The option menu."""
		while True:
			print("1)Limpiar una lista M3U\n2)Transformar archivo M3U a Simple Text \n3)Salir\n")
			option = input("Elige una opcion:\n")

			if option == "1":
				Menu.option1()
			elif option == "2":
				Menu.option2()
			elif option == "3":
				Menu.option3()
			else:
				print("Por favor elige una opcion correcta.")
				sleep(1)
				Menu.pick_an_option()

	def option1():
		"""What to do if the user picks option 1
		Handles getting data from the user, and
		calls Cleaner Class to clean the file.
		"""
		file = Menu.GetData.get_file()
		output_file = Menu.GetData.get_output_file()

		patterns = Menu.GetData.get_patterns()

		cleaner = M3UFileCleaner(patterns)
		cleaner.delete_unneeded_lines(file, output_file)

		cls()

		print(f'Se han borrado {cleaner.deleted_lines} lineas.')

		sleep(2)

	def option2():
		"""What to do if user picks option 2.

		Parses a m3u file to a simple_text file.
		"""

		file = Menu.GetData.get_file()
		output_file = Menu.GetData.get_output_file()
		separator_character = Menu.GetData.get_separator_character()

		segments, length = M3UFileReader.read(file)

		parser = SimpleTextParser.M3U(separator_character)
		simple_text_list = parser.parse(segments)

		BaseFileWriter.write_lines(simple_text_list, output_file)

		print(f'{length} lineas han sido convertidas a formato Simple Text')

	def option3():
		"""What to do if user picks option 3.
		Exits the program.
		"""
		print("Hasta luego :).")
		exit()

	class GetData:

		def get_patterns():
			"""Manages obtaining user patterns."""

			patterns = []
			while True:
				new_pattern = input('Introduce un patron(C para cancelar)')
				if new_pattern == 'C':
					break
				else:
					patterns.append(new_pattern)
			return patterns

		def get_file():
			"""Manages obtaining initial file."""

			file_name = input('Introduce el nombre de tu archivo con extension\n')
			file = open(file_name, 'r+', encoding='utf-8')

			return file

		def get_output_file():
			"""Manages obtaining output file."""

			output_file_name = input('Introduce el nombre de el archivo de salida\n')
			output_file = open(output_file_name, 'w', encoding='utf-8')

			return output_file

		def get_separator_character():
			"""Manages obtaining the separator character from user"""
			separator_character = input("Introduce el caracter separador porfavor(Deja vacio o da un espacio para espacio):\n")
			return separator_character


Menu.pick_an_option()
