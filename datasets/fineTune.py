import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import json

# Base URLs
base_url = "https://www.aldiwan.net/sea-%D8%A7%D9%84%D9%88%D8%A7%D9%81%D8%B1.html?page="
poem_base_url = "https://www.aldiwan.net/"
traget_sea="الوافر"
# Range of pages to scrape
start_page = 1
end_page = 2
conversation_list = []
# Choices for each question

# Counter for unique ID generation
# question_id = 2000


# List of strings
# options = [
#     "أحذ الكامل", "أحذ المديد", "أحذ الوافر", "البسيط", "التفعيله", "الخبب", "الخفيف", "الدوبيت",
#     "الرجز", "الرمل", "السريع", "السلسلة", "الطويل", "القوما", "الكامل", "الكامل المقطوع",
#     "المتدارك", "المتدارك المنهوك", "المتقارب", "المجتث", "المديد", "المضارع", "المقتضب", "المنسرح",
#     "المواليا", "الهزج", "الوافر", "تفعيلة الرجز", "تفعيلة الرمل", "تفعيلة الكامل", "تفعيلة المتقارب",
#     "مجزوء البسيط", "مجزوء الخفيف", "مجزوء الدوبيت", "مجزوء الرجز", "مجزوء الرمل", "مجزوء السريع",
#     "مجزوء الطويل", "مجزوء الكامل", "مجزوء المتدارك", "مجزوء المتقارب", "مجزوء المجتث", "مجزوء المديد",
#     "مجزوء المقتضب", "مجزوء المنسرح", "مجزوء المواليا", "مجزوء الهزج", "مجزوء الوافر", "مجزوء موشح",
#     "مخلع البسيط", "مخلع الرجز", "مخلع الرمل", "مخلع السريع", "مخلع الكامل", "مخلع موشح", "مربع البسيط",
#     "مربع الرجز", "مشطور الرجز", "مشطور السريع", "مشطور الطويل", "منهوك البسيط", "منهوك الرجز",
#     "منهوك الكامل", "منهوك المنسرح", "موشح"
# ]

# def get_random_option(exclude=None):
#     """
#     Returns a random value from the list, excluding the specified option if provided.
    
#     Parameters:
#     exclude (str): The value to exclude from being chosen.
    
#     Returns:
#     str: A randomly selected value from the list.
#     """
#     available_options = [option for option in options if option != exclude]
#     return random.choice(available_options)

# Example usage:
# random_option = get_random_option(exclude="الكامل")
# print(f"Random option (excluding 'أحذ الكامل'): {random_option}")

# Open CSV file for writing
with open("poems_data1.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["id", "question", "choices", "answerKey","source"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Loop through each page
    for page_num in range(start_page, end_page + 1):
        # Construct page URL
        page_url = f"{base_url}{page_num}"
        print(f"Scraping page: {page_url}")
        
        # Request and parse page content
        page_response = requests.get(page_url)
        page_soup = BeautifulSoup(page_response.content, 'html.parser')
        
        # Find all the <div class="record col-12"> elements
        records = page_soup.find_all("div", class_="record col-12")
        
        # Loop through each record to extract links
        for record in records:
            poem_link_tag = record.find("a", class_="float-right")
            
            if poem_link_tag:
                poem_relative_url = poem_link_tag.get("href")
                poem_url = poem_base_url + poem_relative_url
                
                # Request and parse the poem page
                poem_response = requests.get(poem_url)
                poem_soup = BeautifulSoup(poem_response.content, 'html.parser')
                
                # Extract all <h3> elements from the main content div
                main_div = poem_soup.find('div', {"id": 'poem_content'})
                if main_div:
                    h3_elements = [h3.get_text(strip=True) for h3 in main_div.find_all("h3")]
                    for i in range(0, len(h3_elements) - 1, 2):  # Step by 2
                        h3_text_current = h3_elements[i]
                        h3_text_next = h3_elements[i + 1]
                        
                        # Update question to include both h3_text_current and h3_text_next
                        question = f'''ما هو البحر الشعري لهذا البيت
                        {h3_text_current} - {h3_text_next}?'''
                        answer=traget_sea
                        conversation = {
                        "messages": [
                            {"role": "system", "content": "انت مساعد شخصي تستطيع معرفة البحر الشعري لاي بيت شعر؟"},
                            {"role": "user", "content": question},
                            {"role": "assistant", "content":answer}
                            ]
                        }
                        print(question)
                        conversation_list.append(conversation)
                        # choices = {
                        #     "text": [
                        #         traget_sea,
                        #         get_random_option(exclude=traget_sea),
                        #         get_random_option(exclude=traget_sea),
                        #         get_random_option(exclude=traget_sea)
                        #     ],
                        #     "label": ["A", "B", "C", "D"]
                        # }
                        # answer_key = "A"

                        # writer.writerow({
                        #     "id": question_id,
                        #     "question": question,
                        #     "choices": choices,
                        #     "answerKey": answer_key,
                        #     "source":poem_url
                        # })
                        # print(question_id)

                        # question_id += 2  # Increment question_id by 2

                    # for h3_text in h3_elements:
                    #     choices = {
                    #     "text": ["الكامل",get_random_option(exclude="الكامل"), get_random_option(exclude="الكامل"), get_random_option(exclude="الكامل")],
                    #     "label": ["A", "B", "C", "D"]
                    # }
                    #     answer_key = "A"
                    #     question='''ما هو البحر الشعري لهذا البيت
                    #     {h3_text}?'''
                    #     writer.writerow({
                    #         "id": question_id,
                    #         "question": question,
                    #         "choices": choices,
                    #         "answerKey": answer_key
                    #     })
                    #     question_id += 1
                
                # Wait to avoid overwhelming the server
                time.sleep(1)

print("Scraping complete. Data saved to poems_data.csv")
with open("poems_data_1.json", 'w') as f:
    for conversation in conversation_list:
        json.dump(conversation, f)
        f.write('\n')
# import pandas as pd
# import ast
# import json
# from tqdm import tqdm

# def ibm_llm(model, csv_file, max_samples=1000, output_file='output.json'):
#     # Load data from the CSV file
#     data = pd.read_csv(csv_file)

#     # Initialize a list to store the conversation messages
#     conversation_list = []

#     # Select a subset of the data based on max_samples
#     for i, example in tqdm(data.iterrows(), total=min(max_samples, len(data)), desc="Evaluating IBM WatsonX AI LLM"):
#         if i >= max_samples:
#             break
            
#         question = example['question']
#         # Safely evaluate the string representation of the dictionary
#         choices_dict = ast.literal_eval(example['choices'])
#         choices = choices_dict['text']
#         correct_answer = example['answerKey'].strip().upper()  # Normalize the correct answer

#         # Prepare the prompt for the LLM
#         prompt_input = f"""
# You are an AI assistant created from text json response for finetuning.
# User: {question}
# """
        
#         try:
#             generated_response = model.generate_text(prompt=prompt_input, guardrails=False)
#             # Store messages in the required JSON format
#             conversation = {
#                 "messages": [
#                     {"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."},
#                     {"role": "user", "content": question},
#                     {"role": "assistant", "content": generated_response.strip()}
#                 ]
#             }
#             conversation_list.append(conversation)

#         except Exception as e:
#             print(f"Error generating text for example {i + 1}: {e}")
#             continue

#     # Save all conversations to a JSON file
#     with open(output_file, 'w') as f:
#         for conversation in conversation_list:
#             json.dump(conversation, f)
#             f.write('\n')  # Write a newline for separation

# # Example usage
# # ibm_llm(your_model_instance, 'your_file.csv', max_samples=1000, output_file='output.json')
