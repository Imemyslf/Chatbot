import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent = 2)
        
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n = 1, cutoff= 0.7)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["questions"] == question:
            return q["answer"]

def chat_bot(message_1):
    knowledge_base: dict = load_knowledge_base('Files/knowledge_base.json')
    user_input: str = message_1
    
    if user_input.lower() == 'quit':
        list = ["False"]
        return list
    
    best_match: str | None = find_best_match(user_input, [q["questions"] for q in knowledge_base["questions"]])
    if best_match:
        answer: str = get_answer_for_question(best_match, knowledge_base)
        return f'{answer}'
    else:
        lost = ['Bot: I don\'t know the answer. Can you teach me?',user_input,2]
        return lost
    
def response(question, new_answer):
    knowledge_base: dict = load_knowledge_base('Files/knowledge_base.json')
    # new_answer: str = input('Type the answer or "skip" to skip: ')
    question = question.lower()
    if new_answer.lower() != "skip":
        knowledge_base["questions"].append({"questions": question, "answer": new_answer})
        save_knowledge_base('Files/knowledge_base.json', knowledge_base)  # Save the updated knowledge base
        return 'Bot: Thank you! I learned a new response.'


                
if __name__ == '__main__':
     chat_bot()
    