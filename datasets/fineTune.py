import pandas as pd
import ast
import json
from tqdm import tqdm

def ibm_llm(model, csv_file, max_samples=1000, output_file='output.json'):
    # Load data from the CSV file
    data = pd.read_csv(csv_file)

    # Initialize a list to store the conversation messages
    conversation_list = []

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
You are an AI assistant created from text json response for finetuning.
User: {question}
"""
        
        try:
            generated_response = model.generate_text(prompt=prompt_input, guardrails=False)
            # Store messages in the required JSON format
            conversation = {
                "messages": [
                    {"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."},
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": generated_response.strip()}
                ]
            }
            conversation_list.append(conversation)

        except Exception as e:
            print(f"Error generating text for example {i + 1}: {e}")
            continue

    # Save all conversations to a JSON file
    with open(output_file, 'w') as f:
        for conversation in conversation_list:
            json.dump(conversation, f)
            f.write('\n')  # Write a newline for separation

# Example usage
# ibm_llm(your_model_instance, 'your_file.csv', max_samples=1000, output_file='output.json')
