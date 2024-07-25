from .function import PROMPT_FUNCTION_SYSTEM_PROMPT
from .func_dict_list import GAME_OF_24_FUNC_DICT_LIST
from .solver import FunctionSolverBase
from ..llm import GPT
from .utlis import parselist

from typing import List, Dict
from loguru import logger
import datetime

# python -m accumulation_of_thoughts.prompt_function.gameof24


class GameOf24Solver(FunctionSolverBase):
    """
    Game of 24 solver (With Prmopt Function)

    Args:
        assistant (class: GPT): The assistant to help solve the problem
        batch_size (int): The batch size, which is limited by the max token length of the assistant
        functions_list (List[Dict]): list of functions dictionary
    """

    def __init__(
        self, assistant: GPT, batch_size: int = 6, functions_list: List[Dict] = None
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
        self.base_user_prompt = super().define_function_all()
        self.first_round_list = None
        self.second_round_list = None
        self.third_round_list = None
        self.question = (
            self.base_user_prompt
            + "**Question**:\n{q}\nWith the above function, output as required."
        )
        self.assistant = assistant
        self.batch_size = batch_size

    def solve(self, task: str = "3,3,8,8") -> str:
        """
        Solve the task
        """
        self.task = task
        time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        logger.add(f"logs/game_of_24_{time}.log", rotation="1 day")
        logger.info("System Prompt:\n" + PROMPT_FUNCTION_SYSTEM_PROMPT)
        self.stage1()
        self.stage2()
        self.stage3()
        return self.result

    def stage1(self):
        """
        Solve the first stage\n
        choose 2 numbers from the input list, and combine them with one of the four operations.
        then compress the list, remove the duplicates
        """
        stage1_question = self.question.format(
            q=f"Compression(Choose2Numbers([{self.task}]))"
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
        same as stage 1
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
        Evaluate the expression and if the result is 24, return True; otherwise, return False.
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
