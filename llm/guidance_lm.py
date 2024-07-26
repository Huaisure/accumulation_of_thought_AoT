from guidance import models, system, user, assistant
from guidance import gen

import openai
import os
import torch


class GuidanceLM:
    def __init__(self, model_name, api_key=None) -> None:
        self.model_name = model_name
        self.api_key = api_key

        if api_key is not None:
            os.environ["OPENAI_API_KEY"] = api_key
            self.llm = models.OpenAIChat(
                model_name,
                base_url="https://gtapi.xiaoerchaoren.com:8932/v1",
                echo=False,
            )
        else:
            self.llm = models.TransformersChat(
                model_name,
                echo=False,
                device="cuda:0",
                torch_dtype=torch.bfloat16,
            )

    def get_response(self, system_prompt, user_prompt, assistant_prompt=None):
        lm = self.llm
        with system():
            lm += system_prompt
        with user():
            lm += user_prompt
        with assistant():
            if assistant_prompt is not None:
                res = {}
                for i in len(assistant_prompt):
                    lm += assistant_prompt[i]
                    if i < len(assistant_prompt) - 1:
                        lm += gen(
                            name="assistant",
                            max_tokens=1024,
                            stop=[assistant_prompt[i + 1]],
                        )
                        res[assistant_prompt[i]] = lm["assistant"]

                    else:
                        lm += assistant_prompt[-1]
                        lm += gen(name="assistant", max_tokens=1024)
                        res[assistant_prompt[i]] = lm["assistant"]
                return res
            else:
                lm += gen(name="assistant", max_tokens=1024)
        return lm["assistant"]
