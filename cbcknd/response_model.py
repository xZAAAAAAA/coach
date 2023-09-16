
import json

class ResponseModel:

    def __init__(self, response_str):
        response_dict = json.loads(response_str)
        self.training_plan_title = response_dict["training_plan_title"]
        self.summary = response_dict["summary"]
        self.explanation = response_dict["explanation"]
        self.workouts = response_dict["workouts"]
        self.change_training_plan = response_dict["change_training_plan"] if "change_training_plan" in response_dict else None
        self.change_reason = response_dict["change_reason"] if "change_reason" in response_dict else ""
        self.change_data_source = response_dict["change_data_source"] if "change_data_source" in response_dict else ""

    
    def get_trainings_plan(self):
        existing_training_plan = {
            "training_plan_title": self.training_plan_title,
            "summary": self.summary,
            "explanation": self.explanation,
            "workouts": self.workouts
        }
        return existing_training_plan
       