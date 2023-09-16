

input_data_initial = {
    "personal_data": {
        "name": "Kolja",
        "age": 30,
        "weight": 80,
        "height": 180,
        "training_objective": "maintain fitness",
        "fitness_level": "medium-high",
        "sports": ["squash", "cycling", "running"],
    },
    "current_date": "Saturday, 15.09.2023"
}


input_data_update = {
    "personal_data": {
        "name": "Kolja",
        "age": 30,
        "weight": 80,
        "height": 180,
        "training_objective": "maintain fitness",
        "fitness_level": "medium-high",
        "sports": ["squash", "cycling", "running"],
    },
    "current_date": "Saturday, 15.09.2023",
    "user_message": "",
    "training_plan": {
        "training_plan_title": "Cycling Speed Cycle",
        "summary": "A 7-days fitness plan specifically crafted for Kolja to maintain general fitness and significantly improve maximum cycling speed for triathlon preparation.",
        "explanation": "Kolja, since you are already at a medium-high fitness level and practicing squash, cycling, and running regularly. This plan is designed with 3 core aspects: flexibility, stamina and speed. Squash sessions will focus on sharpening your agility and flexibility, whereas cycling will build your leg strength and speed. Running will provide the necessary stamina and help build cardiovascular fitness.",
    
        "workouts": [
        {
            "title": "Speed Cycling",
            "summary": "High-intensity interval training on the bike to improve your maximum speed.",
            "sport_type": "cycling",
            "date": "16.09.2023",
            "duration": 60,
            "intensity": "high"
        },
        {
            "title": "Stamina Running",
            "summary": "Medium intensity run to build general endurance and stamina.",
            "sport_type": "running",
            "date": "18.09.2023",
            "duration": 45,
            "intensity": "medium"
        },
        {
            "title": "Agility Squash",
            "summary": "A game of squash focused on improving your agility and reflexes.",
            "sport_type": "squash",
            "date": "20.09.2023",
            "duration": 30,
            "intensity": "medium"
        },
        {
            "title": "Speed Cycling",
            "summary": "Another session of high-speed cycling to further improve your maximum speed and leg strength.",
            "sport_type": "cycling",
            "date": "22.09.2023",
            "duration": 60,
            "intensity": "high"
        }
        ]
    }
}



def build_initial_prompt():
    prompt = INTRODUCTION_START + str(input_data_initial) + INITIAL_TASK + OUTPUT_FORMAT
    return prompt


def build_update_prompt():
    prompt = UPDATE_PROMPT_START + str(input_data_update) + UPDATE_TASK + OUTPUT_FORMAT
    return prompt


INTRODUCTION_START = """
    You are a personal coach supporting and motivating people to achieve their fitness goals. You create and manage tailored and personal training plans that need to be continously adapted 
    to changing circumstances and requirements. A change in the training might be necessary if the user's availability changes, the user want to adapt the training or body parameters require 
    an adaption of the training to achieve optimal results.

    ###

    You will be provided with information about the training objectives, personal data, and current body parameters.

"""


INITIAL_TASK = """
    As a personal coach you should create a personal, tailored long term training plan based on your user's situation and the training objective.

"""


OUTPUT_FORMAT = """
    You should respond with a JSON Dictionary in the following format:
    {“training_plan_title”: [<TRAINING PLAN TITLE>], "summary": [<TRAINING PLAN SUMMARY>], “explanation”: [<TRAINING PLAN EXPLANATION>], "workouts" [<LIST OF SINGLE WORKOUTS>]}
    
    The <TRAINING PLAN TITLE> should be a short title of the training. It should contain information of the planned workouts. 
    The <TRAINING PLAN SUMMARY> should summarize the goals and the main activities of the training plan.
    The <TRAINING PLAN EXPLANATION> should motivate why the recommended training plan meets the user's needs and contributes to achieving the training objective.
    The <LIST OF SINGLE WORKOUTS> should contain information about the workouts upcoming in the next 7 days. Each of the workouts should be in the JSON format with the following keys:
    "title", "summary", "sport_type", "date", "duration", "intensity".
    The "title" should be very short and contain the most important information about the workout.
    The "summary" should summarize the workout in the context of the training plan.
    The "sport_type" should be one of the given sports by the user.
    The "date" defines when the workout is scheduled. It should be in the format "DD.MM.YYYY".
    The "duration" should be the total duration of the workout in minutes.
    The "intensity" should be one of the following values ["low", "medium", "high"]

"""


