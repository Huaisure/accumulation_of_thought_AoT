from .solver import FunctionSolverBase, PromptFunction

from typing import List
from loguru import logger

import warnings


class SolveStage(FunctionSolverBase):
    """
    The stage to solve the problem

    Args:
        func_list (List[PromptFunction]): The function list used in the stage
        task (str): The task to solve
        assistant (class: GPT): The assistant to help solve the problem
        outermost_func (PromptFunction): The outermost function
    """

    def __init__(
        self,
        func_list: List[PromptFunction],
        task: str,
        assistant,
        outermost_func: PromptFunction = None,
        system_prompt: str = None,
    ) -> None:
        super().__init__()
        self.functions = func_list
        self.user_prompt = super().define_function_all()
        self.assistant = assistant

        if outermost_func is None:
            self.outermost_func = self.func_list[0]
            warnings.warn(
                f"The outermost function is not specified, the first function in the list (function name: {self.func_list[0].name}) is used as the outermost function,\
                that may cause the output to be incorrect. Please specify the outermost function."
            )
        else:
            self.outermost_func = outermost_func
        self.system_prompt = system_prompt
        self.question = task

        logger.info("Solve Stage Initialized")
        logger.info("System Prompt: \n" + self.system_prompt)
        logger.info("User Prompt: \n" + self.user_prompt)

    def update_task(self, question: str):
        self.question = question

    def solve(self):
        self.task = (
            self.user_prompt
            + f"**Question**:\n{self.question}\nWith the above function, output as required."
        )

        # logger.info("System Prompt: \n" + self.system_prompt)
        logger.info("User Prompt: \n" + self.question)
        response = self.assistant.get_response(
            user_prompt=self.task, system_prompt=self.system_prompt
        )
        logger.info("Response: \n" + response)
        # Make sure func_list[0] is the outermost function
        return self.outermost_func.output_parse(response)
