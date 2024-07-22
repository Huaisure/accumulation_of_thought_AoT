gameof24 = {
    "Description": "The goal is to use four given numbers to make the number 24 using basic arithmetic operations: addition, subtraction, multiplication, and division. Each of the numbers must be used exactly once.",
    "Constraints": [
        "Usage of Numbers: All four given numbers must be used exactly once in the solution.",
        "Allowed Operations: You can only use the basic arithmetic operations: addition (+), subtraction (-), multiplication (x), and division (÷).",
        "Combination: Numbers can be combined in any order using parentheses to structure the operations as needed.",
        "Result: The final result of the operations must be exactly 24.",
        "No Repetition of Numbers: Each number must be used only once in the expression.",
        "Intermediate Results: All intermediate results must be valid and must not involve division by zero or any undefined operations.",
    ],
    "Format": 'The final answer should be presented in the format: "Final Answer: <expression with 4 given numbers and operations>"',
    "Method": {
        "Have Code": True,
        "Flow": [
            "Generate Permutations: Generate all possible permutations of the four given numbers. Since there are four numbers, there will be 4!=24 permutations.",
            "Generate Operator Combinations: Generate all possible combinations of three operators (addition, subtraction, multiplication, division) since you need three operations to combine four numbers.",
            "Generate Parentheses Combinations: Generate all valid ways to insert parentheses to define the order of operations. This includes considering all valid expressions such as (a⋅(b⋅(c⋅d))), (a⋅b)⋅(c⋅d), etc.",
            "Evaluate Expressions: Evaluate each generated expression. If an expression evaluates to 24, return it as a solution.",
        ],
        "Code": """
function solveGameOf24(numbers):
    permutations = generatePermutations(numbers)
    operators = ['+', '-', '*', '/']
    operatorCombinations = generateOperatorCombinations(operators, 3)
    parenthesesCombinations = generateParenthesesCombinations()

    for perm in permutations:
        for opCombo in operatorCombinations:
            for parens in parenthesesCombinations:
                expression = createExpression(perm, opCombo, parens)
                if evaluateExpression(expression) == 24:
                    return "Final Answer: " + expression
    return "No solution found"

function generatePermutations(numbers):
    // Returns all permutations of the list `numbers`

function generateOperatorCombinations(operators, length):
    // Returns all combinations of `length` operators from `operators`

function generateParenthesesCombinations():
    // Returns all valid parentheses combinations for expressions of four numbers and three operators

function createExpression(perm, opCombo, parens):
    // Creates an expression string from a permutation of numbers, a combination of operators, and a parentheses structure

function evaluateExpression(expression):
    // Evaluates the expression string and returns the result
""",
        "Code Explanation": [
            "generatePermutations: This function generates all possible ways to arrange the four numbers.",
            "generateOperatorCombinations: This function generates all possible combinations of three operators.",
            "generateParenthesesCombinations: This function generates all valid ways to insert parentheses into an expression involving four numbers and three operators.",
            "createExpression: This function constructs an expression string from a given permutation of numbers, combination of operators, and parentheses structure.",
            "evaluateExpression: This function evaluates the constructed expression to check if it equals 24.",
        ],
        "Category": "Mathematical Reasoning",
    },
}
