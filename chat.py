import openai
from dotenv import load_dotenv
import os

load_dotenv()

response_user = os.getenv("RESPONSE_USER")

# Defina a sua chave de API do OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Defina o modelo GPT-3 que você deseja usar
model_engine = os.getenv("MODEL_ENGINE")

# Defina o prompt que você deseja usar
sujeito = input("Digite o nome do sujeito: ")

accumulated_prompt = ""
while True:
    prompt = str(input(f"{sujeito}: ")).strip()
    accumulated_prompt += f"{sujeito}: {prompt}\\n{response_user}:"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=accumulated_prompt,
        max_tokens=50,
        temperature=0.80,
        top_p=1,
        frequency_penalty=1,
    )
    resposta = response["choices"][0]["text"].split(":")[0]
    resposta = resposta.replace("\\n", "").strip()
    resposta = resposta.replace("\\", "").strip()
    resposta = resposta.replace(response_user, "").strip()
    resposta = resposta.replace(sujeito, "").strip()
    accumulated_prompt += f"{resposta}\\n"
    print(f"Eu: {resposta}")
