import threading

from flask import Flask, request, jsonify, send_file
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the pre-trained model
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Flask app setup
print("Enter your authtoken, which can be copied from https://dashboard.ngrok.com/get-started/your-authtoken")
# conf.get_default().auth_token = getpass.getpass()

app = Flask(__name__,
            static_url_path='/',
            static_folder='../frontend/build',
            )

# Open a ngrok tunnel to the HTTP server
# public_url = ngrok.connect(5000).public_url
# print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:5000/\"")

# Update the app's base URL to use the public ngrok URL
# app.config["BASE_URL"] = public_url

# Function to calculate cosine similarity
def calculate_cosine_similarity(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]

# Function to split text by semantic similarity
def split_text_by_semantic_similarity(text, threshold):
    sentences = text.split('.')
    embeddings = model.encode(sentences)

    grouped_sentences = []
    current_group = [sentences[0]]

    for i in range(1, len(sentences)):
        sim = calculate_cosine_similarity(embeddings[i-1], embeddings[i])
        if sim < threshold:
            grouped_sentences.append(' '.join(current_group))
            current_group = [sentences[i]]
        else:
            current_group.append(sentences[i])

    grouped_sentences.append(' '.join(current_group))
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

# Start the Flask server in a new thread
threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()
