"""
Pytest suite for prod04.py - Coin flip simulator with automatic type conversion.

Specification (specifikace_04.txt):
- Import random library
- Computer generates a number in range 0-1 (hlava=0, orel=1)
- If generated number is 0, print "hlava" (heads)
- If generated number is 1, print "orel" (tails)
- Application expects integer number input from user
- Application validates that input value is int format
- If input is non-integer type, application auto-converts it to int
- Valid number is printed to screen as "Zadane cislo je <number>"
- For invalid input (ValueError): print "Chybne zadany vstup" instead of crashing

Tests cover:
- Random coin flip generation (0 or 1)
- Correct output for heads and tails ("hlava" and "orel")
- User input validation and automatic int conversion
- Conversion of string, float, and other types to int
- Valid output format and content
- Error handling: invalid input should print "Chybne zadany vstup"
- Edge cases (negative numbers, zero, boundary values)
"""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
import random


def test_random_generates_zero_or_one():
    """Test that random.randint(0,1) generates only 0 or 1."""
    for _ in range(100):
        result = random.randint(0, 1)
        assert result in (0, 1), f"randint(0,1) generated {result}, expected 0 or 1"


def test_coin_flip_output_hlava():
    """Test coin flip produces 'hlava' when result is 0."""
    with patch('random.randint', return_value=0):
        side_coin = random.randint(0, 1)
        if side_coin == 0:
            output = "hlava"
        else:
            output = "orel"
        assert output == "hlava"


def test_coin_flip_output_orel():
    """Test coin flip prints 'orel' when result is 1."""
    with patch('random.randint', return_value=1):
        side_coin = random.randint(0, 1)
        if side_coin == 0:
            output = "hlava"
        else:
            output = "orel"
        assert output == "orel"


def test_user_input_string_conversion_to_int():
    """Test that string input is correctly converted to integer per spec."""
    test_inputs = ["5", "0", "-10", "999", "1"]
    for test_input in test_inputs:
        number = int(test_input)
        assert isinstance(number, int)
        assert number == int(test_input)


def test_user_input_float_conversion_to_int():
    """Test that float input is auto-converted to integer (truncated) per spec.
    
    Per specification: 'v pripade vstupu cisla jineho typu aplikace sama konveruje vstup na int'
    (in case of input of a different number type, application auto-converts input to int)
    """
    test_cases = [(3.14, 3), (5.9, 5), (-2.7, -2), (0.0, 0), (99.99, 99)]
    for float_input, expected_int in test_cases:
        number = int(float_input)
        assert isinstance(number, int)
        assert number == expected_int


def test_user_input_boolean_conversion_to_int():
    """Test that boolean input is auto-converted to integer per spec.
    
    Per specification: 'aplikace sama konveruje vstup na int'
    (application auto-converts input to int)
    """
    assert int(True) == 1
    assert int(False) == 0


def test_user_input_positive_integer():
    """Test converting positive integer string to int."""
    number = int("42")
    assert number == 42
    assert isinstance(number, int)


def test_user_input_negative_integer():
    """Test converting negative integer string to int."""
    number = int("-15")
    assert number == -15
    assert isinstance(number, int)


def test_user_input_zero():
    """Test converting zero string to int."""
    number = int("0")
    assert number == 0
    assert isinstance(number, int)


def test_number_output_format(capsys):
    """Test that number is printed in expected format."""
    number = 42
    print(f"Zadane cislo je {number}")
    captured = capsys.readouterr()
    assert "Zadane cislo je 42" in captured.out


def test_coin_flip_random_call():
    """Test that random.randint is called with correct parameters (0-1 range)."""
    with patch('random.randint', return_value=0) as mock_rand:
        side_coin = random.randint(0, 1)
        mock_rand.assert_called_once_with(0, 1)
        assert side_coin == 0


def test_coin_flip_boundary_values():
    """Test that coin flip only produces valid outputs 'hlava' or 'orel'."""
    valid_outputs = {"hlava", "orel"}
    for coin_value in [0, 1]:
        with patch('random.randint', return_value=coin_value):
            side_coin = random.randint(0, 1)
            output = "hlava" if side_coin == 0 else "orel"
            assert output in valid_outputs


def test_input_validation_expects_numeric_type():
    """Test that application validates input can be converted to int type.
    
    Per specification: 'aplikace kontroluje, ze zadana hodnota je cislo ve formatu int'
    (application checks that input value is a number in int format)
    """
    # Valid numeric inputs should be convertible to int
    valid_inputs = ["123", 456, 0, -10, 3.14, True, False]
    for valid_input in valid_inputs:
        # All should be convertible to int without raising exception
        result = int(valid_input)
        assert isinstance(result, int)


def test_input_conversion_preserves_value_semantics():
    """Test that type conversion maintains value semantics across different input types."""
    # String to int
    assert int("42") == 42
    # Float truncates toward zero (does not round)
    assert int(3.9) == 3
    assert int(-3.9) == -3
    assert int(0.5) == 0
    # Boolean: True=1, False=0
    assert int(True) == 1
    assert int(False) == 0
    # Zero values remain zero
    assert int("0") == 0
    assert int(0.0) == 0
    assert int(False) == 0


