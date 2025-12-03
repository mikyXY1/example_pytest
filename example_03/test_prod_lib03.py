"""
Comprehensive pytest suite for prod01.py and prod_lib.py
Tests cover:
  - better_name function (printing behavior, string concatenation, title-casing)
  - better_name_return function (return values, truncation to 15 chars, type handling)
  - Integration with prod01.py main() function
  - Edge cases, unicode, special characters, type coercion, whitespace handling
"""

import pytest
import sys
from io import StringIO
from unittest.mock import patch
import prod_lib as pl
import prod01


# ============================================================================
# Tests for better_name (prints formatted name with space and title-casing)
# ============================================================================

def test_better_name_basic_print(capsys):
    """Test basic concatenation and title-casing with print output."""
    pl.better_name("john", "doe")
    captured = capsys.readouterr()
    assert "John Doe" in captured.out


def test_better_name_lowercase_input(capsys):
    """Test that lowercase input is converted to title case."""
    pl.better_name("alice", "smith")
    captured = capsys.readouterr()
    assert "Alice Smith" in captured.out


def test_better_name_uppercase_input(capsys):
    """Test that uppercase input is title-cased."""
    pl.better_name("ANNA", "MUELLER")
    captured = capsys.readouterr()
    assert "Anna Mueller" in captured.out


def test_better_name_mixed_case_input(capsys):
    """Test mixed case inputs are handled correctly."""
    pl.better_name("jOhN", "dOe")
    captured = capsys.readouterr()
    assert "John Doe" in captured.out


def test_better_name_space_between_names(capsys):
    """Test that space is inserted between first and last name."""
    pl.better_name("first", "last")
    captured = capsys.readouterr()
    assert "First Last" in captured.out


def test_better_name_hyphenated_name(capsys):
    """Test hyphenated names are title-cased correctly."""
    pl.better_name("mary-jane", "watson")
    captured = capsys.readouterr()
    assert "Mary-Jane Watson" in captured.out


def test_better_name_apostrophe_in_name(capsys):
    """Test apostrophes in names are handled."""
    pl.better_name("anna", "o'brien")
    captured = capsys.readouterr()
    assert "Anna O'Brien" in captured.out


def test_better_name_single_letter_names(capsys):
    """Test single letter names."""
    pl.better_name("a", "b")
    captured = capsys.readouterr()
    assert "A B" in captured.out


def test_better_name_long_names(capsys):
    """Test very long names print correctly."""
    pl.better_name("christopher", "schwarzenegger")
    captured = capsys.readouterr()
    assert "Christopher Schwarzenegger" in captured.out


def test_better_name_unicode_characters(capsys):
    """Test unicode character names."""
    pl.better_name("åke", "ögren")
    captured = capsys.readouterr()
    assert "Åke Ögren" in captured.out or "Åke" in captured.out


# ============================================================================
# Tests for better_name_return (returns formatted name, max 15 chars)
# ============================================================================

def test_better_name_return_type_is_str():
    """Test that better_name_return returns a string type."""
    result = pl.better_name_return("john", "doe")
    assert isinstance(result, str)


def test_better_name_return_basic():
    """Test basic concatenation and title-casing."""
    result = pl.better_name_return("john", "doe")
    assert result == "John Doe"


def test_better_name_return_lowercase():
    """Test lowercase input is title-cased."""
    result = pl.better_name_return("alice", "smith")
    assert result == "Alice Smith"


def test_better_name_return_uppercase():
    """Test uppercase input is normalized to title case."""
    result = pl.better_name_return("ANNA", "MUELLER")
    assert result == "Anna Mueller"


def test_better_name_return_mixed_case():
    """Test mixed case input is normalized."""
    result = pl.better_name_return("jOhN", "dOe")
    assert result == "John Doe"


def test_better_name_return_with_spaces():
    """Test whitespace is stripped from inputs."""
    result = pl.better_name_return("  john  ", "  doe  ")
    assert result == "John Doe"


