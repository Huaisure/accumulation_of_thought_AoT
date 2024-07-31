from .retriever import Retriever
from .item import ThoughtItem
from .sentence_model import SentenceModel
from ..llm import GPT, Pipeline, GuidanceLM
from ..prompts import NewTemplatePrompt, UpgradePrompt

from typing import Union

import json


class ThoughtsManager:
    """
    function: manage thoughts

    methods:

    1.extract thoughts template from QA pairs. A thoughts template consists of a 4-tuple: \
        (Description of the task, Method to solve the task, An example of the task and its answer, The classification of the task)\
            which means this manager can learn from huge amounts of QA pairs datasets.

    2.given a task, return the corresponding thoughts template

    3.update the thoughts template:
        given a 3-tuple (new task, new answer, corresponding template), update the thoughts template

    4.create a new thoughts template:
        given a new task, and no corresponding template, create a new template
    """

    def __init__(
        self,
        thoughts_template_path: str,
        sentence_model_name: str,
        llm_assistant: Union[GuidanceLM, GPT, Pipeline] = None,
        emb_pth: str = None,
        threshold: float = 0.5,
        execute_search_all: bool = False,
        logger=None,
    ):
        self.path = thoughts_template_path
        self.emb = emb_pth
        self.threshold = threshold
        self.search_all = execute_search_all
        self.llm = llm_assistant
        self.sentencemodel = SentenceModel(sentence_model_name)
        # self.thoughts_template = ThoughtItem(thoughts_template_path)
        self.retriever = Retriever(self.sentencemodel, self.emb, self.threshold)
        self.logger = logger

    def get_template(self, task) -> ThoughtItem:
        """
        get the corresponding template given a task
        """
        idx = self.retriever.search(task)
        self.logger.info(f"idx: {idx}")
        if idx == -1:
            # if the similarity is less than the threshold
            # create a new template
            return self._create_template_according_to_task(task)
        else:
            return ThoughtItem(self.path, idx)

    def _create_template_according_to_task(self) -> ThoughtItem:
        """
        this method is used to create a new template according to the task,
        considering some tasks may not have a template in the template file.
        """
        # find the most similar template
        template = ThoughtItem(self.path, self.retriever.search(self.task, create=True))
        system_prompt = NewTemplatePrompt.system_prompt
        user_prompt = NewTemplatePrompt.user_prompt.format(self.task, template)
        assistant_prompt = NewTemplatePrompt.assistant_prompt
        # TODO: compare the effect of whether or not to give a template
        template_response = self.llm.get_response(
            system_prompt, user_prompt, assistant_prompt
        )
        return self._extract_template_from_response(template_response, assistant_prompt)

    def _extract_template_from_response(self, response, assist) -> ThoughtItem:
        """
        extract the template from the response from gpt
        """
        # TODO
        # Accoding to the rule made in the NewTemplatePrompt, extract the template from the response
        if self.llm.__class__ == GuidanceLM:
            if type(response) is not dict:
                raise ValueError("The response should be a dict.")
            tmp = {}
            tmp["D"] = response[assist[0]]
            tmp["M"] = response[assist[1]]
            tmp["E"] = {}
            tmp["E"]["Q"] = response[assist[3]]
            tmp["E"]["A"] = response[assist[4]]
            tmp["C"] = response[assist[5]]
            return ThoughtItem(**tmp)
        else:
            raise NotImplementedError("The method is not implemented yet")

    def extract_template_from_qa_pairs(self, qa_pairs) -> ThoughtItem:
        """
        extract the thoughts template from a list of qa pairs
        """
        for qa_pair in qa_pairs:
            self._extract_template_from_qa_pair(qa_pair)

    def _extract_template_from_qa_pair(self, qa_pair) -> ThoughtItem:
        # TODO
        pass

    def upgrade_template(
        self, new_task: str, new_answer: str, old_template: ThoughtItem
    ):
        """
        upgrade the template
        """
        new_template = self._learn_from_new_task(new_task, new_answer, old_template)
        old_template.upgrade(new_template)

    def _learn_from_new_task(
        self, new_task: str, new_answer: str, old_template: ThoughtItem
    ):
        """
        learn from the new task and the answer
        """
        # TODO
        # learn from the new task and the answer
        system_prompt = UpgradePrompt.system_prompt
        user_prompt = UpgradePrompt.user_prompt.format(
            new_task, new_answer, old_template
        )
        assistant_prompt = UpgradePrompt.assistant_prompt
        response = self.llm.get_response(system_prompt, user_prompt, assistant_prompt)
        new_template = self._extract_template_from_response(response, assistant_prompt)
        return new_template

    def add_template(self, new_template):
        if type(new_template) not in [dict, ThoughtItem]:
            raise ValueError("The new template should be a dict or a ThoughtItem.")
        if type(new_template) is ThoughtItem:
            new_template = json.dumps(new_template.data)
        else:
            new_template = json.dumps(new_template)
        with open(self.path, "a") as file:
            file.write(new_template)
