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

    if '.' in equation and equation.replace('.', '').isnumeric():
        return float(equation)
    if equation.isnumeric():
        return int(equation)

    # First remove leading and trailing parentheses
    rev = reversed(equation.rstrip())

    # The transition will be the operator (+, -, *,  or /)
    second_part = []
    transition = []

    # Encapsulate an ending parenthetical equation  
    nesting = 0
    for char in rev:
        if char == ')':
            nesting += 1
        if char == '(':
            nesting -= 1
        if not nesting and not char.isnumeric():
            if char == '(':
                second_part.append(char)
            else:
                transition.append(char)
            break
        second_part.append(char)

    # Multiplication and division have higher priority,
    # So find next plus or minus sign first
    if not char in '+-':
        for char in rev:
            if char in '+-)':
                break
            transition.append(char)
    if char in '+-':
        op = char
        first_part = list(rev)
        second_part.extend(transition[:-1])
    else:
        op = None

    # If there is no plus or minus sign between end of first part and
    # beginning of second part, find multiplicaton or division sign
    if not op:
        first_part = []
        for char in transition:
            if char in '*/' and not op:
                op = char
                continue
            if not op:
                second_part.append(char)
            else:
                first_part.append(char)
        first_part.extend(rev)

    first_part = ''.join(reversed(first_part)).strip()
    second_part = ''.join(reversed(second_part)).strip()
    if second_part[0] == '(':
        second_part = second_part[1:-1]

    # If entire equation in parentheses
    if not first_part:
        return evaluate_equation(second_part)

    if op == '+':
        return evaluate_equation(first_part) + evaluate_equation(second_part)
    if op == '-':
        return evaluate_equation(first_part) - evaluate_equation(second_part)
    if op == '*':
        return evaluate_equation(first_part) * evaluate_equation(second_part)
    if op == '/':
        return evaluate_equation(first_part) / evaluate_equation(second_part)

    return None


if __name__ == '__main__':

    test_equations = [
        '3 - 4',
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
    float_eq = '3.2 - 10 * (4.9 + 8.5)'
    assert evaluate_equation(float_eq) == eval(float_eq)
    assert evaluate_equation_regex(float_eq) == eval(float_eq)

    print('All tests pass')