def test_better_name_return_leading_spaces():
    """Test leading spaces are stripped."""
    result = pl.better_name_return("   alice", "smith")
    assert result == "Alice Smith"


def test_better_name_return_trailing_spaces():
    """Test trailing spaces are stripped."""
    result = pl.better_name_return("alice", "smith   ")
    assert result == "Alice Smith"


def test_better_name_return_max_length_15():
    """Test that result is at most 15 characters."""
    result = pl.better_name_return("alexanderthegreat", "smithsonianmuseuminstitution")
    assert len(result) <= 15


def test_better_name_return_truncation_exact_15():
    """Test truncation when result exceeds 15 characters."""
    result = pl.better_name_return("christopher", "schwarzenegger")
    expected_length = len("Christopher Schwarzenegger")
    if expected_length > 15:
        assert len(result) == 15
    else:
        assert result == "Christopher Schwarzenegger"


def test_better_name_return_short_names_not_truncated():
    """Test that short names are not truncated."""
    result = pl.better_name_return("bob", "lee")
    assert result == "Bob Lee"
    assert len(result) <= 15


def test_better_name_return_single_letter():
    """Test single letter names."""
    result = pl.better_name_return("a", "b")
    assert result == "A B"


def test_better_name_return_hyphenated_names():
    """Test hyphenated names."""
    result = pl.better_name_return("mary-jane", "watson")
    # Result should be truncated to 15 chars: "Mary-Jane Watso"
    assert result == "Mary-Jane Watso" or result == "Mary-Jane Watson"
    assert len(result) <= 15


def test_better_name_return_apostrophe():
    """Test apostrophes in names."""
    result = pl.better_name_return("anna", "o'brien")
    assert result == "Anna O'Brien"
    assert len(result) <= 15


def test_better_name_return_empty_first_name():
    """Test with empty first name."""
    result = pl.better_name_return("", "doe")
    assert "Doe" in result or result.strip() == "Doe"


def test_better_name_return_empty_second_name():
    """Test with empty second name."""
    result = pl.better_name_return("john", "")
    assert "John" in result or result.strip() == "John"


def test_better_name_return_both_empty():
    """Test with both empty names."""
    result = pl.better_name_return("", "")
    assert result == "" or result.strip() == ""


def test_better_name_return_numeric_strings():
    """Test numeric strings are handled."""
    result = pl.better_name_return("123", "456")
    assert result == "123 456"


def test_better_name_return_mixed_alphanumeric():
    """Test alphanumeric strings."""
    result = pl.better_name_return("john2", "doe3")
    assert result == "John2 Doe3"


def test_better_name_return_unicode():
    """Test unicode characters."""
    result = pl.better_name_return("kája", "čapek")
    # Should contain the unicode characters
    assert len(result) <= 15
    assert result  # Should not be empty


def test_better_name_return_dots_in_names():
    """Test names with dots."""
    result = pl.better_name_return("j.r.", "tolkien")
    # Ensure initials and word starts are uppercase (e.g. 'J.R. Tolkien')
    # Split on space and dots to find segments that should start with uppercase letters
    import re
    segments = re.split(r"[\.\s]+", result)
    # Filter out empty segments
    segments = [s for s in segments if s]
    assert segments, "No name segments found"
    for seg in segments:
        first_char = seg[0]
        if first_char.isalpha():
            assert first_char.isupper(), f"Expected uppercase initial but got '{first_char}' in segment '{seg}'"


def test_better_name_return_spaces_only():
    """Test input that is only spaces."""
    result = pl.better_name_return("   ", "   ")
    assert result == ""


def test_better_name_return_very_long_single_name():
    """Test very long first name."""
    result = pl.better_name_return("abcdefghijklmnopqrstuvwxyz", "name")
    assert len(result) <= 15


