from typing import List, Dict
from .function import PromptFunction, PROMPT_FUNCTION_SYSTEM_PROMPT
from .solver import FunctionSolverBase
from ..llm import GPT
from .utlis import parselist
from .func_dict_list import GAME_OF_24_FUNC_DICT_LIST

from loguru import logger
import datetime

# python -m accumulation_of_thoughts.prompt_function.gameof24


class GameOf24Solver(FunctionSolverBase):
    """
    Game of 24 solver (With Prmopt Function)

    Args:
        assistant (GPT): The assistant to help solve the problem
        batch_size (int): The batch size, which is limited by the max token length of the assistant
        functions_list (List[Dict]): list of functions dictionary
    """

    def __init__(
        self, assistant: GPT, batch_size: int = 5, functions_list: List[Dict] = None
    ):
        super().__init__()
        # super().load_function(functions)
        if functions_list:
            self.load_function(functions_list)

        else:
            raise ValueError("functions_list is required")
        # self.func: Dict[str, PromptFunction] = {}
        for f in self.functions:
            self.func[f.name] = f
        self.base_user_prompt = super().define_function()
        self.first_round_list = None
        self.second_round_list = None
        self.third_round_list = None
        self.question = (
            self.base_user_prompt
            + "**Question**:\n{q}\nWith the above function, output as required."
        )
        self.assistant = assistant
        self.batch_size = 5

    def solve(self, task: str = "3,3,8,8") -> str:
        """
        Solve the task
        """
        time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        logger.add(f"logs/game_of_24_{time}.log", rotation="1 day")
        logger.info("System Prompt:\n" + PROMPT_FUNCTION_SYSTEM_PROMPT)
        self.stage1(task)
        self.stage2()
        self.stage3()
        return self.result

    def stage1(self, task: str):
        """
        Solve the first stage
        """
        stage1_question = self.question.format(
            q=f"Compression(Choose2Numbers([{task}]))"
        )
        logger.success("#################### Stage 1 ####################")
        logger.info(stage1_question)
        response = self.assistant.get_response(
            system_prompt=PROMPT_FUNCTION_SYSTEM_PROMPT, user_prompt=stage1_question
        )
        logger.info("Response:\n" + response)
        self.first_round_list = parselist(
            self.func["Compression"].output_parse(response)
        )

    def stage2(self):
        """
        Solve the second stage
        """
        logger.success("#################### Stage 2 ####################")
        second_round_list = []
        for i in range(0, len(self.first_round_list), self.batch_size):
            task = """
```python
result = []
for each item in the {list}:
    result.extend(Compression(Choose2Numbers(item)))
output=result
```
""".format(
                list=self.first_round_list[i : i + self.batch_size]
            )
            stage2_question = self.question.format(q=task)
            logger.info(stage2_question)
            response = self.assistant.get_response(
                system_prompt=PROMPT_FUNCTION_SYSTEM_PROMPT, user_prompt=stage2_question
            )
            logger.info("Response:\n" + response)
            second_round_list.extend(self.func["Compression"].output_parse(response))
            self.second_round_list = second_round_list

    def stage3(self):
        """
        Solve the third stage
        """
        logger.success("#################### Stage 3 ####################")
        task = self.second_round_list
        stage3_question = self.question.format(q=f"parsefinalanswer(Evaluate({task}))")
        logger.info(stage3_question)
        response = self.assistant.get_response(
            system_prompt=PROMPT_FUNCTION_SYSTEM_PROMPT, user_prompt=stage3_question
        )
        logger.info("Response:\n" + response)
        self.result = self.func["Evaluate"].output_parse(response)


