from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434",api_key="ollama")

response = client.responses.create(
    model="qwen2.5:7b",
    tools=[],
    input="Hello"
)

print(response.output_text)