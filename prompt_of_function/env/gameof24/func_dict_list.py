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
        -> output: [[((1+2)+3),4],[((1+2)-3),4],[((1+2)*3),4],[((1+2)/3),4],[(3-(1+2)),4],[3/(1+2),4],[((1+2)+4),3],[((1+2)-4),3],[((1+2)*4),3],[((1+2)/4),3],[(4-(1+2)),3],[(4/(1+2)),3],[(1+2),(3+4)],[(1+2),(3-4)],[(1+2),(3*4)],[(1+2),(3/4)],[(1+2),(4-3)],[(1+2),(4/3)]]""",
            """Guidelines:
        - Add parentheses to the expression formed by the two selected terms, e.g., select (1+2) and 3, then output is [((1+2)+3),4] not [(1+2)+3,4],
        - Treat the contents of the brackets as a whole and do not break them apart""",
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
            "Remove the duplicates in the input list.",
            "Fistly, caculate the result of the expressions in each item.",
            "Secondly, if two items have exactly the same number (order is irrelevant), remove the duplicate and reserve one of them.",
            """Example: input=[[(9+5),5,5],[(2*7),5,5],[(9-5),5,5],[(5+9),14,5]]
            (1) [(9+5),5,5] is [14,5,5]. The composition of numbers is {'14':1,'5':2}.
            (2) [5,(2*7),5] is [5,14,5]. The composition of numbers is {'14':1,'5':2}.
            (3) [(9-5),5,5] is [4,5,5]. The composition of numbers is {'4':1,'5':2}.
            (4) [(5+9),14,5] is [14,5,5]. The composition of numbers is {'14':2,'5':1}.
            The two items [(9+5),5,5] and [5,(2*7),5] have the same composition of numbers, so remove the duplicate. And other items are different from each other.
            -> output: [[(9+5),5,5],[(9-5),5,5],[(5+9),14,5]]""",
            "Carefully check the composition of numbers in each item.",
        ],
        #     "The input list consists of numbers and expressions.",
        #     "Firstly, caculate the result of the expressions in each item.",
        #     "If two items have exactly the same number (order is irrelevant), remove the duplicate.",
        #     """Example:input=[[(9+5),5,5],[(9*5),5,5],[5,(9+5),5],[5,5,(5+9)],[5,5,(2*7)]]
        # intermeidiate step:
        #     (1) Calculate the result of the expression in each item: [[14,5,5],[45,5,5],[5,14,5],[5,5,14],[5,5,14]]
        #     (2) Remove the duplicate: [14,5,5] and [5,14,5] and [5,5,14] and [5,5,14] have the composition of identical numbers, so remove the duplicates. and return the corresponding item in the original list.
        # -> output=[[(9+5),5,5],[(9*5),5,5]]""",
        #     "Make sure the items in the output list are the same as the corresponding items in the input list.",
        #     "Return the compressed list.",
        # ],
    },
    {
        "name": "Evaluate",
        "input": ["A list that each item is a list of numbers or expressions"],
        "rule": [
            "For each item in the input list: Evaluate24(item) -> output: [expression or None]",
            "Synthesise all the output, returning the [expression] if it exists, or [None] if all the results are None.",
            """Example:
        1) input=[[6,(7+(12+10))],[12,(6/(10-7))],[10,(6*(12-7))]]
        For each item:
            (1) Evaluate24([6,(7+(12+10))]) -> output: [None]
            (2) Evaluate24([12,(6/(10-7))]) -> output: [(12*(6/(10-7)))]
            (3) Evaluate24([10,(6*(12-7))]) -> output: [None]
        -> output: [(12*(6/(10-7)))]

        2) input=[[3,(3+(8+8))],[(8-8),(3*3)]]
        For each item:
            (1) Evaluate24([3,(3+(8+8))]) -> output: [None]
            (2) Evaluate24([(8-8),(3*3)]) -> output: [None]
        -> output: [None]""",
        ],
    },
    {
        "name": "Evaluate24",
        "input": ["A list that contains numbers or expressions"],
        "rule": [
            "The input list is like: [(a op (b op c)),d] or [(a op b), (c op d)], denote the two expressions as [exp1, exp2]",
            "For each item in the list do the following:",
            "Choose2Numbers(item) -> output: [six expressions]",
            "For each expression in [six expressions], evaluate the expressions and if one ot them the result is 24, return the corresponding [expression], otherwise return [None].",
            """Example:
        input=[[6,(7+(12+10))],[12,(6/(10-7))],[10,(6*(12-7))]]
        analysis:
            (1) Choose2Numbers([6,(7+(12+10))]) -> output: [[(6+(7+(12+10))),[(6-(7+(12+10)))],[(6*(7+(12+10)))],[(6/(7+(12+10)))],[((7+(12+10))-6)],[((7+(12+10))/6)]]
                exp1: 6:6; exp1=6
                exp2: (7+(12+10)): 12+10=22, 7+22=29; exp2=29
                for each expression in [six expressions]:
                    [(6+(7+(12+10)))]: exp1+exp2=6+29=35, 35 != 24
                    [(6-(7+(12+10)))]: exp1-exp2=6-29=-23, -23 != 24
                    [(6*(7+(12+10)))]: exp1*exp2=6*29=174, 174 != 24
                    [(6/(7+(12+10)))]: exp1/exp2=6/29=0.20689655172413793, 0.20689655172413793 != 24
                    [((7+(12+10))-6)]: exp2-exp1=29-6=23, 23 != 24
                    [((7+(12+10))/6)]: exp2/exp1=29/6=4.833333333333333, 4.833333333333333 != 24
                -> output: [None]
            (2) Choose2Numbers([12,(6/(10-7))]) -> output: [[(12+(6/(10-7)))],[(12-(6/(10-7)))],[(12*(6/(10-7)))],[(12/(6/(10-7)))],[((6/(10-7))-12)],[((6/(10-7))/12)]]
                exp1: 12:12; exp1=12
                exp2: (6/(10-7)): 10-7=3, 6/3=2; exp2=2
                for each expression in [six expressions]:
                    [(12+(6/(10-7)))]: exp1+exp2=12+2=14, 14 != 24
                    [(12-(6/(10-7)))]: exp1-exp2=12-2=10, 10 != 24
                    [(12*(6/(10-7)))]: exp1*exp2=12*2=24, 24 == 24
                -> output: [[(12*(6/(10-7)))]]
            Because there has been a result that is 24, so return the corresponding expression.
        ->output: [(12*(6/(10-7)))]

        input=[[3,(3+(8+8))],[(8-8),(3*3)]]
        analysis:
            (1) Choose2Numbers([3,(3+(8+8))]) -> output: [[(3+(3+(8+8)))],[(3-(3+(8+8)))],[(3*(3+(8+8)))],[(3/(3+(8+8)))],[((3+(8+8))-3)],[((3+(8+8))/3)]]
                exp1: 3:3; exp1=3
                exp2: (3+(8+8)): 8+8=16, 3+16=19; exp2=19
                for each expression in [six expressions]:
                    [(3+(3+(8+8)))]: exp1+exp2=3+19=22, 22 != 24
                    [(3-(3+(8+8)))]: exp1-exp2=3-19=-16, -16 != 24
                    [(3*(3+(8+8)))]: exp1*exp2=3*19=57, 57 != 24
                    [(3/(3+(8+8)))]: exp1/exp2=3/19=0.15789473684210525, 0.15789473684210525 != 24
                    [((3+(8+8))-3)]: exp2-exp1=19-3=16, 16 != 24
                    [((3+(8+8))/3)]: exp2/exp1=19/3=6.333333333333333, 6.333333333333333 != 24
                -> output: [None]
            (2) Choose2Numbers([(8-8),(3*3)]) -> output: [[((8-8)+(3*3))],[((8-8)-(3*3))],[((8-8)*(3*3))],[((8-8)/(3*3))],[((3*3)-(8-8))],[((3*3)/(8-8))]]
                exp1: (8-8):0; exp1=0
                exp2: (3*3):3*3=9; exp2=9
                for each expression in [six expressions]:
                    [((8-8)+(3*3))]: exp1+exp2=0+9=9, 9 != 24
                    [((8-8)-(3*3))]: exp1-exp2=0-9=-9, -9 != 24
                    [((8-8)*(3*3))]: exp1*exp2=0*9=0, 0 != 24
                    [((8-8)/(3*3))]: exp1/exp2=0/9=0.0, 0.0 != 24
                    [((3*3)-(8-8))]: exp2-exp1=9-0=9, 9 != 24
                    [((3*3)/(8-8))]: exp2/exp1=9/0=inf, inf != 24
                -> output: [None]
            Because there is no result that is 24, so return None.
        ->output: [None]""",
            "Guidelines: Be sure to pay attention to the accuracy of your calculations! Please give priority to calculating the expression in parentheses.",
        ],
    },
    {
        "name": "parsefinalanswer",
        "input": ["A list in which each item is either an expression or None"],
        "rule": [
            "Find the item in the list that is not None and return it",
            "Example: input=[None, (12*(6/(10-7))), None] -> output=(12*(6/(10-7)))",
            "If all items are None, return 'None'.",
        ],
    },
    {
        "name": "Choose2NumbersForEachItem",
        "input": ["A list of lists of numbers and expressions"],
        "rule": [
            "result = []",
            "Function Choose2Numbers() is defined above.",
            "For each item in the input list, result.extend(Choose2Numbers(item))",
            """Example: input=[[(1+2),3,4],[(1-2),3,4]]
        For each item:
            (1) Choose2Numbers([(1+2),3,4]) -> output: [[((1+2)+3),4],[((1+2)-3),4],[((1+2)*3),4],[((1+2)/3),4],[(3-(1+2)),4],[(3/(1+2)),4],[(1+2),(3+4)],[(1+2),(3-4)],[(1+2),(3*4)],[(1+2),(3/4)]],[(1+2),(4-3)],[(1+2),(4/3)],[(1+2)+4,3],[((1+2)-4),3],[((1+2)*4),3],[((1+2)/4),3],[(4-(1+2)),3],[(4/(1+2)),3]]
            (2) Choose2Numbers([(1-2),3,4]) -> output: [[((1-2)+3),4],[((1-2)-3),4],[((1-2)*3),4],[((1-2)/3),4],[(3-(1-2)),4],[(3/(1-2)),4],[(1-2),(3+4)],[(1-2),(3-4)],[(1-2),(3*4)],[(1-2),(3/4)]],[(1-2),(4-3)],[(1-2),(4/3)],[(1-2)+4,3],[((1-2)-4),3],[((1-2)*4),3],[((1-2)/4),3],[(4-(1-2)),3],[(4/(1-2)),3]
        -> output: [[((1+2)+3),4],[((1+2)-3),4],[((1+2)*3),4],[((1+2)/3),4],[(3-(1+2)),4],[(3/(1+2)),4],[(1+2),(3+4)],[(1+2),(3-4)],[(1+2),(3*4)],[(1+2),(3/4)]],[(1+2),(4-3)],[(1+2),(4/3)],[(1+2)+4,3],[((1+2)-4),3],[((1+2)*4),3],[((1+2)/4),3],[(4-(1+2)),3],[(4/(1+2)),3],[((1-2)+3),4],[((1-2)-3),4],[((1-2)*3),4],[((1-2)/3),4],[(3-(1-2)),4],[(3/(1-2)),4],[(1-2),(3+4)],[(1-2),(3-4)],[(1-2),(3*4)],[(1-2),(3/4)]],[(1-2),(4-3)],[(1-2),(4/3)],[(1-2)+4,3],[((1-2)-4),3],[((1-2)*4),3],[((1-2)/4),3],[(4-(1-2)),3],[(4/(1-2)),3]]""",
        ],
    },
]
