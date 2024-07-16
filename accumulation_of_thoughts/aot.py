from .thoughts_manager import ThoughtsManager, ThoughtsTemplate, Retriever
from .prompts import BasicPrompt, NewTemplatePrompt


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
        logger=None,
    ):

        self.logger = logger

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

        self.thoughts_manager = ThoughtsManager(
            template_pth,
            sentence_model_name,
            llm_assistant=self.llm,
            emb_pth=emb_pth,
            threshold=threshold,
        )
        self.task = inputs
        self.has_template = False

    def get_template(self):
        self.template = self.thoughts_manager.get_template(self.task)

    # def update_template(self, idx, new_template):
    #     self.thoughts_template.update(idx, new_template)

    def update_input(self, new_input):
        self.task = new_input
        self.has_template = False

    def run(self, new_input):
        self.update_input(new_input)
        self.get_template()
        self.logger.success("Get template successfully!")
        self.logger.info(f"Template: {self.template}")
        system_prompt = BasicPrompt.system_prompt
        user_prompt = BasicPrompt.user_prompt.format(
            user_input=self.task, thought_template=self.template
        )
        response = self.llm.get_response(system_prompt, user_prompt)
        self.logger.info(f"Response: {response}")