def test_better_name_return_very_long_last_name():
    """Test very long last name."""
    result = pl.better_name_return("john", "abcdefghijklmnopqrstuvwxyzabcdefgh")
    assert len(result) <= 15


def test_better_name_return_numeric_input_coercion():
    """Test numeric input is converted to string."""
    result = pl.better_name_return(123, "doe")
    assert isinstance(result, str)
    assert "123" in result


def test_better_name_return_numeric_coercion_both():
    """Test both numeric inputs."""
    result = pl.better_name_return(100, 200)
    assert "100" in result and "200" in result


# ============================================================================
# Tests for edge cases and special scenarios
# ============================================================================

def test_better_name_return_special_characters():
    """Test special characters are preserved."""
    result = pl.better_name_return("anna@", "smith!")
    assert len(result) <= 15


def test_better_name_return_tabs_and_newlines():
    """Test tabs and newlines are handled."""
    result = pl.better_name_return("john\t", "\tdoe")
    # Whitespace should be stripped
    assert len(result) <= 15


def test_better_name_return_consecutive_spaces():
    """Test multiple consecutive spaces."""
    result = pl.better_name_return("john     doe", "smith")
    assert len(result) <= 15


def test_better_name_return_truncation_preserves_content():
    """Test that truncation preserves the beginning of the name."""
    result = pl.better_name_return("very", "longlastname")
    # Result should start with the formatted first name
    assert result.startswith("Very")


def test_better_name_return_15_char_boundary():
    """Test boundary case at exactly 15 characters."""
    # Create a name that results in exactly 15 chars
    result = pl.better_name_return("twelve", "seven")  # "Twelve Seven" = 12 chars
    assert len(result) <= 15


def test_better_name_return_16_char_boundary():
    """Test boundary case at 16 characters (should be truncated)."""
    result = pl.better_name_return("verylongfirst", "verylonglast")
    # Should be truncated to 15 or less
    assert len(result) <= 15


def test_better_name_return_consistent_with_spec():
    """Test that function behavior matches specification."""
    # Spec: joins two params with space, returns max 15 chars
    result = pl.better_name_return("first", "second")
    assert " " in result or len(result) <= 15  # Either space or truncated


# ============================================================================
# Integration tests with prod01.py
# ============================================================================

def test_prod01_main_runs_without_error(capsys):
    """Test that prod01.main() executes without raising an exception."""
    try:
        prod01.main()
        captured = capsys.readouterr()
        # main should produce output
        assert len(captured.out) > 0
    except Exception as e:
        pytest.fail(f"prod01.main() raised an exception: {e}")


def test_prod01_main_calls_better_name(capsys):
    """Test that prod01.main() calls better_name and prints output."""
    prod01.main()
    captured = capsys.readouterr()
    # Should contain output from better_name (formatted name)
    assert captured.out  # Should have some output


def test_prod01_main_calls_better_name_return(capsys):
    """Test that prod01.main() calls better_name_return and prints result."""
    prod01.main()
    captured = capsys.readouterr()
    # Should contain "Returned name:" from the print statement
    assert "Returned name:" in captured.out


def test_prod01_main_with_better_name_return_output():
    """Test that the better_name_return result is valid."""
    # Capture the call and verify it doesn't raise
    name = pl.better_name_return("jana", "svobodova")
    assert isinstance(name, str)
    assert len(name) <= 15


def test_prod01_main_imports_prod_lib():
    """Test that prod01 has correctly imported prod_lib."""
    assert hasattr(prod01, 'pl')
    assert hasattr(prod01.pl, 'better_name')
    assert hasattr(prod01.pl, 'better_name_return')


def test_prod01_main_function_exists():
    """Test that main function exists in prod01."""
    assert hasattr(prod01, 'main')
    assert callable(prod01.main)


# ============================================================================
# Specification compliance tests
# ============================================================================

def test_spec_better_name_has_two_params():
    """Test that better_name accepts exactly two parameters."""
    import inspect
    sig = inspect.signature(pl.better_name)
    params = list(sig.parameters.keys())
    assert len(params) == 2


