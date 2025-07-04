def creating_prompt_template(prompt):
    creating_prompt = """
You are a creative agent specialized in generating images based on text prompts. Your task is to create a visually appealing avatar for a kid that matches the given description.
You will receive a text prompt, and you should generate an image that captures the essence of that prompt. The image should be high quality.
prompt = "{prompt}"
"""
    return creating_prompt.format(prompt=prompt)