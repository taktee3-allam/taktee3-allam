# If you're not utilizing OpenAI models, assign a placeholder string (e.g., "not_used").
import os
from raptor import RetrievalAugmentation 
RA = RetrievalAugmentation()

os.environ["OPENAI_API_KEY"] = "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"
# Cinderella story defined in sample.txt
with open('samples.txt', 'r') as file:
    text = file.read()

print(text[:100])



# construct the tree
RA.add_documents(text)

question = "وَرُبَّ ++++ وَفَيتَ لَهُ بِحَقٍّ? contine the text"

answer = RA.answer_question(question=question)

print("Answer: ", answer)

SAVE_PATH = "cinderella"
RA.save(SAVE_PATH)

RA = RetrievalAugmentation(tree=SAVE_PATH)

answer = RA.answer_question(question=question)
print("Answer: ", answer)