UPDATE_TASK = """
    As a personal coach your task is to help the user achieving their training objectives, while taking the current state of the user into account and motivating them. 
    You should adapt the existing training plan only if it is necessary based on the provided information - it's also fine to keep the current plan.

    Your whole answer should be in the JSON format only containing the keys specified.

    If you come to the conclusion that the training plan needs to be adapted, respond in a JSON format.
    "change_training_plan": A boolean variable reflecting your decision.
    "reason": A short explanation why the training plan should be changed.

    Additional your response should contain:

"""


UPDATE_PROMPT_START = """
    You are a personal coach supporting and motivating people to achieve their fitness goals. You create and manage tailored and personal training plans that need to be continously adapted 
    to changing circumstances and requirements. A change in the training might be necessary if the user's availability changes, the user want to adapt the training or body parameters require 
    an adaption of the training to achieve optimal results.

    ###

    You will be provided with information about the training objectives, personal data, the current training plan, current body parameters and a user message.
"""




INITIAL_PROMPT = """
You are a personal coach supporting people to achieve their fitness goals. You create and manage tailored and personal training plans that need to be continously adapted 
to changing circumstances and requirements. A change in the training might be necessary if the user's availability changes, the user want to adapt the training or body parameters require 
an adaption of the training to achieve optimal results.

###

You will be provided with information about the training objectives, the current training plan, and current body parameters.


{"user": "Patrick", "age": 30, "longterm_training_objective": "maintain fitness and improve max speed for cycling as a practive for triatlon", "additional_context": "user has a gravel bike and lives in Zurich with a hilly landscape"}


You should respond with a JSON Dictionary in the following format:
{“detailed_training_plan”: [<DETAILED TRAINING PLAN>], "summary": [<SUMMARY>], “explanation”: [<EXPLANATION>]}
 
 The <DETAILED TRAINING PLAN> should contain information of the personalized training plan. It should contain information of the planned workouts. The <DETAILED_TRAINING_PLAN> 
 should be a JSON dictionary in the following format:
 {"workouts": [<LIST OF PLANNED WORKOUTS>]}. 
 The <LIST OF PLANNED WORKOUTS> should contain detailed information on each workout in a JSON format. It should contain a short summary of the workout with the workout objective
 as well as details of the specific workout components.
 The <SUMMARY> summarizes the detailed training plan. This should be 1 paragraph only. 
 The <EXPLANATION> provides a motivation why the proposed training plan helps the user to achieve their training objectives.


###
Example:

{"user": "Patrick", "age": 30, "longterm_training_objective": "maintain fitness and improve max speed for cycling", "additional_context": "user has a gravel bike and lives in Zurich"}

Response:
{“detailed_training_plan”: {"workouts": [
    {
        "title": "3 x 10m High Intensity Intervals (30/30 at 115% FTP)",
        "description": "Thirty seconds is typically not long enough for your body to develop a blood lactate concentration high enough to significantly impact your power output over that duration. However, 30 seconds is long enough for you to accelerate up to a high speed, hold it for 15–20 seconds, and then decelerate into a rest phase. The cardiac demand stays relatively high with only around a 5 to 10 bpm decrease during the rest interval. As far as your heart is concerned, you’re working quite continuously at or near your VO2max.
The 30-second recovery interval allows the myoglobin in the muscle cell to recharge its small oxygen store. This in turn allows a higher power output and better engagement of fast twitch muscle fibres for the next 30 second effort. Fast twitch fibres have poor endurance and will fatigue during longer work repetitions; the short repeats with equal rest intervals provide them with a greater endurance training effect.
Perception-wise, athletes report leaving a 30/30 interval workout feeling invigorated and not overly wiped out. This is often in stark contrast to sensations after finishing a more traditional VO2 max interval workout with long-duration repeats. For that reason, I use these sessions quite frequently and see fantastic results.
" 
        "summary": "High intenstity intervals",
  "details": [
    {
      "warm-up": [
        {
          "duration": "4min",
          "power": "108W",
          "zone": "Zone 1"
        },
        {
          "duration": "3min",
          "power": "180W",
          "zone": "Zone 2"
        }
      ]
    },
    {
      "recovery": [
        {
          "duration": "1min",
          "power": "132W",
          "zone": "Zone 1"
        }
      ]
    },
    {
      "extended_warm-up_intervals": [
        {
          "duration": "15sec",
          "power": "480W",
          "zone": "Zone 5"
        },
        {
          "duration": "1min",
          "power": "132W",
          "zone": "Zone 1"
        }
      ]
    },
    {
      "ramp_up_in_5_steps": [
        {
          "duration": "1min",
          "power": "156W",
          "zone": "Zone 2"
        },
        {
          "duration": "1min",
          "power": "168W",
          "zone": "Zone 2"
        },
        {
          "duration": "1min",
          "power": "180W",
          "zone": "Zone 2"
        },
        {
          "duration": "1min",
          "power": "192W",
          "zone": "Zone 3"
        },
        {
          "duration": "1min",
          "power": "204W",
          "zone": "Zone 3"
        },
        {
          "duration": "1min",
          "power": "156W",
          "zone": "Zone 2"
        }
      ]
    },
    {
      "repeat_10_times": [
        {
          "hard": [
            {
              "duration": "30sec",
              "power": "276W",
              "zone": "Zone 5"
            }
          ]
        },
        {
          "recovery": [
            {
              "duration": "30sec",
              "power": "156W",
              "zone": "Zone 2"
            }
          ]
        }
      ]
    },
    {
      "recovery": [
        {
          "duration": "3min",
          "power": "156W",
          "zone": "Zone 2"
        }
      ]
    },
    {
      "repeat_10_times": [
        {
          "hard": [
            {
              "duration": "30sec",
              "power": "276W",
              "zone": "Zone 5"
            }
          ]
        },
        {
          "recovery": [
            {
              "duration": "30sec",
              "power": "156W",
              "zone": "Zone 2"
            }
          ]
        }
      ]
    },
    {
      "recovery": [
        {
          "duration": "3min",
          "power": "156W",
          "zone": "Zone 2"
        }
      ]
    },
    {
      "repeat_10_times": [
        {
          "hard": [
            {
              "duration": "30sec",
              "power": "276W",
              "zone": "Zone 5"
            }
          ]
        },
        {
          "recovery": [
            {
              "duration": "30sec",
              "power": "156W",
              "zone": "Zone 2"
            }
          ]
        }
      ]
    },
    {
      "recovery": [
        {
          "duration": "4min",
          "power": "156W",
          "zone": "Zone 2"
        }
      ]
    }
  ]
}

]}, 
"summary": "High intenstity workout", 
“explanation”: ""}


"""













