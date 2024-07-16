from .retriever import Retriever
from .thoughts_template import ThoughtsTemplate
from .sentence_model import SentenceModel
from ..llm import GPT, Pipeline, GuidanceLM
from ..prompts import NewTemplatePrompt

from typing import Union


class ThoughtsManager:
    """
    function: manage thoughts

    methods:

    1.extract thoughts template from QA pairs. A thoughts template consists of a 4-tuple: \
        (Description of the task, Method to solve the task, An example of the task and its answer, The classification of the task)

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
    ):
        self.path = thoughts_template_path
        self.emb = emb_pth
        self.threshold = threshold
        self.search_all = execute_search_all
        self.llm = llm_assistant
        self.sentencemodel = SentenceModel(sentence_model_name)
        # self.thoughts_template = ThoughtsTemplate(thoughts_template_path)
        self.retriever = Retriever(self.sentencemodel, self.emb, self.threshold)

    def get_template(self, task) -> ThoughtsTemplate:
        """
        get the corresponding template given a task
        """
        idx = self.retriever.search(task)
        if idx == -1:
            # if the similarity is less than the threshold
            # create a new template
            return self._create_template_according_to_task(task)
        else:
            return ThoughtsTemplate(self.path, idx)

    def _create_template_according_to_task(self) -> ThoughtsTemplate:
        """
        this method is used to create a new template according to the task,
        considering some tasks may not have a template in the template file.
        """
        # find the most similar template
        template = ThoughtsTemplate(
            self.path, self.retriever.search(self.task, create=True)
        )
        system_prompt = NewTemplatePrompt.system_prompt
        user_prompt = NewTemplatePrompt.user_prompt.format(self.task, template)
        assistant_prompt = NewTemplatePrompt.assistant_prompt
        # TODO: compare the effect of whether or not to give a template
        template_response = self.llm.get_response(
            system_prompt, user_prompt, assistant_prompt
        )
        return self._extract_template_from_response(template_response, assistant_prompt)

    def _extract_template_from_response(self, response, assist) -> ThoughtsTemplate:
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
            return ThoughtsTemplate(**tmp)
        else:
            raise NotImplementedError("The method is not implemented yet")

    def extract_template_from_qa_pairs(self, qa_pairs) -> ThoughtsTemplate:
        """
        extract the thoughts template from a list of qa pairs
        """
        for qa_pair in qa_pairs:
            self._extract_template_from_qa_pair(qa_pair)

    def _extract_template_from_qa_pair(self, qa_pair) -> ThoughtsTemplate:
        # TODO
        pass

    def add_template(self, new_template):
        with open(self.path, "a") as file:
            file.write(new_template)
