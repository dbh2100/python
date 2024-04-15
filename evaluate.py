"""This module defines a function that replicates Python's builtin eval()"""

import re

# Regular expression patterns
PARENTHESIS_RE = re.compile(r'\( [^()]* \)', flags=re.VERBOSE)
MULT_DIV_RE = re.compile(r'(-?\d+) \s* ([*/]) \s* (-?\d+)', flags=re.VERBOSE)
ADD_SUB_RE = re.compile(r'(-?\d+) \s* ([+-]) \s* (-?\d+)', flags=re.VERBOSE)


def _evaluate_binary(match_obj):

    num1 = int(match_obj.group(1))
    op = match_obj.group(2)
    num2 = int(match_obj.group(3))

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
    """Evaluate an equation of integers using regular expressions"""

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

    return equation if return_string else int(equation)


def evaluate_equation(equation):
    """Evaluate an equation of integers just using builtins"""

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

    print('All tests pass')
