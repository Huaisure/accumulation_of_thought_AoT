import openai


class GPT:
    def __init__(self, api_key, model_id):
        self.api_key = api_key
        self.model_id = model_id

    def get_response(self, prompt, instruct=None):
        messages = self.prompt2messages(prompt, instruct)
        client = openai.OpenAI(
            api_key=self.api_key, base_url="https://threefive.gpt7.link/v1"
        )
        response = client.chat.completions.create(
            model=self.model_id, messages=messages
        )
        # print("response:",response)
        return response.choices[0].message.content

    def prompt2messages(self, prompt, instruct=None):
        messages = []
        if instruct is not None:
            messages.append({"role": "system", "content": instruct})
        messages.append({"role": "user", "content": prompt})
        return messages
