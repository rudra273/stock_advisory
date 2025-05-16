# test_chain_gemini.py
from app.services.llm.gemini_llm import GeminiLLM
from app.services.llm.openai_llm import OpenAILLM

llm = GeminiLLM().get_llm()

# llm = OpenAILLM().get_llm()

# Define the prompt
prompt = "Explain the concept of LangChain in simple terms."


response = llm.invoke(prompt)


# Print the response
print(f"Prompt: {prompt}\n")
print(f"Response:\n{response.content}") 