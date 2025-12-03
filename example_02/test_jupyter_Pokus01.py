import json
from pathlib import Path


NOTEBOOK_PATH = Path(__file__).with_name("Pokus01.ipynb")


def load_notebook(path: Path):
	assert path.exists(), f"Notebook not found: {path}"
	text = path.read_text(encoding="utf-8")
	# Notebook may be JSON; parse it
	return json.loads(text)


def test_notebook_has_expected_number_of_cells():
	nb = load_notebook(NOTEBOOK_PATH)
	assert "cells" in nb
	# Based on the provided notebook, expect at least 6 cells
	assert len(nb["cells"]) >= 6


def test_first_cell_is_markdown_title():
	nb = load_notebook(NOTEBOOK_PATH)
	first = nb["cells"][0]
	assert first.get("cell_type") == "markdown"
	source = "".join(first.get("source", []))
	assert "Jupyter Notebook" in source


def test_second_cell_contains_hello_world_print():
	nb = load_notebook(NOTEBOOK_PATH)
	second = nb["cells"][1]
	assert second.get("cell_type") == "code"
	src = "\n".join(second.get("source", []))
	assert 'msg1 = "Hello, World!"' in src
	assert "print(msg1)" in src


def test_third_cell_markdown_contains_message():
	nb = load_notebook(NOTEBOOK_PATH)
	third = nb["cells"][2]
	assert third.get("cell_type") == "markdown"
	source = "".join(third.get("source", []))
	assert "Toto je další zpráva" in source


def test_fourth_cell_contains_hello_earth():
	nb = load_notebook(NOTEBOOK_PATH)
	fourth = nb["cells"][3]
	assert fourth.get("cell_type") == "code"
	src = "\n".join(fourth.get("source", []))
	assert 'msg2 = "Hello, Earth!"' in src
	assert "print(msg2)" in src


def test_markdown_before_bash_is_bold():
	nb = load_notebook(NOTEBOOK_PATH)
	# find a markdown cell that contains the bold label
	found = False
	for cell in nb["cells"]:
		if cell.get("cell_type") == "markdown":
			text = "".join(cell.get("source", []))
			if "Zobrazení zprávy pomocí Bash příkazu" in text:
				found = True
				assert "**" in text or text.strip().startswith("**")
	assert found, "Expected markdown label before bash cell not found"


def test_bash_cell_uses_echo():
	nb = load_notebook(NOTEBOOK_PATH)
	# find a code cell that contains echo or !echo
	found = False
	for cell in nb["cells"]:
		if cell.get("cell_type") == "code":
			src = "\n".join(cell.get("source", []))
			if 'echo "Message from Bash Shell!"' in src or '!echo "Message from Bash Shell!"' in src:
				found = True
	assert found, "Bash echo command not found in any code cell"


def test_no_cells_contain_forbidden_text():
	nb = load_notebook(NOTEBOOK_PATH)
	forbidden = ["rm -rf", "import os.system", "subprocess.call"]
	for cell in nb["cells"]:
		src = "".join(cell.get("source", []))
		for token in forbidden:
			assert token not in src

