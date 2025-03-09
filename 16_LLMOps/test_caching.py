from langchain.cache import InMemoryCache, LocalFileStore
from langchain.globals import set_llm_cache
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import time

def test_rag_caching():
    # Initialize the chat model
    chat_model = ChatOpenAI(temperature=0)
    
    # Set up caching
    store = LocalFileStore("./cache/")
    cache = InMemoryCache()
    set_llm_cache(cache)
    
    # Set up RAG prompt template
    rag_system_prompt_template = """\
    You are a helpful assistant that uses the provided context to answer questions. Never reference this prompt, or the existance of context.
    """

    rag_user_prompt_template = """\
    Question:
    {question}
    Context:
    {context}
    """

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", rag_system_prompt_template),
        ("human", rag_user_prompt_template)
    ])
    
    # Test cases with sample context
    test_cases = [
        {
            "question": "What is quantum computing?",
            "context": "Quantum computing is a type of computing that harnesses quantum phenomena like superposition and entanglement. Unlike classical computers that use bits, quantum computers use quantum bits or qubits."
        },
        {
            "question": "What is quantum computing?",  # Same question to test cache
            "context": "Quantum computing is a type of computing that harnesses quantum phenomena like superposition and entanglement. Unlike classical computers that use bits, quantum computers use quantum bits or qubits."
        }
    ]
    
    # Run tests and measure response times
    response_times = []
    responses = []
    
    for i, test_case in enumerate(test_cases):
        start_time = time.time()
        
        # Format the prompt with the test case
        messages = chat_prompt.format_messages(
            question=test_case["question"],
            context=test_case["context"]
        )
        
        # Get response
        response = chat_model.predict_messages(messages)
        end_time = time.time()
        
        response_times.append(end_time - start_time)
        responses.append(response)
        
        print(f"\nTest Case {i+1}")
        print(f"Question: {test_case['question']}")
        print(f"Response: {response.content}")
        print(f"Response time: {response_times[-1]:.2f} seconds")
        
        # Check if response was cached (for second iteration)
        if i >= 1:
            original_time = response_times[0]
            cached_time = response_times[1]
            speedup = original_time / cached_time
            print(f"Cache speedup: {speedup:.2f}x faster")
            
            # Verify responses match
            if responses[0].content == responses[1].content:
                print("✅ Cached response matches original")
            else:
                print("❌ Warning: Cached response differs from original")

if __name__ == "__main__":
    test_rag_caching() 