if __name__ == "__main__":
    api_key = "sk-Jp9YCIcVzEiwgIgg87F463EdC7F84992B8CcC4D6459d505a"
    model_id = "gpt-4o"
    assistant = GPT(api_key=api_key, model_id=model_id)
    solver = GameOf24Solver(
        assistant=assistant, functions_list=GAME_OF_24_FUNC_DICT_LIST
    )

    task = "3,3,8,8"
    solver.solve(task)

    # func_dict_list = [
    #     {
    #         "name": "Choose2Numbers",
    #         "input": ["A list of numbers and expressions"],
    #         "rule": [
    #             "The expressions in the input consist of numbers and the four regular operations.",
    #             "Select two items from the input list and combine them with one of the four operations.",
    #             """Example: input=[(1+2),3,4]
    #     Select two items:
    #         (1) select (1+2) and 3: [((1+2)+3),4],[((1+2)-3),4],[((1+2)*3),4],[((1+2)/3),4],[(3-(1+2)),4],[(3/(1+2)),4]
    #         (2) select (1+2) and 4: [((1+2)+4),3],[((1+2)-4),3],[((1+2)*4),3],[((1+2)/4),3],[(4-(1+2)),3],[(4/(1+2)),3]
    #         (3) select 3 and 4: [(1+2),(3+4)],[(1+2),(3-4)],[(1+2),(3*4)],[(1+2),(3/4)],[(1+2),(4-3)],[(1+2),(4/3)]
    #     -> output=[[((1+2)+3),4],[((1+2)-3),4],[((1+2)*3),4],[((1+2)/3),4],[(1+2),(3+4)],[(1+2),(3-4)],[(1+2),(3*4)],[(1+2),(3/4)]],[((1+2)+4),3],[((1+2)-4),3],[((1+2)*4),3],[((1+2)/4),3]]""",
    #             "Brackets are to be added outside the two selected items.Like:select (1+2) and 3, then output is [((1+2)+3),4] not [(1+2)+3,4]",
    #             "Do not open pre-existing brackets!",
    #             "The number of digits in the output should be the same as the number of digits in the input.",
    #             "Return all possible combinations of the two selected items and the four operations. No need to calculate the result.",
    #         ],
    #     },
    #     {
    #         "name": "EvaluateExpression",
    #         "input": ["the expression to evalute", "a list of numbers"],
    #         "rule": [
    #             'If the expression to evaluate does not fulfill the requirement "to use the numbers in the list, each number must be used only once", return False.',
    #             "Otherwise, evaluate the expression and if the result is 24, return True; otherwise, return False.",
    #             "Example: input=['((1+2)+3)',[1,2,3,4]] -> Because 4 is not used, so output=False",
    #             "Example: input=['((1+2)+3)',[1,2,3]] -> Because the result is 6, so output=False",
    #             "Example: input=['((1+2)+3+3)',[1,2,3]] -> Because 3 is used twice, but there is only one 3 in the list, so output=False",
    #             "Example: input=['(8/(3-(8/3)))',[3,8,3,8]] -> Because all numbers in the list are used exactly once and the result of the expression is 24, so output=True",
    #             "Guidelines: The expression in parentheses is evaluated first.",
    #         ],
    #     },
    #     {
    #         "name": "Compression",
    #         "input": ["A list of lists of numbers and expressions"],
    #         "rule": [
    #             "The input list consists of numbers and expressions.",
    #             "If there are same numbers and expressions in the list, remove the duplicates.",
    #             "Example: input=[[(9+5),5,5],[(9*5),5,5],[5,(9+5),5],[5,5,(5+9)]] -> output=[[(9+5),5,5],[(9*5),5,5]]",
    #             "Return the compressed list.",
    #         ],
    #     },
    #     {
    #         "name": "Evaluate",
    #         "input": [
    #             "A list in which each item contains a number and an expression consisting of three numbers"
    #         ],
    #         "rule": [
    #             "Initialize an empty list to store the results. Result=[]",
    #             "For each item in the list do the following:",
    #             "Firstly, Calulate the result of the expression, denoted as num2.",
    #             "Calulate (num1+num2), (num1-num2), (num1*num2), (num1/num2), (num2-num1),(num2/num1).",
    #             "If any of the results is 24, return corresponding expression; otherwise, return 'None'.",
    #             """Example:
    # input=[[6,(7+(12+10))],[12,(6/(10-7))],[10,(6*(12-7))]]
    # analysis:
    #     (1)[6,(7+(12+10))]: num1=6,num2=29, num1+num2=35, num1-num2=-23, num1*num2=174, num1/num2=0.2069, num2-num1=23, num2/num1=4.8333, none of the results is 24, Result.append(None);
    #     (2)[12,(6/(10-7))]: num1=12,num2=2, num1+num2=14, num1-num2=10, num1*num2=24, num1/num2=6, num2-num1=-10, num2/num1=0.1667, the result of (num1*num2) is 24, Result.append((12*(6/(10-7))));
    #     (3)[10,(6*(12-7))]: num1=10,num2=30, num1+num2=40, num1-num2=-20, num1*num2=300, num1/num2=0.3333, num2-num1=20, num2/num1=3, none of the results is 24, Result.append(None);
    # output=[None, (12*(6/(10-7))), None]""",
    #         ],
    #     },
    #     {
    #         "name": "parsefinalanswer",
    #         "input": ["A list in which each item is either an expression or None"],
    #         "rule": [
    #             "Find the item in the list that is not None and return it",
    #         ],
    #     },
    # ]


