import openai
import os

print('--------------------------------')
print(openai.__version__)
print('--------------------------------')

# Defina sua chave de API do OpenAI como variável de ambiente ou substitua `os.environ.get("OPENAI_KEY")` pela sua chave diretamente.
openai.api_key = os.environ.get("OPENAI_KEY")  # Substitua pela sua chave, se necessário
openai_key = os.environ.get("OPENAI_KEY")
print("Valor da variável de ambiente OPENAI_KEY:",openai_key)
def enviar_bom_dia():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Diga bom dia!"}
            ],
            max_tokens=10  # Limitando para uma resposta curta
        )

        # Imprime a resposta do ChatGPT
        print(response.choices[0].message['content'].strip())
    
    except Exception as e:
        print(f"Erro ao acessar OpenAI: {e}")

# Chama a função para enviar "Bom dia!"
        

enviar_bom_dia()
