import threading

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from ibm_watsonx_ai.foundation_models import Model

# Load the pre-trained model
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Flask app setup
print("Enter your authtoken, which can be copied from https://dashboard.ngrok.com/get-started/your-authtoken")
# conf.get_default().auth_token = getpass.getpass()

app = Flask(__name__,
            static_url_path='/',
            static_folder='../frontend/build',
            )

CORS(app)

# Open a ngrok tunnel to the HTTP server
# public_url = ngrok.connect(5000).public_url
# print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:5000/\"")

# Update the app's base URL to use the public ngrok URL
# app.config["BASE_URL"] = public_url

# Function to calculate cosine similarity
def calculate_cosine_similarity(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]

def embeddings_average(embeddings: list[list[float]]) -> list[float]:
    return [float(sum(col) / len(col)) for col in zip(*embeddings)]

# Function to split text by semantic similarity
def split_text_by_semantic_similarity(text, threshold):
    sentences = text.split('.')
    embeddings = model.encode(sentences)

    grouped_sentences = []
    current_group = [(sentences[0], embeddings[0])]

    for i in range(1, len(sentences)):
        sim = calculate_cosine_similarity(embeddings[i-1], embeddings[i])
        if sim < threshold:
            grouped_sentences.append({'sentence': ' '.join(group[0] for group in current_group), 'embedding': embeddings_average([group[1] for group in current_group])})
            current_group = [(sentences[i], embeddings[i])]
        else:
            current_group.append((sentences[i], embeddings[i]))

    grouped_sentences.append({'sentence': ' '.join(group[0] for group in current_group), 'embedding': embeddings_average([group[1] for group in current_group])})
    return grouped_sentences

@app.route("/")
def index():
    return send_file('../frontend/build/index.html')

# Flask route to handle POST requests
@app.route("/api/split_text", methods=["POST"])
def split_text():
    data = request.get_json()
    text = data.get("text", "")
    threshold = float(data.get("threshold",0.90))

    if not text:
        return jsonify({"error": "No text provided"}), 400

    grouped_sentences = split_text_by_semantic_similarity(text, threshold)
    return jsonify({"grouped_sentences": grouped_sentences})

ibm_creds = {
    "url" : "https://eu-de.ml.cloud.ibm.com",
    "apikey" : "sUXUX4iNrOIeA3CVar3LLNqMnxMMkLht4lkJ7SM4Jare"
}
model_parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 900,
    "repetition_penalty": 1
}
ibm_model = Model(
    project_id = "3f3e8a02-628e-4736-920e-130b2b284414",
    model_id = "sdaia/allam-1-13b-instruct",
    params = model_parameters,
    credentials = ibm_creds,
)

@app.route("/api/prompt", methods=["POST"])
def prompt_ibm():
    data = request.get_json()
    use_taqtee3 = data.get("useTaqtee3", False)
    prompt = data.get("prompt", "")

    if use_taqtee3:
        # TODO: fill actual addition to the prompt
        prompt = f"Answer this prompt: {prompt}"

    generated_response = ibm_model.generate_text(prompt=prompt, guardrails=False)
    return jsonify({"response": generated_response})

# Start the Flask server in a new thread
threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()