#     system_prompt = PROMPT_FUNCTION_SYSTEM_PROMPT
#     user_prompt = solver.solve()

#     FirstRoundList = """[[(3+8),3,8], [(3-8),3,8], [(3*8),3,8], [(3/8),3,8], [(8+3),3,8], [(8-3),3,8], [(8*3),3,8], [(8/3),3,8], [(3+3),8,8], [(3-3),8,8], [(3*3),8,8], [(3/3),8,8]]"""

#     # user_prompt += (
#     #     "\n"
#     #     + "**Question**:\n"
#     #     + "Compression(Choose2Numbers([5,9,9,9]))"
#     #     + "\nWith the above function, output as required."
#     # )
#     question = (
#         user_prompt
#         + """
# **Question**:
# {q}
# With the above function, output as required.
#     """
#     )
#     print(user_prompt)

#     time = datetime.datetime.now().strftime("%Y-%m-%d")
#     logger.remove()
#     logger.add(f"logs/{time}.log", rotation="1 day")
#     logger.info("System Prompt:\n" + system_prompt)
#     logger.info("User Prompt:\n" + user_prompt)

#     api_key = "sk-Jp9YCIcVzEiwgIgg87F463EdC7F84992B8CcC4D6459d505a"
#     model_id = "gpt-4o"
#     gpt = GPT(api_key=api_key, model_id=model_id)

#     # response = gpt.get_response(system_prompt=system_prompt, user_prompt=user_prompt)
#     # logger.info("Response:\n" + response)
#     # print(response)

#     # Stage 1: Get the first round list
#     first_round_list = None
#     task = "3,3,8,8"
#     stage1_question = question.format(q=f"Compression(Choose2Numbers([{task}]))")
#     logger.success("#################### Stage 1 ####################")
#     logger.info(stage1_question)
#     response = gpt.get_response(
#         system_prompt=system_prompt, user_prompt=stage1_question
#     )
#     logger.info("Response:\n" + response)
#     #     response = """
#     # 1. function Choose2Numbers(input:[3,3,8,8])
#     # -> output: [[(3+3),8,8],[(3-3),8,8],[(3*3),8,8],[(3/3),8,8],[(3+8),3,8],[(3-8),3,8],[(3*8),3,8],[(3/8),3,8],[(3+8),3,8],[(3-8),3,8],[(3*8),3,8],[(3/8),3,8],[(8+8),3,3],[(8-8),3,3],[(8*8),3,3],[(8/8),3,3]]

#     # 2. function Compression(input:[[(3+3),8,8],[(3-3),8,8],[(3*3),8,8],[(3/3),8,8],[(3+8),3,8],[(3-8),3,8],[(3*8),3,8],[(3/8),3,8],[(3+8),3,8],[(3-8),3,8],[(3*8),3,8],[(3/8),3,8],[(8+8),3,3],[(8-8),3,3],[(8*8),3,3],[(8/8),3,3]])
#     # -> output: [[(3+3),8,8],[(3-3),8,8],[(3*3),8,8],[(3/3),8,8],[(3+8),3,8],[(3-8),3,8],[(3*8),3,8],[(3/8),3,8],[(8+8),3,3],[(8-8),3,3],[(8*8),3,3],[(8/8),3,3]]
#     # """
#     first_round_list = solver.func["Compression"].output_parse(response)

#     # Stage 2: Get the second round list
#     second_round_list = []
#     batch_size = 5
#     for i in range(0, len(first_round_list), batch_size):
#         task = """
# ```
# result = []
# for each item in the {list}:
#     result.extend(Compression(Choose2Numbers(item)))
# ```
# """.format(
#             list=first_round_list[i : i + batch_size]
#         )
#         stage2_question = question.format(q=task)
#         logger.success("#################### Stage 2 ####################")
#         logger.info(stage2_question)
#         response = gpt.get_response(
#             system_prompt=system_prompt, user_prompt=stage2_question
#         )
#         logger.info("Response:\n" + response)
#         second_round_list.extend(solver.func["Compression"].output_parse(response))

#     # Stage 3: Get the third round list
#     third_round_list = []
#     for item in second_round_list:
#         task = item
#         stage3_question = question.format(
#             q=f"EvaluateExpression(Choose2Numbers({task}))"
#         )
#         logger.success("#################### Stage 3 ####################")
#         logger.info(stage3_question)
#         response = gpt.get_response(
#             system_prompt=system_prompt, user_prompt=stage3_question
#         )
#         logger.info("Response:\n" + response)
#         third_round_list.extend(
#             solver.func["EvaluateExpression"].output_parse(response)
#         )
