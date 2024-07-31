from ...function.solver_base import FunctionSolverBase
from ...function.evaluate_solver import EvaluateSolver
from .func_dict_list import GAME_OF_24_FUNC_DICT_LIST
from ...utlis import parselist, compress, evaluate, task_preprocess
from .gameof24_task import (
    STAGE1_TASK,
    STAGE2_TASK,
    STAGE3_TASK,
    STAGE1_TASK_WITHOUT_COMPRESSION,
    STAGE2_TASK_WITHOUT_COMPRESSION,
)

from typing import List, Dict
from loguru import logger

# python -m accumulation_of_thoughts.prompt_function.gameof24


class GameOf24Solver(FunctionSolverBase):
    """
    Game of 24 solver (With Prmopt Function)

    Args:
        assistant (class: GPT): The assistant to help solve the problem
        batch_size (int): The batch size, which is limited by the max token length of the assistant
        functions_list (List[Dict]): list of functions dictionary

    example:
    >>> gameof24_solver = GameOf24Solver(assistant, functions_list=GAME_OF_24_FUNC_DICT_LIST)
    >>> gameof24_solver.solve("3,3,8,8")
    """

    task_description = "Game of 24: Given four numbers, return a list of expressions that can be combined to 24. Each number must be used once."
    objective = (
        "a list of expressions that contains each number excatly once and reach 24."
    )

    def __init__(
        self,
        assistant,
        batch_size: int = 6,
        functions_list: List[Dict] = GAME_OF_24_FUNC_DICT_LIST,
    ):
        super().__init__()
        # super().load_function(functions)
        if functions_list:
            self.load_function(functions_list)

        else:
            # At this time, we do not support the situation where the function list is empty
            raise ValueError("functions_list is required")

        self.first_round_list = None
        self.second_round_list = None
        self.third_round_list = None
        self.assistant = assistant
        self.batch_size = batch_size

    def solve(self, task: str = "3,3,8,8") -> str:
        """
        Solve the task

        Args:
            task (str): The task to solve

        Returns:
            str: The result of the task
        """
        self.task = task
        # time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        # logger.remove()
        # logger.add(f"logs/game_of_24_{time}.log", rotation="1 day")
        # logger.info("System Prompt:\n" + PROMPT_FUNCTION_SYSTEM_PROMPT)

        # ** Stage 1 begin **
        logger.success("#################### Stage 1 ####################")
        self._set_stage(
            func_list=[self.func["Compression"], self.func["Choose2Numbers"]],
            task=STAGE1_TASK.format(task=task_preprocess(self.task)),
            outermost_func=self.func["Compression"],
        )
        self.stage1 = self.solve_stage[0]
        self.stage1_result = self.stage1.solve()
        self.first_round_list = parselist(self.stage1_result)
        logger.info("Stage 1 result:\n" + self.stage1_result)
        logger.info("First round list:\n" + str(self.first_round_list))

        # ** Stage 2 begin **
        logger.success("#################### Stage 2 ####################")
        self.stage2_result = []
        self.second_round_list = []
        self._set_stage(
            func_list=[
                self.func["Compression"],
                self.func["Choose2Numbers"],
                self.func["Choose2NumbersForEachItem"],
            ],
            task=None,
            outermost_func=self.func["Compression"],
        )
        self.stage2 = self.solve_stage[1]
        # due to the limitation of max token, decompose first round list in piece
        for i in range(0, len(self.first_round_list), self.batch_size):
            self.stage2.update_task(
                STAGE2_TASK.format(list=self.first_round_list[i : i + self.batch_size])
            )
            self.stage2_result.append(self.stage2.solve())
            self.second_round_list.extend(parselist(self.stage2_result[-1]))
        logger.info("Stage 2 result:\n" + str(self.stage2_result))
        logger.info("Second round list:\n" + str(self.second_round_list))

        # # ** Stage 3 begin **
        logger.success("#################### Stage 3 ####################")
        self.stage3_result = []
        self.third_round_list = []
        self._set_stage(
            func_list=[self.func["Evaluate"]],
            task=None,
            outermost_func=self.func["Evaluate"],
        )
        self.stage3 = self.solve_stage[2]
        self.result = None
        # due to the limitation of max token, decompose first round list in piece
        for i in range(0, len(self.second_round_list), self.batch_size * 3):
            self.stage3.update_task(
                STAGE3_TASK.format(
                    list=self.second_round_list[i : i + self.batch_size * 3],
                    task="[3,3,8,8]",
                )
            )
            res = parselist(self.stage3.solve())
            self.stage3_result.extend(res)
            for r in res:
                if "None" not in r:
                    self.result = r
                    break
            if self.result:
                break

            # self.third_round_list.extend(parselist(self.stage3_result[-1]))
            # if self.stage3_result[-1] != "None":
            #     self.result = self.stage3_result[-1]
            #     break
        logger.info("Stage 3 result:\n" + str(self.stage3_result))
        logger.info("Result:\n" + self.result)
        # logger.info("Third round list:\n" + str(self.third_round_list))
        # self.result = self.stage3_result[-1]

    def solve_with_compress(self, task: str = "3,3,8,8") -> str:
        """
        Handwritten compression function, different from the previous compression using GPT
        """
        self.task = task
        # time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        # logger.remove()
        # logger.add(f"logs/game_of_24_{time}.log", rotation="1 day")

        # ** Stage 1 begin **
        logger.success("#################### Stage 1 ####################")
        self._set_stage(
            func_list=[self.func["Choose2Numbers"]],
            task=STAGE1_TASK_WITHOUT_COMPRESSION.format(
                task=task_preprocess(self.task)
            ),
            outermost_func=self.func["Choose2Numbers"],
        )
        self.stage1 = self.solve_stage[0]
        self.stage1_result = self.stage1.solve()
        self.first_round_list = compress(parselist(self.stage1_result))
        # logger.info("Stage 1 result:\n" + self.stage1_result)
        logger.info("First round list:\n" + str(self.first_round_list))
        logger.info("First round list length: " + str(len(self.first_round_list)))

        # ** Stage 2 begin **
        logger.success("#################### Stage 2 ####################")
        self.stage2_result = []
        self.second_round_list = []
        self._set_stage(
            func_list=[
                self.func["Choose2Numbers"],
                self.func["Choose2NumbersForEachItem"],
            ],
            task=None,
            outermost_func=self.func["Choose2NumbersForEachItem"],
        )
        self.stage2 = self.solve_stage[1]
        # due to the limitation of max token, decompose first round list in piece
        for i in range(0, len(self.first_round_list), self.batch_size):
            self.stage2.update_task(
                STAGE2_TASK_WITHOUT_COMPRESSION.format(
                    list=self.first_round_list[i : i + self.batch_size]
                )
            )
            self.stage2_result.append(self.stage2.solve())
            self.second_round_list.extend(parselist(self.stage2_result[-1]))
        self.second_round_list = compress(self.second_round_list)
        # logger.info("Stage 2 result:\n" + str(self.stage2_result))
        logger.info("Second round list:\n" + str(self.second_round_list))
        logger.info("Second round list length: " + str(len(self.second_round_list)))

        # ** Stage 3 begin **
        """
        logger.success("#################### Stage 3 ####################")
        self.stage3_result = []
        self.third_round_list = []
        self.stage3 = self.set_stage(
            func_list=[
                self.func["Choose2Numbers"],
                self.func["Evaluate24"],
                self.func["Evaluate"],
            ],
            task=None,
            outermost_func=self.func["Evaluate"],
        )
        self.result = None
        for i in range(0, len(self.second_round_list), self.batch_size * 3):
            self.stage3.update_task(
                STAGE3_TASK.format(
                    list=self.second_round_list[i : i + self.batch_size * 3],
                    task="[3,3,8,8]",
                )
            )
            res = parselist(self.stage3.solve())
            self.stage3_result.extend(res)
            for r in res:
                if "None" not in r:
                    self.result = r
                    break
            if self.result:
                break
        """

        # Stage 3 Plan B:
        # abondon Evaluate and return the whole list, then stage3.function equals to stage2.function
        logger.success("#################### Stage 3 ####################")
        self.stage3_result = []
        self.third_round_list = []
        self.stage3 = self.stage2
        batch_size_stage3 = self.batch_size * 3
        for i in range(0, len(self.second_round_list), batch_size_stage3):
            self.stage3.update_task(
                STAGE2_TASK_WITHOUT_COMPRESSION.format(
                    list=self.second_round_list[i : i + batch_size_stage3]
                )
            )
            self.stage3_result.append(self.stage3.solve())
            self.third_round_list = parselist(self.stage3_result[-1])
            self.result = evaluate(self.third_round_list)
            if self.result:
                # logger.info("Stage 3 result:\n" + str(self.stage3_result))
                logger.info("Result:\n" + self.result)
                return self.result
        logger.error("No solution found")
        return "No solution found"

    def evaluate_states(self, current_states: List[str]) -> List[float]:
        """
        Evaluate the states

        Args:
            current_states (List[str]): The current states

        Returns:
            List[float]: The probabilities of the states
        """
        evaluate_solver_instance = EvaluateSolver(
            self.task_description, self.objective, current_states, self.assistant
        )
        return parselist(evaluate_solver_instance.solve())

    def _test_evaluate(self):
        test_states = [
            "[((3+3)+8),8]",
            "[(8/3),3,8]",
            "[(3*3),8,8]",
            "[(8*8),3,3]",
            "[(3-(8/3)),8]",
            "[((3*3)+8),8]",
        ]
        print(self.evaluate_states(test_states))
