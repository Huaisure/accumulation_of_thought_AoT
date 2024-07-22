import openai


class GPT:
    def __init__(self, api_key, model_id):
        self.api_key = api_key
        self.model_id = model_id

    def get_response(self, user_prompt, system_prompt=None):
        messages = self.prompt2messages(user_prompt, system_prompt)
        client = openai.OpenAI(
            api_key=self.api_key, base_url="https://threefive.gpt7.link/v1"
        )
        response = client.chat.completions.create(
            model=self.model_id, messages=messages
        )
        # print("response:",response)
        return response.choices[0].message.content

    def prompt2messages(self, user_prompt, system_prompt=None):
        messages = []
        if system_prompt is not None:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        return messages
