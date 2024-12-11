from collections import deque


operators = [ "+", "*", "||" ]


def yield_lines(file_path: str):
    with open(file_path, 'r') as filestream:
        for line in filestream:
            yield line.strip('\n')

def create_rpn_formulas(next_numbers, previous_formula=[]):
    if previous_formula == []:
        formula = [next_numbers[0]]
        next_numbers = next_numbers.copy()
        del next_numbers[0]

        return create_rpn_formulas(next_numbers, formula)

    formulas = []
    for op in operators:
        formula = previous_formula.copy()
        formula.append(next_numbers[0])
        formula.append(op)
        formulas.append(formula)

    next_numbers = next_numbers.copy()
    del next_numbers[0]

    if len(next_numbers) > 0:
        next_formulas = []
        for formula in formulas:
            next_formulas += create_rpn_formulas(next_numbers, formula)
        
        return next_formulas

    return formulas

def eval_rpn(formula):
    stack = deque(formula)
    while len(stack) > 1:
        a, b, c = stack.popleft(), stack.popleft(), stack.popleft()
        
        if c == "+":
            result = a + b
        elif c == "*":
            result = a * b
        elif c == "||":
            result = int(str(a) + str(b))
        
        stack.appendleft(result)
    return stack[0]


def main():
    solution = 0

    for line in yield_lines("2024/day7/input"):
        test_val, numbers = line.split(": ")
        test_val = int(test_val)
        numbers = list(int(num) for num in numbers.split(" "))

        formulas = create_rpn_formulas(numbers)
        results = (eval_rpn(formula) for formula in formulas)
        if test_val in results:
            solution += test_val

    print(solution)


main()