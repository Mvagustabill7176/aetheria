import os
import openai
from flask import Flask, request, jsonify

# Load your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Route to test the app
@app.route("/")
def index():
    return "Aetheria backend is running."

# Route where you send emotional text and get a summary back
@app.route("/summarize", methods=["POST"])
def summarize():
    user_input = request.json.get("text", "")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a reflective AI companion."},
            {"role": "user", "content": f"Summarize this emotional pattern: {user_input}"}
        ],
        temperature=0.7,
        max_tokens=500
    )

    summary = response.choices[0].message["content"]
    return jsonify({"summary": summary})

from flask import Flask, request, jsonify, render_template
import uuid

app = Flask(__name__, template_folder='templates')

user_db = {}
initial_questions = [
    "What core beliefs define your understanding of the world?",
    "Describe a moment where you felt truly seen or understood.",
    "What emotions visit you most often?",
    "What do you feel your purpose is right now?",
    "What limiting thoughts or patterns would you like to change?"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    user_id = str(uuid.uuid4())
    user_db[user_id] = {"answers": [], "current_question": 0}
    return jsonify({"user_id": user_id, "question": initial_questions[0]})

@app.route('/interact', methods=['POST'])
def interact():
    data = request.json
    user_id = data.get("user_id")
    answer = data.get("answer")
    if user_id not in user_db:
        return jsonify({"error": "Invalid user ID."}), 404
    profile = user_db[user_id]
    profile["answers"].append(answer)
    profile["current_question"] += 1
    if profile["current_question"] < len(initial_questions):
        return jsonify({"next_question": initial_questions[profile["current_question"]], "complete": False})
    else:
        insight = "This is a placeholder insight from GPT."  # Replace with real GPT call
        return jsonify({"complete": True, "insight": insight})
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

