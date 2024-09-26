import getpass
import os
import threading
from flask import Flask, request, jsonify,render_template_string
# from pyngrok import ngrok, conf
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

# Load the pre-trained model
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Flask app setup
print("Enter your authtoken, which can be copied from https://dashboard.ngrok.com/get-started/your-authtoken")
# conf.get_default().auth_token = getpass.getpass()

app = Flask(__name__)

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
# def index():
#     return jsonify({
#     "grouped_sentences": ["\u062a\u0644\u0645\u062d\u062a \u0639\u0644\u0649 \u062e\u0644\u0642 \u0643\u062b\u064a\u0631 \u0645\u0646 \u0627\u0644\u0646\u0627\u0633 \u0625\u0647\u0645\u0627\u0644 \u0623\u0628\u062f\u0627\u0646\u0647\u0645\u060c \u0641\u0645\u0646\u0647\u0645 \u0645\u0646 \u0644\u0627 \u064a\u0646\u0638\u0641 \u0641\u0645\u0647 \u0628\u0627\u0644\u062e\u0644\u0627\u0644\u0661 \u0628\u0639\u062f \u0627\u0644\u0623\u0643\u0644\u060c \u0648\u0645\u0646\u0647\u0645 \u0645\u0646 \u0644\u0627 \u064a\u0646\u0642\u064a \u064a\u062f\u064a\u0647 \u0641\u064a \u063a\u0633\u0644\u0647\u0645\u0627 \u0645\u0646 \u0627\u0644\u0632\u0647\u0645\u0662\u060c \u0648\u0645\u0646\u0647\u0645 \u0645\u0646 \u0644\u0627 \u064a\u0643\u0627\u062f \u064a\u0633\u062a\u0627\u0643\u060c \u0648\u0641\u064a\u0647\u0645 \u0645\u0646 \u0644\u0627 \u064a\u0643\u062a\u062d\u0644\u060c \u0648\u0641\u064a\u0647\u0645 \u0645\u0646 \u0644\u0627 \u064a\u0631\u0627\u0639\u064a \u0627\u0644\u0625\u0628\u0637 \u0625\u0644\u0649 \u063a\u064a\u0631 \u0630\u0644\u0643\u060c \u0641\u064a\u0639\u0648\u062f \u0647\u0630\u0627 \u0627\u0644\u0625\u0647\u0645\u0627\u0644 \u0628\u0627\u0644\u062e\u0644\u0644 \u0641\u064a \u0627\u0644\u062f\u064a\u0646 \u0648\u0627\u0644\u062f\u0646\u064a\u0627", " \u0641\u064a \u0627\u0644\u0628\u062f\u0627\u064a\u0629 \u0645\u0646 \u0627\u0644\u0645\u0647\u0645 \u062c\u062f\u0627\u064b \u0645\u0639\u0631\u0641\u0629 \u0627\u0644\u0637\u0631\u064a\u0642\u0629 \u0627\u0644\u0623\u0641\u0636\u0644 \u0644\u062a\u0646\u0638\u064a\u0641 \u0639\u064a\u0648\u0646 \u0627\u0644\u063a\u0627\u0632 \u0648\u0627\u0644\u0641\u0631\u0646 \u0628\u0634\u0643\u0644 \u0639\u0627\u0645\u060c \u0648\u0630\u0644\u0643 \u0644\u062a\u0641\u0627\u062f\u064a \u0627\u0644\u062a\u0633\u0628\u0628 \u0628\u062a\u0644\u0641\u0647\u060c \u0648\u0644\u0647\u0630\u0627 \u064a\u064f\u0646\u0635\u062d \u0628\u0642\u0631\u0627\u0621\u0629 \u062f\u0644\u064a\u0644 \u0625\u0631\u0634\u0627\u062f\u0627\u062a \u0627\u0644\u0627\u0633\u062a\u0639\u0645\u0627\u0644\u060c \u0642\u0628\u0644 \u062a\u0646\u0638\u064a\u0641 \u0627\u0644\u0639\u064a\u0648\u0646\u060c \u0644\u0644\u062a\u0623\u0643\u062f \u0645\u0646 \u0637\u0631\u064a\u0642\u0629 \u0627\u0644\u062a\u0646\u0638\u064a\u0641 \u0627\u0644\u0623\u0641\u0636\u0644 \u0648\u0644\u0645\u0639\u0631\u0641\u0629 \u0625\u0630\u0627 \u0643\u0627\u0646 \u0645\u0646 \u0627\u0644\u0645\u0645\u0643\u0646 \u0625\u0632\u0627\u0644\u0629 \u0627\u0644\u0639\u064a\u0648\u0646 \u0628\u0634\u0643\u0644 \u0643\u0627\u0645\u0644 \u0644\u062a\u0646\u0638\u064a\u0641\u0647\u0627 \u0623\u0645 \u0644\u0627", " \u0641\u0642\u062f \u0623\u0639\u0644\u0646\u062a \u062c\u0645\u0627\u0639\u0629 \u062d\u0632\u0628 \u0627\u0644\u0644\u0647 \u0627\u0644\u0644\u0628\u0646\u0627\u0646\u064a \u0627\u0633\u062a\u0647\u062f\u0627\u0641 \u0627\u0644\u0642\u0627\u0639\u062f\u0629 \u0627\u0644\u0623\u0633\u0627\u0633\u064a\u0629 \u0644\u0644\u062f\u0641\u0627\u0639 \u0627\u0644\u062c\u0648\u064a \u0627\u0644\u0635\u0627\u0631\u0648\u062e\u064a \u0627\u0644\u062a\u0627\u0628\u0639 \u0644\u0642\u064a\u0627\u062f\u0629 \u0627\u0644\u0645\u0646\u0637\u0642\u0629 \u0627\u0644\u0634\u0645\u0627\u0644\u064a\u0629 \u0641\u064a \u062b\u0643\u0646\u0629 \u0628\u064a\u0631\u064a\u0627 \u0628\u0631\u0634\u0642\u0629 \u0645\u0646 \u200f\u0635\u0648\u0627\u0631\u064a\u062e \u0627\u0644\u0643\u0627\u062a\u064a\u0648\u0634\u0627", " \u0641\u064a \u062d\u064a\u0646 \u0623\u0643\u062f\u062a \u0648\u0633\u0627\u0626\u0644 \u0625\u0639\u0644\u0627\u0645 \u0625\u0633\u0631\u0627\u0626\u0644\u064a\u064a\u0629\u060c \u0641\u062c\u0631 \u0627\u0644\u062c\u0645\u0639\u0629\u060c \u0627\u0646\u0642\u0637\u0627\u0639 \u0627\u0644\u062a\u064a\u0627\u0631 \u0627\u0644\u0643\u0647\u0631\u0628\u0627\u0626\u064a \u0641\u064a \u0635\u0641\u062f \u0648\u0628\u0644\u062f\u0629 \u0628\u064a\u0631\u064a\u0627 \u0641\u064a \u0627\u0644\u062c\u0644\u064a\u0644 \u0627\u0644\u0623\u0639\u0644\u0649 \u0628\u0639\u062f \u0625\u0637\u0644\u0627\u0642 \u0631\u0634\u0642\u0629 \u0635\u0648\u0627\u0631\u064a\u062e \u0645\u0646 \u0644\u0628\u0646\u0627\u0646", " \u0643\u0645\u0627 \u0630\u0643\u0631\u062a \u0627\u0646\u062f\u0644\u0627\u0639 \u062d\u0631\u064a\u0642 \u0643\u0628\u064a\u0631 \u0641\u064a \u063a\u0627\u0628\u0629 \u0628\u064a\u0631\u064a\u0627 \u0628\u0639\u062f \u0625\u0637\u0644\u0627\u0642 \u0645\u0648\u062c\u0629 \u0643\u0628\u064a\u0631\u0629 \u0645\u0646 \u0627\u0644\u0635\u0648\u0627\u0631\u064a\u062e \u0645\u0646 \u0644\u0628\u0646\u0627\u0646", ""]
# })
def index():
    # Inline HTML template
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Text Splitter</title>
        <style>
            .sentence {
                padding: 5px;
                font-size: 18px;
                margin: 5px 0;
            }
            /* Define a few colors to alternate */
            .color1 { color: #ff6347; }  /* Tomato */
            .color2 { color: #4682b4; }  /* SteelBlue */
            .color3 { color: #32cd32; }  /* LimeGreen */
            .color4 { color: #ffa500; }  /* Orange */
            .loading { font-size: 16px; color: blue; }
        </style>
    </head>
    <body>

        <h1>Text Semantic Splitter</h1>
        <textarea id="inputText" rows="10" cols="80" placeholder="Enter your text here..."></textarea>
        <br><br>
        <label for="threshold">Threshold: <span id="thresholdValue">0.30</span></label>
        <input type="range" id="threshold" min="0.1" max="1.0" step="0.01" value="0.30" oninput="updateThreshold()">
        <br><br>
        <button onclick="submitText()">Submit</button>

        <div id="loading" class="loading" style="display: none;">Loading...</div>

        <h2>Grouped Sentences:</h2>
        <div id="result"></div>

        <script>
            let currentThreshold = 0.30;

            // Function to update threshold value from slider
            function updateThreshold() {
                currentThreshold = document.getElementById('threshold').value;
                document.getElementById('thresholdValue').innerText = currentThreshold;
                submitText();  // Automatically refresh results when threshold changes
            }

            // Function to handle the button click and interact with the API
            function submitText() {
                const text = document.getElementById("inputText").value;
                const apiUrl = "/api/split_text";
                const resultDiv = document.getElementById("result");
                const loadingDiv = document.getElementById("loading");
                
                // Show loading indicator
                loadingDiv.style.display = 'block';

                fetch(apiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        text: text,
                        threshold: currentThreshold  // Use the dynamic threshold
                    })
                })
                .then(response => response.json())
                .then(data => {
                    resultDiv.innerHTML = "";  // Clear previous results
                    const sentences = data.grouped_sentences;
                    let colorClass = 1;

                    sentences.forEach(sentence => {
                        const span = document.createElement("span");
                        span.textContent = sentence;
                        span.className = `sentence color${colorClass}`;
                        resultDiv.appendChild(span);
                        resultDiv.appendChild(document.createElement("br"));
                        colorClass = (colorClass % 4) + 1;  // Cycle through color classes
                    });

                    // Hide loading indicator after results are displayed
                    loadingDiv.style.display = 'none';
                })
                .catch(error => {
                    console.error('Error:', error);
                    // Hide loading indicator on error
                    loadingDiv.style.display = 'none';
                });
            }
        </script>

    </body>
    </html>


    ''')
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