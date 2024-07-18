from ..thoughts_manager import ThoughtsTemplate


class SpecificPrompt:
    @staticmethod
    def format(input: str, tmp: ThoughtsTemplate) -> tuple:
        system_prompt = """
    You are an expert in {domain}. Your task is to answer specific questions related to this field. Below is an example question and its corresponding answer, followed by a thought template to assist in your reasoning process. Use the example and thought template as guides to formulating your response, but always prioritize addressing the specific question in the [User Input]."""
        user_prompt = """
    User Input:
    {user_input}

    Example:
    Question:
    {Q}
    Answer:
    {A}

    Thought Template:
    {M}

    Important:
    - Focus on addressing the specific question in the [User Input].
    - Use the example and thought template as guides, but tailor the response to the context and details of the [User Input].
    - Ensure the response is highly relevant and accurate to the question asked in the [User Input].
    """
        return system_prompt.format(tmp["C"]), user_prompt.format(
            user_input=input, Q=tmp["E"]["Q"], A=tmp["E"]["A"], M=tmp["M"]
        )
