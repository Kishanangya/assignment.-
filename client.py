import asyncio
import websockets
import json
from sentence_transformers import SentenceTransformer, util
from textblob import TextBlob
import re
import nltk



# Load the SentenceTransformer model for semantic similarity
model = SentenceTransformer('all-MiniLM-L6-v2')

def grade_answer(student_answer, question_data):
    """Grade the answer based on semantic similarity and key concepts."""
    ideal_answer = question_data["ideal_answer"]
    key_concepts = question_data["key_concepts"]

    # Step 1: Compute semantic similarity
    embeddings1 = model.encode(student_answer, convert_to_tensor=True)
    embeddings2 = model.encode(ideal_answer, convert_to_tensor=True)
    similarity_score = util.pytorch_cos_sim(embeddings1, embeddings2).item()

    # Step 2: Check for missing key concepts
    missing_concepts = [
        concept for concept in key_concepts if concept.lower() not in student_answer.lower()
    ]
    total_concepts = len(key_concepts)
    matched_concepts = total_concepts - len(missing_concepts)

    # Step 3: Penalize incomplete or keyword-only answers
    blob = TextBlob(student_answer)
    word_count = len(blob.words)
    sentence_count = len(blob.sentences)

    if word_count < 5 or sentence_count == 0:
        return {
            "score": 0,
            "feedback": "Your answer is incomplete. Please provide a more detailed response."
    }

# Detect keyword-only answers based on key_concepts
    key_concepts_in_answer = [
    concept for concept in key_concepts if concept.lower() in student_answer.lower()
    ]
    if len(key_concepts_in_answer) == len(key_concepts) and word_count <= len(key_concepts) + 2:
         return {
        "score": 0,
        "feedback": "Your answer seems to be a list of keywords or is incomplete. Please provide a detailed response with proper sentences."
    }

    # Step 4: Assign a score
    if similarity_score > 0.8:  # High similarity threshold
        score = 90 + (matched_concepts / total_concepts) * 10
        feedback = "Excellent! Your answer is highly relevant and accurate."
    elif similarity_score > 0.5:  # Moderate similarity threshold
        score = 50 + (matched_concepts / total_concepts) * 50
        feedback = (
            f"Good attempt! Your answer is relevant but could be improved. "
            f"Consider elaborating on: {', '.join(missing_concepts)}."
        )
    else:
        score = (matched_concepts / total_concepts) * 50
        feedback = (
            "Your answer is partially correct but needs improvement. "
            f"Focus on concepts like: {', '.join(missing_concepts)}."
        )

    # Step 5: Handle irrelevant answers
    if similarity_score < 0.3:  # Low similarity threshold
        return {
            "score": 0,
            "feedback": "Your answer is not relevant to the topic. Please try again."
        }

    return {"score": round(score, 2), "feedback": feedback}

async def websocket_client():
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                # Receive the question from the server
                question_data = await websocket.recv()
                question = json.loads(question_data)
                print(f"Question: {question['question']}")

                # Simulate the student's answer (or use input here)
                student_answer = input(f"Your Answer to '{question['question']}': ")

                # Grade the answer based on the new logic
                feedback = grade_answer(student_answer, question)
                print(f"Feedback: {feedback}")

                # Send feedback to the server
                await websocket.send(json.dumps({
                    "question_id": question["id"],
                    "student_answer": student_answer,
                    "grading_feedback": feedback
                }))

                # Receive confirmation from the server
                confirmation = await websocket.recv()
                print(f"Server: {confirmation}")
                
    except websockets.ConnectionClosed:
        print("Connection closed.")
    except asyncio.TimeoutError:
        print("Request timed out.")

# Run the WebSocket client
asyncio.run(websocket_client())
