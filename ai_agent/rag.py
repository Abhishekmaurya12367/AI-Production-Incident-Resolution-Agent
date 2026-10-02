import os
import glob
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def build_rag():
    print("1. Loading documents...")
    knowledge_dir = os.path.join(os.path.dirname(__file__), '..', 'knowledge')
    markdown_files = glob.glob(f'{knowledge_dir}/**/*.md', recursive=True)

    documents = []
    for file_path in markdown_files:
        loader = TextLoader(file_path, encoding='utf-8')
        documents.extend(loader.load())

    print("2. Chunking documents...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    print("3. Generating embeddings & Building Vector DB...")
    # Using a fast, lightweight open-source embedding model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Store in ChromaDB (creates a local ./chroma_db folder)
    persist_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
    vectorstore = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=persist_dir
    )

    print("4. RAG Pipeline built successfully!\n")
    return vectorstore.as_retriever(search_kwargs={"k": 3})

def query_rag(retriever, user_query):
    print(f"User Query: '{user_query}'\n")
    
    # 5. Retrieve relevant documentation
    print("--- 5. Retriever Fetching Relevant Docs ---")
    relevant_docs = retriever.invoke(user_query)
    
    context = ""
    for idx, doc in enumerate(relevant_docs, 1):
        filename = os.path.basename(doc.metadata.get('source', 'unknown'))
        print(f"Found match in: {filename}")
        context += f"\n--- Document: {filename} ---\n{doc.page_content}\n"
    
    # 6. LLM Prompt Construction
    print("\n--- 6. Constructing Prompt for LLM ---")
    prompt = f"""You are an incident response AI. Answer the user's query using ONLY the provided documentation context.

Context:
{context}

Query: {user_query}
Answer:
"""
    print(prompt)
    print("\n(Note: At this stage, this prompt is sent to your LLM (OpenAI/Gemini/Anthropic) to generate the final text answer.)")

if __name__ == "__main__":
    retriever = build_rag()
    
    test_query = "Why is payment service returning 500?"
    query_rag(retriever, test_query)
