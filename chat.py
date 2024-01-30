import json
from difflib import get_close_matches

def load(file_path:str)->dict:
    with open(file_path,'r') as file:
        data:dict=json.load(file)
    return data


def save(file_path:str,data:dict):
    with open(file_path,'w') as file:
        json.dump(data,file,indent=2)


def match(usr_qust:str,qust:str)->str | None:
    matches:list=get_close_matches(usr_qust,qust,n=1,cutoff=0.6)

    return matches[0] if matches else None

def pick_answer(qust:str,json_dict:dict)-> str | None:
    for a in json_dict["questions"]:
        if a["question"] == qust:
            return a["answer"]
        
def chat_bot():
    qa:dict=load('intents.json')

    while True:
        user_input:str= input("You: ")

        if user_input.lower()=='quit':
            break

        best_match: str | None=match(user_input,[q["question"] for q in qa["questions"]])

        if best_match:
            answer: str =pick_answer(best_match,qa)
            print(f'Bot:{answer}')
        else :
            print('Bot: I don\'t know the answer.Can you teach ')

            new_answer:str=input('Type the answer or "skip" to skip')

            if new_answer.lower != 'skip':
                qa["questions"].append({ "question":user_input,"answer":new_answer})
                save('intents.json',qa)
                print('Thank you! I learnt a new response')


if __name__ == '__main__':

    chat_bot()