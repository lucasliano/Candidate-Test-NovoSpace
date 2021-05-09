import pytest

import main     # Runs the main program


def test_verilog():
    '''
    Test Description
    ------------------
    Checks if the output verilog file is the same as the expected. Both were generated with the testcase.v file.

    '''

    input = ""
    expected = ""
    try:
        input_file = open("output.v","r")
        input = input_file.read()
    except Exception as e:
        print("Error while reading input verilog file: " + e)
    finally:
        input_file.close()

    try:
        expected_file = open("expected/expected.v","r")
        expected = expected_file.read()
    except Exception as e:
        print("Error while reading expected verilog file: " + e)
    finally:
        expected_file.close()

    assert input == expected

def test_mem_file():
    '''
    Test Description
    ------------------
    Checks if the output memory map file is the same as the expected. Both were generated with the testcase.v file.

    '''

    input = ""
    expected = ""
    try:
        input_file = open("memdump0.mem","r")
        input = input_file.read()
    except Exception as e:
        print("Error while reading input verilog file: " + e)
    finally:
        input_file.close()

    try:
        expected_file = open("expected/memdump0.mem","r")
        expected = expected_file.read()
    except Exception as e:
        print("Error while reading expected verilog file: " + e)
    finally:
        expected_file.close()

    assert input == expected