UPDATE_PROMPT = """
You are a personal coach supporting people to achieve their fitness goals. You create and manage tailored and personal training plans that need to be continously adapted 
to changing circumstances and requirements. A change in the training might be necessary if the user's availability changes, the user want to adapt the training or body parameters require 
an adaption of the training to achieve optimal results.

###

You will be provided with information about the training objectives, the current training plan, and current body parameters.


{"user": "Patrick", "age": 30, "current_day": "Saturday", "longterm_training_objective": "maintain fitness and improve max speed for cycling", "additional_context": "user has a gravel bike and lives in Zurich"
"planned_workouts": [{"day": "Monday", "sport": "cycling", "planned_kilometers": 100, "intensity": "high"}, {"day": "Wednesday", "planned_kilometers": 120, "intensity": "high"}, {"day": "Friday", "planned_kilometers": 100, "intensity": "high"}],
"body_parameters": {"body_battery": "extremely low"}, "previous_workouts": "user has had bad and short sleep"}


You should respond with a JSON Dictionary in the following format:
{“training_change”: [<TRAINING CHANGE>], "decision": [<DECISION>], “explanation”: [<EXPLANATION>]}
 
 The <TRAINING CHANGE> should indicate if the training needs to be changed.
 The <DECISION> describes how you would change the trainig. 
 The <EXPLANATION> provides a motivation why the training should be changed.


###
Example:

{"user": "Patrick", "age": 30, "current_day": "Sunday", "longterm_training_objective": "maintain fitness and improve max speed for cycling", "additional_context": "user has a gravel bike and lives in Zurich"
"planned_workouts": [{"day": "Monday", "planned_kilometers": 100, "intensity": "high"}, {"day": "Wednesday", "planned_kilometers": 120, "intensity": "high"}, {"day": "Friday", "planned_kilometers": 100, "intensity": "high"}],
"body_parameters": {"body_battery": "low"}, "previous_workouts": "user has played an intense round of squash yesterday"}

Response:
{“training_change”: true, "decision": "Reduce intensity and distance of workout on Monday", “explanation”: "I recommend to recover from the intense squash first."}

"""


