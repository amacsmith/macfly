import openai

class OpenAIHTMLParser:
    def __init__(self, api_key, model="gpt-4"):
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key

    def parse(self, html_content, prompt=None):
        if prompt:
            full_prompt = f"{prompt}\n\nExtract relevant data from the following HTML content and return it as a JSON object:\n\n{html_content}"
        else:
            full_prompt = f"Extract relevant data from the following HTML content and return it as a JSON object:\n\n{html_content}"
        response = openai.Completion.create(
            model=self.model,
            prompt=full_prompt,
            max_tokens=1500
        )
        return response.choices[0].text.strip()
