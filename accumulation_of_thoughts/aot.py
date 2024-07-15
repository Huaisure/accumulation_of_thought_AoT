from .retriever import Retriever
from .thoughts_template import ThoughtsTemplate
from loguru import logger


class AccumulationOfThoughts:
    def __init__(
        self,
        model_name="meta-llama/Llama-3-8B-Instruct",
        api_key=None,
        sentence_model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        emb_pth=None,
        template_pth=None,
        threshold=0.5,
        inputs=None,
        use_guidance=False,
    ):
        self.retriever = Retriever(sentence_model_name, emb_pth, threshold)
        self.thoughts_template = ThoughtsTemplate(template_pth)

        if not use_guidance:
            if api_key is not None:
                from .llm import GPT

                self.llm = GPT(api_key)
            else:
                from .llm import Pipeline

                self.llm = Pipeline(model_name)
        else:
            from .llm import GuidanceLM

            self.llm = GuidanceLM(model_name, api_key)
        self.task = inputs
        self.has_template = False

    def get_template(self, idx):
        idx = self.retriever.search(self.task)
        if idx == -1:
            self.has_template = False
        else:
            self.has_template = True
            return self.thoughts_template.gettemplate(idx)

    def create_template_according_to_task(self):
        """
        this method is used to create a new template according to the task,
        considering some tasks may not have a template in the template file.
        """
        template = self.retriever.search(self.task, create=True)
        template = self.llm.get_respond(template)
        pass

    def update_template(self, idx, new_template):
        self.thoughts_template.update(idx, new_template)

    def update_input(self, new_input):
        self.task = new_input

    def run(self):
        template = self.get_template(self.task)
        if self.has_template:
            logger.success("Get template successfully!")
            logger.info(f"Template: {template}")
        else:
            logger.error("No template found!")
            template = self.create_template_according_to_task()
            logger.info(f"Create a new template: {template}")
        response = self.llm.get_respond(self.task, template)
        logger.info(f"Response: {response}")
        pass
