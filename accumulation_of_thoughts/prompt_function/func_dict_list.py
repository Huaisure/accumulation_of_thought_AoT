GAME_OF_24_FUNC_DICT_LIST = [
    {
        "name": "Choose2Numbers",
        "input": ["A list of numbers and expressions"],
        "rule": [
            "The expressions in the input consist of numbers and the four regular operations.",
            "Select two items from the input list and combine them with one of the four operations.",
            """Example: input=[(1+2),3,4]
        Select two items:
            (1) select (1+2) and 3: [((1+2)+3),4],[((1+2)-3),4],[((1+2)*3),4],[((1+2)/3),4],[(3-(1+2)),4],[(3/(1+2)),4]
            (2) select (1+2) and 4: [((1+2)+4),3],[((1+2)-4),3],[((1+2)*4),3],[((1+2)/4),3],[(4-(1+2)),3],[(4/(1+2)),3]
            (3) select 3 and 4: [(1+2),(3+4)],[(1+2),(3-4)],[(1+2),(3*4)],[(1+2),(3/4)],[(1+2),(4-3)],[(1+2),(4/3)]
        -> output=[[((1+2)+3),4],[((1+2)-3),4],[((1+2)*3),4],[((1+2)/3),4],[(1+2),(3+4)],[(1+2),(3-4)],[(1+2),(3*4)],[(1+2),(3/4)]],[((1+2)+4),3],[((1+2)-4),3],[((1+2)*4),3],[((1+2)/4),3]]""",
            "Brackets are to be added outside the two selected items.Like:select (1+2) and 3, then output is [((1+2)+3),4] not [(1+2)+3,4]",
            "Do not open pre-existing brackets!",
            "The number of digits in the output should be the same as the number of digits in the input.",
            "Return all possible combinations of the two selected items and the four operations. No need to calculate the result.",
        ],
    },
    {
        "name": "EvaluateExpression",
        "input": ["the expression to evalute", "a list of numbers"],
        "rule": [
            'If the expression to evaluate does not fulfill the requirement "to use the numbers in the list, each number must be used only once", return False.',
            "Otherwise, evaluate the expression and if the result is 24, return True; otherwise, return False.",
            "Example: input=['((1+2)+3)',[1,2,3,4]] -> Because 4 is not used, so output=False",
            "Example: input=['((1+2)+3)',[1,2,3]] -> Because the result is 6, so output=False",
            "Example: input=['((1+2)+3+3)',[1,2,3]] -> Because 3 is used twice, but there is only one 3 in the list, so output=False",
            "Example: input=['(8/(3-(8/3)))',[3,8,3,8]] -> Because all numbers in the list are used exactly once and the result of the expression is 24, so output=True",
            "Guidelines: The expression in parentheses is evaluated first.",
        ],
    },
    {
        "name": "Compression",
        "input": ["A list of lists of numbers and expressions"],
        "rule": [
            "The input list consists of numbers and expressions.",
            "If there are same numbers and expressions in the list, remove the duplicates.",
            "Example: input=[[(9+5),5,5],[(9*5),5,5],[5,(9+5),5],[5,5,(5+9)]] -> output=[[(9+5),5,5],[(9*5),5,5]]",
            "Return the compressed list.",
        ],
    },
    {
        "name": "Evaluate",
        "input": [
            "A list in which each item contains a number and an expression consisting of three numbers"
        ],
        "rule": [
            "Initialize an empty list to store the results. Result=[]",
            "For each item in the list do the following:",
            "Firstly, Calulate the result of the expression, denoted as num2.",
            "Calulate (num1+num2), (num1-num2), (num1*num2), (num1/num2), (num2-num1),(num2/num1).",
            "If any of the results is 24, return corresponding expression; otherwise, return 'None'.",
            """Example:
    input=[[6,(7+(12+10))],[12,(6/(10-7))],[10,(6*(12-7))]]
    analysis:
        (1)[6,(7+(12+10))]: num1=6,num2=29, num1+num2=35, num1-num2=-23, num1*num2=174, num1/num2=0.2069, num2-num1=23, num2/num1=4.8333, none of the results is 24, Result.append(None);
        (2)[12,(6/(10-7))]: num1=12,num2=2, num1+num2=14, num1-num2=10, num1*num2=24, num1/num2=6, num2-num1=-10, num2/num1=0.1667, the result of (num1*num2) is 24, Result.append((12*(6/(10-7))));
        (3)[10,(6*(12-7))]: num1=10,num2=30, num1+num2=40, num1-num2=-20, num1*num2=300, num1/num2=0.3333, num2-num1=20, num2/num1=3, none of the results is 24, Result.append(None);
    output=[None, (12*(6/(10-7))), None]""",
        ],
    },
    {
        "name": "parsefinalanswer",
        "input": ["A list in which each item is either an expression or None"],
        "rule": [
            "Find the item in the list that is not None and return it",
        ],
    },
]