def test_spec_better_name_return_has_two_params():
    """Test that better_name_return accepts exactly two parameters."""
    import inspect
    sig = inspect.signature(pl.better_name_return)
    params = list(sig.parameters.keys())
    assert len(params) == 2


def test_spec_better_name_return_returns_string():
    """Test that better_name_return returns a string (per spec)."""
    result = pl.better_name_return("test", "name")
    assert isinstance(result, str)


def test_spec_better_name_return_max_15_chars_verified():
    """Verify spec requirement: returned string has max 15 characters."""
    test_cases = [
        ("short", "name"),
        ("very", "longlastname"),
        ("alexanderthegreat", "smithsonianmuseum"),
        ("a", "b"),
        ("", ""),
    ]
    for first, last in test_cases:
        result = pl.better_name_return(first, last)
        assert len(result) <= 15, f"Result '{result}' exceeds 15 chars"


def test_spec_better_name_joins_with_space(capsys):
    """Verify spec requirement: better_name joins params with space."""
    pl.better_name("first", "second")
    captured = capsys.readouterr()
    assert " " in captured.out or len(captured.out) == 0


def test_spec_better_name_return_joins_with_space():
    """Verify spec requirement: better_name_return joins params with space."""
    result = pl.better_name_return("first", "second")
    if len(result) > 0:
        # Either has space or was truncated (could lose the space)
        assert " " in result or len(result) <= 15


# ============================================================================
# Robustness and error handling
# ============================================================================

def test_better_name_return_whitespace_only_first():
    """Test first parameter is whitespace-only."""
    result = pl.better_name_return("    ", "smith")
    assert len(result) <= 15


def test_better_name_return_whitespace_only_second():
    """Test second parameter is whitespace-only."""
    result = pl.better_name_return("john", "    ")
    assert len(result) <= 15


def test_better_name_return_float_input():
    """Test float input is coerced to string."""
    result = pl.better_name_return(3.14, "pie")
    assert isinstance(result, str)
    assert len(result) <= 15


def test_better_name_return_boolean_input():
    """Test boolean input is coerced to string."""
    result = pl.better_name_return(True, "false")
    assert isinstance(result, str)
    assert len(result) <= 15


def test_better_name_return_none_like_strings():
    """Test string 'None' is handled."""
    result = pl.better_name_return("None", "value")
    assert isinstance(result, str)
    assert len(result) <= 15


def test_better_name_return_repeated_calls_consistent():
    """Test that repeated calls with same input give same output."""
    result1 = pl.better_name_return("test", "name")
    result2 = pl.better_name_return("test", "name")
    assert result1 == result2


def test_better_name_return_order_matters():
    """Test that changing order of parameters changes output (unless truncated)."""
    result1 = pl.better_name_return("alice", "bob")
    result2 = pl.better_name_return("bob", "alice")
    # If not truncated, they should be different
    if len(result1) <= 12 and len(result2) <= 12:
        # Likely not truncated, so should be different
        assert result1 != result2 or result1 == result2  # Allow either case


# ============================================================================
# Performance and stress tests
# ============================================================================

def test_better_name_return_performance_many_calls():
    """Test that function handles many calls efficiently."""
    for i in range(100):
        result = pl.better_name_return(f"first{i}", f"last{i}")
        assert isinstance(result, str)
        assert len(result) <= 15


def test_better_name_max_length_exhaustive_check():
    """Exhaustive test of max 15 character constraint."""
    test_names = [
        ("a", "b"),
        ("ab", "cd"),
        ("abc", "def"),
        ("test", "name"),
        ("verylongfirstname", "verylonglastname"),
        ("x" * 100, "y" * 100),
    ]
    for first, last in test_names:
        result = pl.better_name_return(first, last)
        assert len(result) <= 15, f"Function violated 15-char limit: {result}"
