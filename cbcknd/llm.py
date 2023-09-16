import openai
import prompt_templates
from datetime import date
from response_model import ResponseModel


def get_initial_training_plan(user_profile, blocked_time_slots=[]):
    input_data = {
        "personal_data": user_profile.__dict__,
        "time": {"current_date": date.today(), "blocked_time_slots": blocked_time_slots},
    }
    prompt = prompt_templates.build_initial_prompt(input_data)
    reponse = ResponseModel(ask_llm(prompt))
    return reponse


def get_updated_training_plan(user_profile, user_message, last_response, whoop_update={}, blocked_time_slots=[]):
    input_data = {
        "personal_data": user_profile.__dict__,
        "time": {"current_date": date.today(), "blocked_time_slots": blocked_time_slots},
        "user_message": user_message,
        "training_plan": last_response.get_trainings_plan(),
        "whoop_update": whoop_update
    }
    prompt = prompt_templates.build_update_prompt(input_data)
    reponse = ResponseModel(ask_llm(prompt))
    return reponse


def ask_llm(prompt):
    openai.api_key = "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"
    output = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
    return output["choices"][0]["message"]["content"]


if __name__ == "__main__":
    response = ask_llm(prompt_templates.build_update_prompt())
    print(response)
   


