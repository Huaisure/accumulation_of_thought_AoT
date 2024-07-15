from guidance import models, system, user, assistant
from guidance import gen


class GuidanceLM:
    def __init__(self, model_name, api_key=None) -> None:
        self.model_name = model_name
        self.api_key = api_key

        if api_key is not None:
            self.llm = models.OpenAI(
                api_key,
                model_name,
                api_key=api_key,
                base_url=" ",
            )
        else:
            self.llm = models.LlamaCpp(model_name, temperature=0.4)

    def get_response(self, system_prompt, user_prompt, assistant_prompt=None):
        lm = self.llm
        with system():
            lm += system_prompt
        with user():
            lm += user_prompt
        with assistant():
            lm += assistant_prompt
            lm += gen(max_tokens=2048, name="assistant")
        return lm["assistant"]
