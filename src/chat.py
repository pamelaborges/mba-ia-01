from search import search_prompt

PROVIDERS = {
    "1": "openai",
    "2": "gemini",
}

def main():
    
    print("Bem vindo ao chatbot!")
    llm = input("Qual llm deseja utilizar? \n1: OpenAI \n2: Gemini \n").strip()
    
    provider = PROVIDERS.get(llm)
    if provider is None:
        raise ValueError("Opção inválida")
        
    while True:
        question = input("Como posso te ajudar?")
        answer = search_prompt(question, provider)
        print(answer)
        
        
if __name__ == "__main__":
    main()
