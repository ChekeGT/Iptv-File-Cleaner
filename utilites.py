# Utilities
from os import system, name


def cls():
	if name == 'posix':
		system("clear")
	else:
		system("cls")
