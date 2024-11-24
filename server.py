import asyncio
import websockets
import json

questions = [
    {
        "id": 1, 
        "question": "What is Artificial Intelligence?", 
        "ideal_answer": "Artificial Intelligence is the simulation of human intelligence by machines, involving tasks like learning, reasoning, and problem-solving.",
        "key_concepts": ["simulation", "human intelligence", "machines", "learning", "reasoning", "problem-solving"]
    },
    {
        "id": 2, 
        "question": "What is Machine Learning?", 
        "ideal_answer": "Machine Learning is a subset of AI that focuses on learning patterns from data.",
        "key_concepts": ["subset", "AI", "learning", "patterns", "data"]
    },
    {
        "id": 3,
        "question": "What are the main types of Machine Learning?",
        "ideal_answer": "The main types of Machine Learning are supervised, unsupervised, and reinforcement learning.",
        "key_concepts": ["supervised", "unsupervised", "reinforcement learning"]
    },
    {
        "id": 4,
        "question": "What is supervised learning?",
        "ideal_answer": "Supervised learning is a type of Machine Learning where the model is trained using labeled data.",
        "key_concepts": ["supervised", "Machine Learning", "labeled data", "trained"]
    },
    {
        "id": 5,
        "question": "What is unsupervised learning?",
        "ideal_answer": "Unsupervised learning is a type of Machine Learning where the model identifies patterns and relationships in data without labels.",
        "key_concepts": ["unsupervised", "Machine Learning", "patterns", "relationships", "data", "labels"]
    },
    {
        "id": 6,
        "question": "What is deep learning?",
        "ideal_answer": "Deep learning is a subset of Machine Learning based on neural networks that mimic the human brain.",
        "key_concepts": ["subset", "Machine Learning", "neural networks", "human brain"]
    },
    {
        "id": 7,
        "question": "What are neural networks?",
        "ideal_answer": "Neural networks are computing systems inspired by the human brain, consisting of layers of nodes.",
        "key_concepts": ["computing systems", "human brain", "layers", "nodes"]
    },
    {
        "id": 8,
        "question": "What is natural language processing (NLP)?",
        "ideal_answer": "Natural Language Processing is a field of AI that focuses on the interaction between computers and human language.",
        "key_concepts": ["AI", "interaction", "computers", "human language", "NLP"]
    },
    {
        "id": 9,
        "question": "What is computer vision?",
        "ideal_answer": "Computer vision is a field of AI that enables computers to interpret and analyze visual data from the world.",
        "key_concepts": ["AI", "computers", "interpret", "analyze", "visual data"]
    },
    {
        "id": 10,
        "question": "What is the Turing Test?",
        "ideal_answer": "The Turing Test is a method to evaluate a machine's ability to exhibit intelligent behavior indistinguishable from a human.",
        "key_concepts": ["Turing Test", "evaluate", "machine", "intelligent behavior", "human"]
    },
    {
        "id": 11,
        "question": "What is reinforcement learning?",
        "ideal_answer": "Reinforcement learning is a type of Machine Learning where an agent learns to make decisions by interacting with the environment and receiving rewards or penalties.",
        "key_concepts": ["reinforcement learning", "Machine Learning", "agent", "decisions", "environment", "rewards", "penalties"]
    },
    {
        "id": 12,
        "question": "What are the ethical concerns in AI?",
        "ideal_answer": "Ethical concerns in AI include privacy, bias, accountability, transparency, and job displacement.",
        "key_concepts": ["ethics", "privacy", "bias", "accountability", "transparency", "job displacement"]
    },
    {
        "id": 13,
        "question": "What is the difference between AI and Machine Learning?",
        "ideal_answer": "AI is a broader concept focused on building intelligent systems, while Machine Learning is a subset of AI that uses data and algorithms to learn patterns.",
        "key_concepts": ["AI", "intelligent systems", "Machine Learning", "subset", "data", "algorithms", "patterns"]
    },
    {
        "id": 14,
        "question": "What is overfitting in Machine Learning?",
        "ideal_answer": "Overfitting is when a Machine Learning model performs well on training data but fails to generalize to new, unseen data.",
        "key_concepts": ["overfitting", "Machine Learning", "training data", "generalize", "unseen data"]
    },
    {
        "id": 15,
        "question": "What is the role of data preprocessing in Machine Learning?",
        "ideal_answer": "Data preprocessing involves cleaning and transforming raw data to make it suitable for Machine Learning models.",
        "key_concepts": ["data preprocessing", "cleaning", "transforming", "raw data", "suitable", "Machine Learning"]
    }
]


async def handle_connection(websocket, path):
    """Handles client connection and sends questions one by one."""
    try:
        for question in questions:
            # Send question to the client
            await websocket.send(json.dumps(question))
            print(f"Sent question: {question['question']}")

            # Wait for feedback or answer from the client
            response = await websocket.recv()
            print(f"Received feedback: {response}")

            # Send confirmation and prepare for the next question
            await websocket.send("Feedback received. Sending the next question...")
    except websockets.ConnectionClosed:
        print("Connection closed by the client.")
    except asyncio.TimeoutError:
        print("Request timed out.")

# Start WebSocket server
start_server = websockets.serve(handle_connection, "localhost", 8765)
print("Server started. Waiting for connections...")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
