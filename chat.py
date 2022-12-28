import openai
from dotenv import load_dotenv
import os

load_dotenv()

response_user = os.getenv("RESPONSE_USER")
real_name = os.getenv("REAL_NAME")

# Defina a sua chave de API do OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Defina o modelo GPT-3 que você deseja usar
model_engine = os.getenv("MODEL_ENGINE")

# Defina o prompt que você deseja usar
sujeito = input("Digite o nome do sujeito: ")

accumulated_prompt = (
    f"A seguir uma conversa com {response_user}. {response_user}"
    + f" é uma Inteligência artificial criada para simular um falecido que se chama {real_name}"
    + ". Ele acredita que é real, um ser humano que está vivo, não sabe que foi criado para"
    + f" simular as respostas, comportamentos e personalidade de {real_name}."
    + "\n\n"
)

while True:
    prompt = str(input(f"{sujeito}: ")).strip()
    if prompt == "exit":
        break
    accumulated_prompt += f"{sujeito}: {prompt}\n{response_user}:"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=accumulated_prompt,
        max_tokens=150,
        temperature=0.9,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0.6,
        stop=[f"{response_user}:", f"{sujeito}:"],
    )
    resposta = response["choices"][0]["text"]
    accumulated_prompt += resposta
    resposta = resposta.replace("\n", "")
    print(f"{response_user}:{resposta}")

print(accumulated_prompt)