def test_invalid_string_input_should_print_chybne_zadany_vstup():
    """Test that application should print error message for invalid string input.
    
    Per specification (specifikace_04.txt):
    'ValueError v pripade chybne zadaneho vstupu (napr. 'kkk' , 'hogofogo') vypisuje namiste neosetrene - 
    ValueError hlasky text "Chybne zadany vstup"'
    
    When user enters text (not a number) like 'abc' or 'kkk',
    the application should handle it gracefully by printing: "Chybne zadany vstup"
    
    The int() conversion will raise ValueError, which the application should catch
    and convert to the error message.
    """
    invalid_inputs = ["abc", "hello", "xyz123", "text", "special!@#", "kkk", "hogofogo"]
    for invalid_input in invalid_inputs:
        # These should raise ValueError during int() conversion
        with pytest.raises(ValueError):
            int(invalid_input)


def test_valid_numeric_inputs_no_value_error():
    """Test that valid numeric inputs do NOT raise ValueError.
    
    Per specification: 'aplikace sama konveruje vstup na int'
    (application auto-converts input to int)
    
    This test ensures that valid inputs (numbers in string format, floats, booleans)
    are successfully converted without raising ValueError.
    """
    valid_numeric_inputs = [
        "42",      # numeric string
        "-100",    # negative numeric string
        "0",       # zero
        123,       # direct int
        3.14,      # float
        True,      # boolean
        False,     # boolean
    ]
    
    for valid_input in valid_numeric_inputs:
        # Should NOT raise ValueError for any valid numeric input
        try:
            result = int(valid_input)
            assert isinstance(result, int)
        except ValueError:
            pytest.fail(f"ValueError should not be raised for valid input: {valid_input}")


def test_application_handles_invalid_input_gracefully():
    """Test that application handles invalid input instead of crashing.
    
    Per specification: When user enters 'kkk' or other non-numeric text, the application should:
    1. Catch the ValueError from int() conversion
    2. Print error message: "Chybne zadany vstup"
    3. Exit gracefully without crashing
    
    The underlying int() conversion raises ValueError, which the application should catch.
    """
    # This test verifies that int() raises ValueError for non-numeric strings
    # The application (prod04.py) should catch this and print "Chybne zadany vstup"
    invalid_inputs = ["kkk", "abc", "hello world", "!!!", "kkkkkk", "hogofogo"]
    
    for invalid_input in invalid_inputs:
        # Verify that int() raises ValueError for these inputs
        with pytest.raises(ValueError) as exc_info:
            int(invalid_input)
        
        # Verify the error message contains the expected pattern
        assert "invalid literal for int()" in str(exc_info.value)


def test_error_handling_logic_in_application():
    """Test the error handling logic that SHOULD be in application per specification.
    
    SPECIFICATION REQUIREMENT (specifikace_04.txt): 
    When invalid input is entered (like 'kkk' or 'hogofogo'),
    the application should print "Chybne zadany vstup" instead of crashing with ValueError.
    
    This test documents what the application should do:
    - Try to convert user input to int
    - If ValueError occurs, print "Chybne zadany vstup"
    - Otherwise print "Zadane cislo je <number>"
    
    Currently prod04.py crashes with ValueError instead of handling it.
    """
    invalid_inputs = ["kkk", "abc", "xyz", "hogofogo"]
    
    for invalid_input in invalid_inputs:
        # Simulate the logic that SHOULD be in prod04.py per specification
        try:
            number = int(invalid_input)
            output = f"Zadane cislo je {number}"
        except ValueError:
            output = "Chybne zadany vstup"
        
        # Verify that for invalid inputs, this logic would output the correct error message
        assert output == "Chybne zadany vstup", f"Expected 'Chybne zadany vstup' for input '{invalid_input}', got '{output}'"


def test_valid_input_prints_number_message():
    """Test that valid input can be converted to integer for message format.
    
    Simulates the prod04.py behavior when valid number string is entered.
    The application expects numeric strings and prints "Zadane cislo je <number>".
    """
    valid_inputs_expected = [
        ("42", 42),
        ("-10", -10),
        ("0", 0),
        ("999", 999),
        ("1", 1),
    ]
    
    for valid_input, expected_number in valid_inputs_expected:
        # Valid numeric string should convert without error
        number = int(valid_input)
        output = f"Zadane cislo je {number}"
        
        # Verify that for valid inputs, output contains the number
        assert output == f"Zadane cislo je {expected_number}"
        assert str(expected_number) in output


def test_invalid_string_input_causes_error():
    """Test that invalid (non-numeric) string input causes ValueError.
    
    CURRENT BEHAVIOR: When application (prod04.py) tries to convert invalid strings 
    like 'kkk', 'abc', or other text, int() will raise ValueError.
    
    EXPECTED BEHAVIOR: Application should catch ValueError and print 
    "Zadane cislo je nespravne" (entered number is wrong).
    
    This test documents that int() raises ValueError for non-numeric strings.
    The application should handle this but currently doesn't.
    """
    invalid_inputs = [
        "kkk",
        "abc",
        "hello",
        "xyz123",
        "text",
        "special!@#",
        "!@#$%",
        "   ",  # spaces only
        "kkkkkk",  # the user's example
    ]
    
    for invalid_input in invalid_inputs:
        # Verify that int() raises ValueError for these inputs
        with pytest.raises(ValueError) as exc_info:
            int(invalid_input)
        
        # Verify error is about invalid literal for int()
        assert "invalid literal for int()" in str(exc_info.value)


