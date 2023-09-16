
# This file contains the user model class
from collections import defaultdict, deque
import datetime

import numpy as np


class User:

    def __init__(self):
        self.name = "User"
        self.age = 0
        self.weight = 70
        self.height = 1.7
        self.training_objective = ""
        self.fitness_level = "average"
        self.sports = []
        self.sleeps_scores = deque([50], maxlen=30)
        self.recovery_scores = deque([50], maxlen=30)

    def calc_fitness_level(self, workout_list):

        week_dict = defaultdict(int)

        for workout in workout_list:
            start_time = datetime.datetime.strptime(workout["start"], '%Y-%m-%dT%H:%M:%S.%fZ')
            end_time = datetime.datetime.strptime(workout["end"], '%Y-%m-%dT%H:%M:%S.%fZ')

            duration = end_time - start_time

            minutes = duration.total_seconds() // 60

            week_number = start_time.isocalendar()[1]

            week_dict[week_number] += minutes

        avg_minutes = np.mean(list(week_dict.values()))

        if avg_minutes < 120:
            self.fitness_level = "low"
        elif avg_minutes < 300:
            self.fitness_level = "average"
        elif avg_minutes < 600:
            self.fitness_level = "ambitious"
        elif avg_minutes < 1200:
            self.fitness_level = "competitive"
        else:   
            self.fitness_level = "professional"

    def update_sleeps_scores(self, sleeps):
        for sleep in reversed(sleeps):
            self.sleeps_scores.append(sleep["score"]["sleep_consistency_percentage"])

    def update_recovery_scores(self, recoveries):
        for recovery in reversed(recoveries):
            self.recovery_scores.append(recovery["score"]["recovery_score"])

    @property
    def last_sleep_score(self):
        return self.sleeps_scores[-1]
    
    @property
    def avg_sleep_score(self):
        return np.mean(self.sleeps_scores)
    
    @property
    def last_recovery_score(self):
        return self.recovery_scores[-1]
    
    @property
    def avg_recovery_score(self):
        return np.mean(self.recovery_scores)

    def to_dict(self):
        # Create a dictionary of the object's attributes
        data = {
            "name": self.name,
            "age": self.age,
            "weight": self.weight,
            "height": self.height,
            "training_objective": self.training_objective,
            "fitness_level": self.fitness_level,
            "sports": self.sports,
            "last_sleep_score": self.last_sleep_score,
            "avg_sleep_score": self.avg_sleep_score,
            "last_recovery_score": self.last_recovery_score,
            "avg_recovery_score": self.avg_recovery_score,
        }

        # Return the dictionary
        return data

