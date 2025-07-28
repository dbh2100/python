"""This module defines functions that replicate Python's builtin eval()"""

import re


# Regular expression patterns
PARENTHESIS_RE = re.compile(r'\( [^()]* \)', flags=re.VERBOSE)
NUMBER_PATTERN = r'-? \d+ ([.]\d*)?'
MULT_DIV_RE = re.compile(
    rf'({NUMBER_PATTERN}) \s* ([*/]) \s* ({NUMBER_PATTERN})', flags=re.VERBOSE)
ADD_SUB_RE = re.compile(
    rf'({NUMBER_PATTERN}) \s* ([+-]) \s* ({NUMBER_PATTERN})', flags=re.VERBOSE
)


def _evaluate_binary(match_obj):

    # Group 2 is the decimal point and following digits, or none
    num1_str, num2_str = map(match_obj.group, (1, 4))
    num1 = float(num1_str) if '.' in num1_str else int(num1_str)
    num2 = float(num2_str) if '.' in num2_str else int(num2_str)
    op = match_obj.group(3)

    if op == '+':
        return str(num1 + num2)

    if op == '-':
        return str(num1 - num2)

    if op == '*':
        return str(num1 * num2)

    if op == '/':
        return str(num1 / num2)

    raise ValueError('Invalid operator')


def evaluate_equation_regex(equation):
    """Evaluate a mathematical equation using regular expressions"""

    # If used recursively, argument would be regex match object
    # so convert to string and remove leading and trailing parentheses
    return_string = False
    if isinstance(equation, re.Match):
        equation = equation.group(0).removeprefix('(').removesuffix(')')
        return_string = True

    # Evaluate all parenthetical components
    while PARENTHESIS_RE.search(equation):
        equation = PARENTHESIS_RE.sub(evaluate_equation_regex, equation)

    # Multiplication and divison have order precedence
    while MULT_DIV_RE.search(equation):
        equation = MULT_DIV_RE.sub(_evaluate_binary, equation)

    # Now execute addition and subtraction
    while ADD_SUB_RE.search(equation):
        equation = ADD_SUB_RE.sub(_evaluate_binary, equation)

    # If function called recursively, keep number as string
    if return_string:
        return equation

    # Otherwise, return number in appropriate format
    return float(equation) if '.' in equation else int(equation)


def evaluate_equation(equation):
    """Evaluate a mathematical equation just using Python builtins"""
    equation = equation.strip()

    # Account for equation beginning with negative number
    if equation == '':
        return 0

    if '.' in equation and equation.replace('.', '').isnumeric():
        return float(equation)
    if equation.isnumeric():
        return int(equation)

    # If the equation ends in a parenthetical statement,
    # evaluate the right-most inner parenthetical statement (middle_part)
    # evaluate_equation(middle_part) could be negative
    if equation.endswith(')'):
        left_part, right_part = equation.rsplit('(', 1)
        middle_part, right_part = right_part.split(')', 1)
        new_equation = left_part + str(evaluate_equation(middle_part)) + right_part
        return evaluate_equation(new_equation)

    plus_index, minus_index, mul_index, div_index, par_end_index = map(equation.rfind, '+-*/)')

    # If a plus or minus sign exists after the last parenthetical statement,
    # use it as the operator because multiplication and division are more tightly-bound
    if (max_plus_minus_index := max(plus_index, minus_index)) > par_end_index:
        index = max_plus_minus_index
    else:
        index = max(mul_index, div_index)
    op = equation[index]

    # Account for negative intermediate value
    right_factor = 1
    if op == '-':
        index -= 1
        while equation[index] not in '+-*/' and not equation[index].isnumeric():
            index -= 1
        if equation[index] in '+-*/':
            right_factor = -1
            minus_index = equation.rfind('-', minus_index)
            if (max_plus_minus_index := max(plus_index, minus_index)) > par_end_index:
                index = max_plus_minus_index
            else:
                index = max(mul_index, div_index)
            op = equation[index]

    # Split the equation into left and right parts based on the operator
    left_part, right_part = equation.rsplit(op, 1)

    if op == '+':
        return evaluate_equation(left_part) + right_factor*evaluate_equation(right_part)
    if op == '-':
        return evaluate_equation(left_part) - right_factor*evaluate_equation(right_part)
    if op == '*':
        return evaluate_equation(left_part) * right_factor*evaluate_equation(right_part)
    if op == '/':
        return evaluate_equation(left_part) / right_factor*evaluate_equation(right_part)

    return None


if __name__ == '__main__':

    print('Starting evaluate.py tests...')

    test_equations = [
        '3 - 4',
        '-2 + 7',
        '3 - 4 + 8',
        '3 - (4 + 8)',
        '3 - 10 * (4 + 8)',
        '(7 + 6 * 10) - 3 * 2 * (4 + 8)',
        '100 - (3 - 10 * (4 + 8))',
    ]

    for eq in test_equations:
        try:
            assert evaluate_equation(eq) == eval(eq)
            assert evaluate_equation_regex(eq) == eval(eq)
        except AssertionError:
            print(f'Incorrect return for equation: {eq}')
            print(f'evaluate_equation: {evaluate_equation(eq)}')
            print(f'evaluate_equation_regex: {evaluate_equation_regex(eq)}')
            print(f'Expected: {eval(eq)}')
            raise

    # Test equation with floating-point numbers
    FLOAT_EQUATION = '3.2 - 10 * (4.9 + 8.5)'
    assert evaluate_equation(FLOAT_EQUATION) == eval(FLOAT_EQUATION)
    assert evaluate_equation_regex(FLOAT_EQUATION) == eval(FLOAT_EQUATION)

    print('All evaluate.py tests pass')
