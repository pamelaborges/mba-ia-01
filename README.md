# Chatbot RAG – Desafio 01

Este diretório implementa um chatbot em linha de comando que responde perguntas sobre o relatório `relatorio_bairros.pdf`. A solução utiliza a abordagem Retrieval-Augmented Generation (RAG) com LangChain, embeddings gerados por OpenAI ou Google Gemini e persistência vetorial em PostgreSQL com a extensão `pgvector`.

## Tecnologias
- LangChain (core, community, text splitters, postgres)
- OpenAI e Google Generative AI (Gemini)
- PostgreSQL + pgvector (via Docker Compose)
- Pydantic Settings para gerenciamento de variáveis de ambiente

## Estrutura
- `docker-compose.yml`: sobe o banco PostgreSQL e aplica a extensão `vector`.
- `requirements.txt`: dependências específicas deste desafio.
- `relatorio_bairros.pdf`: fonte de conhecimento do chatbot.
- `src/settings.py`: carrega variáveis de ambiente a partir de `.env`.
- `src/ingest.py`: pipeline que lê o PDF, divide em chunks, gera embeddings e salva no vetor store.
- `src/store.py`: inicializa o `PGVector` conectado ao PostgreSQL.
- `src/search.py`: chains de busca e geração, com implementações para OpenAI e Gemini.
- `src/prompts.py`: prompt usado para controlar o comportamento do modelo.
- `src/chat.py`: interface CLI que orquestra o fluxo de perguntas e respostas.

## Pré-requisitos
- Python 3.11 ou superior
- Docker + Docker Compose
- Credenciais válidas para os provedores que pretender usar (OpenAI e/ou Google Gemini)

## Configuração do ambiente
1. **Instale as dependências**
   ```bash
   cd desafios/01
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure o arquivo `.env`** (na raiz de `desafios/01/`):
   ```env
   OPENAI_API_KEY=coloque_sua_chave
   OPENAI_MODEL=gpt-4o-mini
   OPENAI_EMBEDDING_MODEL=text-embedding-3-small

   GOOGLE_API_KEY=coloque_sua_chave
   GOOGLE_MODEL=gemini-1.5-flash
   GOOGLE_EMBEDDING_MODEL=models/embedding-001

   DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
   PG_VECTOR_COLLECTION_NAME=data_collection
   PDF_PATH=relatorio_bairros.pdf
   ```
   > Mantenha esse arquivo fora do controle de versão.

3. **Suba o PostgreSQL com pgvector**
   ```bash
   docker compose up -d
   ```
   O serviço auxiliar `bootstrap_vector_ext` cria a extensão `vector` no banco `rag`. Para encerrar os serviços, execute `docker compose down`.

4. **Ingestão do PDF**
   ```bash
   python src/ingest.py
   ```
   O script carrega o PDF, cria chunks com sobreposição, enriquece metadados, gera embeddings e grava tudo em `PG_VECTOR_COLLECTION_NAME`. Reexecute sempre que mudar o conteúdo ou o modelo de embeddings.

5. **Executar o chatbot**
   ```bash
   python src/chat.py
   ```
   - Selecione o provedor: `1` para OpenAI, `2` para Gemini.
   - Faça perguntas sobre o relatório; as respostas seguem rigidamente o conteúdo indexado.

## Fluxo interno
1. `chat.py` recebe perguntas do usuário, escolhe a chain adequada e delega a resposta.
2. `search.py` busca passagens relevantes no vetor store (`PGVector.similarity_search_with_score`), monta o contexto e chama o LLM com o prompt de segurança.
3. `prompts.py` garante que o modelo responda apenas com base no contexto recuperado.
4. `store.py` encapsula a conexão com o banco vetorial.
5. `ingest.py` cuida do pré-processamento e armazenamento dos documentos.

## Dicas
- Atualize `PDF_PATH` se quiser usar outro documento como base de conhecimento.
- Para usar apenas um provedor, basta preencher as variáveis relacionadas a ele.
- Mantenha os contêineres sob controle (`docker compose down`) ao finalizar os testes para liberar recursos.
