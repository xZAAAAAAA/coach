
# This file contains the user model class
from collections import defaultdict
import datetime

import numpy as np


class User:

    def __init__(self):
        self.name = "User"
        self.age = 0
        self.weight = 70
        self.height = 1.7
        self.training_objective = "maintain fitness"
        self.fitness_level = "average"
        self.sports = []

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


