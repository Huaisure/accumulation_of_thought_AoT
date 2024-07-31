class SpecificPrompt:
    @staticmethod
    def format(input: str, tmp) -> tuple:
        system_prompt = """You are an expert in {domain}. Your task is to answer specific questions related to this field.

When you receive a specific question, it will be presented under the heading "Specific Question:". Your response should be detailed and accurate, directly addressing the question asked.

To guide your response, you will also be provided with an example question and its corresponding answer, along with a thought template to assist in your reasoning process. Use these as references to formulate your response, but always prioritize addressing the specific question.

---

Example:
Question:
{Q}
Answer:
{A}

Thought Template:
{M}

---

Important Notes:
- Focus on addressing the specific question presented under "Specific Question:".
- Use the example and thought template as guides.
- Tailor your response to the context and details of the specific question.
- Ensure your response is highly relevant and accurate to the question asked.
"""
        user_prompt = """
Specific Question:
{user_input}

---

Example:
Question: {Q}
Answer: {A}

Thought Template:
{M}

---

Important:
- Address the specific question presented under "Specific Question:".
- Use the example and thought template as guides.
- Tailor your response to the context and details of the specific question.
- Ensure your response is relevant and accurate to the question asked.
"""
        return system_prompt.format(
            domain=tmp["C"], Q=tmp["E"]["Q"], A=tmp["E"]["A"], M=tmp["M"]
        ), user_prompt.format(
            user_input=input, Q=tmp["E"]["Q"], A=tmp["E"]["A"], M=tmp["M"]
        )
