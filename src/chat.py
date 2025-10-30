from search import search_prompt

PROVIDERS = {
    "1": "openai",
    "2": "gemini",
}

def main():
    
    print("Bem vindo ao chatbot!")
    llm = input("Qual llm deseja utilizar? 1: OpenAI | 2: Gemini").strip()
    
    provider = PROVIDERS.get(llm)
    if provider is None:
        raise ValueError("Opção inválida")
        
    while True:
        question = input("Como posso te ajudar?")
        answer = search_prompt(question, provider)
        print(answer)
        
        
if __name__ == "__main__":
    main()
