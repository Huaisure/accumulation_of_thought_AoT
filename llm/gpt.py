import openai


class GPT:
    """
    GPT openai chatbot

    This class interfaces with the OpenAI GPT model.

    Args:
        api_key (str): openai api key
        model_id (str): openai model id
        temperature (float): temperature for the chatbot
    """

    def __init__(self, api_key, model_id, temperature=0.4):
        self.api_key = api_key
        self.model_id = model_id
        self.temperature = temperature

    def get_response(self, user_prompt, system_prompt=None, max_try=3):
        """
        Get the response from the chatbot

        Args:
            user_prompt (str): user prompt
            system_prompt (str): system prompt if have

        Returns:
            str: response from the chatbot
        """
        messages = self._prompt2messages(user_prompt, system_prompt)
        client = openai.OpenAI(
            api_key=self.api_key, base_url="https://gtapi.xiaoerchaoren.com:8932/v1"
        )

        # several tries
        for _ in range(max_try):
            try:
                response = client.chat.completions.create(
                    model=self.model_id, messages=messages, temperature=self.temperature
                )
                return response.choices[0].message.content
            except Exception as e:
                print(e)
                continue
        # response = client.chat.completions.create(
        #     model=self.model_id, messages=messages, temperature=self.temperature
        # )
        # # print("response:",response)
        # return response.choices[0].message.content

    def _prompt2messages(self, user_prompt, system_prompt=None):
        messages = []
        if system_prompt is not None:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        return messages
