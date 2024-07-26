import torch
from transformers import pipeline


class Pipeline:
    def __init__(self, model_name) -> None:
        self.pipeline = pipeline(
            "text-generation",
            model=model_name,
            tokenizer=model_name,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="cuda:0" if torch.cuda.is_available() else "cpu",
        )

    def get_response(self, prompt, instruct=None):
        messages = self.prompt2messages(prompt, instruct)

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
        # length = len(prompt) + len(instruct) if instruct is not None else len(prompt)

        response = outputs[0]["generated_text"][len(inputs) :].strip()
        return response

    def prompt2messages(self, prompt, instruct=None):
        messages = []
        if instruct is not None:
            messages.append({"role": "system", "content": instruct})
        messages.append({"role": "user", "content": prompt})
        return messages
