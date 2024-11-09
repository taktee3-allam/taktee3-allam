# from datasets import load_dataset
# from sentence_transformers import SentenceTransformer
# import numpy as np
# import torch
# from tqdm import tqdm
import requests
from ibm_watsonx_ai.foundation_models import Model
import pandas as pd
from tqdm import tqdm
import ast
google_gemini_api_key="AIzaSyBaD_IKzag8NpHEnn5y4dcHz7bPQzfQbpA"
csv_file="poems_data2.csv"
def get_ibm_credentials():
    """
    Retrieve IBM WatsonX AI credentials from environment variables.
    """
    return {
        "url" : "https://eu-de.ml.cloud.ibm.com",
		"apikey" : "sUXUX4iNrOIeA3CVar3LLNqMnxMMkLht4lkJ7SM4Jare"
    }

def initialize_ibm_watsonx_model():
    """
    Initialize the IBM WatsonX AI LLM.
    """
    model_id = "sdaia/allam-1-13b-instruct"
    parameters = {
        "decoding_method": "greedy",
        "max_new_tokens": 900,
        "repetition_penalty": 1
    }
    project_id = "3f3e8a02-628e-4736-920e-130b2b284414"
    # space_id is not used in the Model initialization; remove if unnecessary

    model = Model(
        model_id=model_id,
        params=parameters,
        credentials=get_ibm_credentials(),
        project_id=project_id
    )
    return model
def generate_gemini_response(prompt, api_key):
    """
    Send a prompt to the Google Gemini API and retrieve the response.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        result = response.json()
        
        # Extract the generated text from the response
        # The exact path may vary based on the API's response structure
        # generated_text = result.get('contents', [{}])[0].get('parts', [{}])[0].get('text', '')
        generated_text=result['candidates'][0]['content']['parts'][0]['text'].replace(".",'').replace("*","")
        # print("result",generated_text)
        return generated_text
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Google Gemini API: {e}")
        return ""

def evaluate_google_gemini(api_key, csv_file, max_samples):
    data = pd.read_csv(csv_file)
    if api_key == "YOUR_GOOGLE_API_KEY":
        print("Google Gemini API key is not set. Skipping Google Gemini evaluation.")
        return None

    correct = 0
    total = 0

    for i, example in tqdm(data.iterrows(), total=min(max_samples, len(data)), desc="Evaluating GOOGLE Gemini LLM"):
        if i >= max_samples:
            break
        question = example['question']
        choices_dict = ast.literal_eval(example['choices'])
        choices = choices_dict['text']
        correct_answer = example['answerKey'].strip().upper() 
        # choices = example['choices']['text']  # List of answer choices
        # correct_answer = example['answerKey']  # e.g., 'A', 'B', 'C', 'D'

        # Prepare the prompt for the LLM
        prompt_input = f"""
You are an AI assistant that selects the correct answer to multiple-choice questions.
Question: {question}
Choices:
A. {choices[0] if len(choices) > 0 else ''}
B. {choices[1] if len(choices) > 1 else ''}
C. {choices[2] if len(choices) > 2 else ''}
D. {choices[3] if len(choices) > 3 else ''}
Please provide only the letter (A, B, C, or D) of the correct answer.
"""
        print(f"prompt_input: {prompt_input}")
        try:
            generated_response = generate_gemini_response(prompt_input, api_key)
            if not generated_response:
                print(f"No response for example {total + 1}. Skipping.")
                continue
            # Extract the first letter from the response
            predicted_answer = generated_response
            print(f"predicted answer: {predicted_answer}")
            print(f"Correct answer: {correct_answer}")
            if predicted_answer == correct_answer:
                correct += 1
            total += 1
            print("correct",correct)
        except Exception as e:
            print(f"Error generating text for example {total + 1}: {e}")
            continue

    if total == 0:
        return 0

    accuracy = correct / total
    return accuracy
def evaluate_ibm_llm(model, csv_file, max_samples=10):
    # Load data from the CSV file
    data = pd.read_csv(csv_file)

    correct = 0
    total = 0

    # Select a subset of the data based on max_samples
    for i, example in tqdm(data.iterrows(), total=min(max_samples, len(data)), desc="Evaluating IBM WatsonX AI LLM"):
        if i >= max_samples:
            break
            
        question = example['question']
        # Safely evaluate the string representation of the dictionary
        choices_dict = ast.literal_eval(example['choices'])
        choices = choices_dict['text']
        correct_answer = example['answerKey'].strip().upper()  # Normalize the correct answer

        # Prepare the prompt for the LLM
        prompt_input = f"""
You are an AI assistant that selects the correct answer to multiple-choice questions.
Question: {question}
Choices:
A. {choices[0] if len(choices) > 0 else ''}
B. {choices[1] if len(choices) > 1 else ''}
C. {choices[2] if len(choices) > 2 else ''}
D. {choices[3] if len(choices) > 3 else ''}
Please provide only the letter (A, B, C, or D) of the correct answer.
"""
        
        try:
            generated_response = model.generate_text(prompt=prompt_input, guardrails=False)
            # Extract the first letter from the response
            predicted_answer = generated_response.strip().upper()[0]
            print(predicted_answer)
            if predicted_answer == correct_answer:
                correct += 1
            total += 1
        except Exception as e:
            print(f"Error generating text for example {total + 1}: {e}")
            continue

    accuracy = correct / total if total > 0 else 0
    return accuracy

# ibm_llm_model = initialize_ibm_watsonx_model()
# print("\nEvaluating IBM WatsonX AI LLM...")
# ibm_llm_accuracy = evaluate_ibm_llm(ibm_llm_model, "poems_data.csv", max_samples=10)
# print(f"Accuracy for IBM WatsonX AI LLM ({ibm_llm_model.model_id}): {ibm_llm_accuracy*100:.2f}%")
print("\nEvaluating Google Gemini LLM...")
gemini_accuracy = evaluate_google_gemini(google_gemini_api_key, csv_file, max_samples=10)
if gemini_accuracy is not None:
    print(f"Accuracy for Google Gemini LLM (gemini-1.5-flash-latest): {gemini_accuracy*100:.2f}%")
    # Evaluate Google
# def evaluate_ibm_llm(model, data, max_samples=1000):
#         correct = 0
#         total = 0

#         for example in tqdm(data.select(range(max_samples)), desc="Evaluating IBM WatsonX AI LLM"):
#             question = example['question']
#             choices = example['choices']['text']  # List of answer choices
#             correct_answer = example['answerKey']  # e.g., 'A', 'B', 'C', 'D'

#             # Prepare the prompt for the LLM
#             # Format the prompt to instruct the model to choose the correct answer
#             prompt_input = f"""
# You are an AI assistant that selects the correct answer to multiple-choice questions.
# Question: {question}
# Choices:
# A. {choices[0]}
# B. {choices[1]}
# C. {choices[2]}
# D. {choices[3]}
# Please provide only the letter (A, B, C, or D) of the correct answer.
# """

#             try:
#                 generated_response = model.generate_text(prompt=prompt_input, guardrails=False)
#                 # Extract the first letter from the response
#                 predicted_answer = generated_response.strip().upper()[0]
#                 if predicted_answer == correct_answer.upper():
#                     correct += 1
#                 total += 1
#             except Exception as e:
#                 print(f"Error generating text for example {total + 1}: {e}")
#                 continue

#         accuracy = correct / total if total > 0 else 0
#         return accuracy
