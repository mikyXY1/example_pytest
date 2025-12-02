# test_prod_lib.py - unit tests for prod_lib.better_name function using pytest
#pytest, ktery testuje fci better_name z modulu prod_lib.py

import pytest
from prod_lib import better_name


def test_better_name_basic_title_case(capsys):
	better_name("john", "doe")
	captured = capsys.readouterr()
	assert captured.out == "John Doe\n"


def test_better_name_strips_and_title(capsys):
	# Leading/trailing spaces should be present in the result if input contains them (function doesn't strip)
	better_name(" john ", " doe ")
	captured = capsys.readouterr()
	# Title() will capitalize letters but keep spaces
	assert captured.out == " John   Doe \n"


def test_better_name_handles_hyphen_and_apostrophe(capsys):
	better_name("anne-marie", "o'neill")
	captured = capsys.readouterr()
	assert captured.out == "Anne-Marie O'Neill\n"


def test_better_name_handles_unicode(capsys):
	better_name("čapek", "karel")
	captured = capsys.readouterr()
	assert captured.out == "Čapek Karel\n"


def test_better_name_returns_none(capsys):
	# Function prints only; return value should be None
	rv = better_name("john", "doe")
	assert rv is None


def test_better_name_non_str_raises_typeerror():
	with pytest.raises(TypeError):
		# Passing an int should raise when concatenating with str
		better_name(123, "doe")


def test_better_name_long_strings(capsys):
	first = "a" * 200
	second = "b" * 300
	better_name(first, second)
	captured = capsys.readouterr()
	# Title should keep same length but first letters capitalized
	assert len(captured.out.strip()) == 200 + 1 + 300


def test_better_name_empty_strings(capsys):
	better_name("", "")
	captured = capsys.readouterr()
	# Will print a single space then newline (function constructs ' ')
	assert captured.out == " \n"


def test_better_name_multiple_spaces_between(capsys):
	better_name("John", "  Doe")
	captured = capsys.readouterr()
	assert captured.out == "John   Doe\n"


def test_better_name_multiple_words_in_names(capsys):
	better_name("Mary Ann", "van buren")
	captured = capsys.readouterr()
	assert captured.out == "Mary Ann Van Buren\n"

