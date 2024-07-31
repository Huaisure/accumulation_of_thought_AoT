import torch
from transformers import pipeline


class Pipeline:
    def __init__(self, model_id) -> None:
        self.pipeline = pipeline(
            "text-generation",
            model=model_id,
            tokenizer=model_id,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="cuda:0" if torch.cuda.is_available() else "cpu",
        )

    def get_response(self, user_prompt, system_prompt=None):
        messages = self._prompt2messages(user_prompt, system_prompt)

        self.pipeline.tokenizer.padding_side = "left"

        inputs = self.pipeline.tokenizer.apply_chat_template(
            messages, tokenize=False, add_special_tokens=True
        )
        terminators = [
            self.pipeline.tokenizer.eos_token_id,
            self.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
        ]

        outputs = self.pipeline(
            inputs,
            max_new_tokens=2048,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.4,
            top_p=0.9,
        )

        response = outputs[0]["generated_text"][len(inputs) :].strip()
        return response

    def _prompt2messages(self, prompt, instruct=None):
        messages = []
        if instruct is not None:
            messages.append({"role": "system", "content": instruct})
        messages.append({"role": "user", "content": prompt})
        return messages