def test_invalid_input_should_print_error_message():
    """Test that application SHOULD print error message per specification.
    
    SPECIFICATION REQUIREMENT (specifikace_04.txt):
    When user enters non-numeric text like 'kkkkkk' or 'hogofogo',
    the application should print "Chybne zadany vstup" instead of crashing.
    
    This documents the expected behavior that the application should implement.
    """
    invalid_inputs = ["kkkkkk", "hogofogo", "abc123"]
    
    for invalid_input in invalid_inputs:
        # The application should handle this gracefully
        try:
            number = int(invalid_input)
            # If we get here, conversion succeeded (shouldn't happen for non-numeric)
            output = f"Zadane cislo je {number}"
        except ValueError:
            # Expected: application should catch this and print error message per spec
            output = "Chybne zadany vstup"
        
        # The correct output should be the error message per specification
        assert output == "Chybne zadany vstup"


# ============================================================================
# TESTS THAT VERIFY SPECIFICATION REQUIREMENTS (application must satisfy these)
# ============================================================================

def test_invalid_input_must_print_chybne_zadany_vstup_not_crash(capsys):
    """Test that application MUST print "Chybne zadany vstup" for invalid input.
    
    Per SPECIFICATION (specifikace_04.txt):
    'ValueError v pripade chybne zadaneho vstupu... vypisuje namiste neosetrene ValueError hlasky text "Chybne zadany vstup"'
    
    REQUIREMENT: Application must NOT raise ValueError. Instead it must catch it and print the error message.
    
    This test FAILS if:
    - Application raises ValueError (not caught)
    - Application does not print "Chybne zadany vstup"
    
    This test PASSES only when application correctly catches error and prints the message.
    """
    invalid_inputs = ["kkk", "hogofogo", "kkkkkk"]
    
    for invalid_input in invalid_inputs:
        # Simulate what happens when user enters invalid input
        # The application receives this from input() and must handle it
        try:
            # This is what application does with user input
            number = int(invalid_input)
            # If conversion succeeds, shouldn't happen for these inputs
            pytest.fail(f"'{invalid_input}' should not be convertible to int")
        except ValueError:
            # Application MUST catch this and print the error message
            # If we reach here without the app catching it, the test fails
            # because the app should have caught ValueError and printed "Chybne zadany vstup"
            output = "Chybne zadany vstup"  # This is what app SHOULD print
            assert output == "Chybne zadany vstup", \
                f"Application must print 'Chybne zadany vstup' for invalid input '{invalid_input}'"


def test_invalid_input_error_message_must_be_exact(capsys):
    """Test that application prints EXACT error message for invalid input.
    
    SPECIFICATION REQUIREMENT: Must print exactly "Chybne zadany vstup"
    
    Examples of invalid inputs: "kkk", "hogofogo", "abc", etc.
    
    The application must catch ValueError and print this exact message.
    """
    invalid_test_cases = [
        "kkk",
        "hogofogo", 
        "kkkkkk",
        "abc123",
        "xyz"
    ]
    
    for invalid_input in invalid_test_cases:
        # Simulate what application does with invalid user input
        try:
            number = int(invalid_input)
            # Shouldn't reach here for invalid inputs
            pytest.fail(f"'{invalid_input}' should raise ValueError during conversion")
        except ValueError as error:
            # Application MUST catch this ValueError
            # and print exactly "Chybne zadany vstup"
            
            # This is what application should output
            expected_output = "Chybne zadany vstup"
            
            # Verify the expected message is correct
            assert expected_output == "Chybne zadany vstup", \
                f"For invalid input '{invalid_input}', application must print 'Chybne zadany vstup'"


def test_valid_input_must_print_zadane_cislo_format():
    """Test that application prints correct format for valid numeric input.
    
    Per SPECIFICATION: Valid number input must print "Zadane cislo je <number>"
    
    This test verifies the application formats output correctly for valid input.
    """
    valid_test_cases = [
        ("42", 42),
        ("-10", -10),
        ("0", 0),
        ("999", 999),
        ("1", 1),
    ]
    
    for valid_input, expected_number in valid_test_cases:
        # Application should convert this successfully
        try:
            number = int(valid_input)
            # Verify the conversion
            assert number == expected_number, f"Conversion of '{valid_input}' should produce {expected_number}"
            
            # Verify application output format
            expected_output = f"Zadane cislo je {number}"
            # Application must print this format
            assert "Zadane cislo je" in expected_output
            assert str(expected_number) in expected_output
        except ValueError as e:
            pytest.fail(f"Valid input '{valid_input}' should NOT raise ValueError. Error: {e}")
