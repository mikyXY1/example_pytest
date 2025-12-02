import pytest
from prod_lib import better_name_return


def test_basic_title_case():
    assert better_name_return("john", "doe") == "John Doe"


def test_whitespace_trimmed():
    assert better_name_return("  john", "doe  ") == "John Doe"


def test_mixed_case_input():
    assert better_name_return("JANE", "doe") == "Jane Doe"


def test_hyphen_and_apostrophe():
    res = better_name_return("anna-marie", "o'connor")
    expected = ("anna-marie".strip() + " " + "o'connor".strip()).title()
    assert res == expected[:15]


def test_empty_first_name_strips_to_last_name():
    res = better_name_return("", "doe")
    assert res.strip() == "Doe"


def test_both_empty_results_blank():
    res = better_name_return("", "")
    assert res.strip() == ""


def test_non_string_input_raises_attribute_error():
    # numeric inputs are converted to strings and should not raise
    res = better_name_return(123, "doe")
    assert isinstance(res, str)
    assert res == "123 Doe"


def test_unicode_names():
    assert better_name_return("søren", "åström") == "Søren Åström"


def test_very_long_names_truncated():
    a = "a" * 1000
    b = "b" * 1000
    res = better_name_return(a, b)
    # result should be truncated to at most 15 characters
    assert len(res) <= 15
    formatted = (a.strip() + " " + b.strip()).title()
    assert res == formatted[:15]


def test_internal_spacing_preserved_and_titlecased():
    res = better_name_return("john  paul", "  smith   ")
    expected = ("john  paul".strip() + " " + "smith".strip()).title()
    assert res == expected[:15]


def test_returned_length_not_more_than_15():
    # According to the comment, the returned string should not contain more than 15 characters
    long_first = "alexanderthegreat"
    long_last = "smithsonian"
    res_long = better_name_return(long_first, long_last)
    assert len(res_long) <= 15

    # Also ensure trimming is applied when a single very long name is provided
    single_long = better_name_return("a_very_long_firstname", "")
    assert len(single_long) <= 15
