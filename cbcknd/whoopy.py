import requests



REQUEST_URL = "https://api.prod.whoop.com/developer"


activity_lookup = {
    -1: "Activity",
    0: "Running",
    1: "Cycling",
    16: "Baseball",
    17: "Basketball",
    18: "Rowing",
    19: "Fencing",
    20: "Field Hockey",
    21: "Football",
    22: "Golf",
    24: "Ice Hockey",
    25: "Lacrosse",
    27: "Rugby",
    28: "Sailing",
    29: "Skiing",
    30: "Soccer",
    31: "Softball",
    32: "Squash",
    33: "Swimming",
    34: "Tennis",
    35: "Track & Field",
    36: "Volleyball",
    37: "Water Polo",
    38: "Wrestling",
    39: "Boxing",
    42: "Dance",
    43: "Pilates",
    44: "Yoga",
    45: "Weightlifting",
    47: "Cross Country Skiing",
    48: "Functional Fitness",
    49: "Duathlon",
    51: "Gymnastics",
    52: "Hiking/Rucking",
    53: "Horseback Riding",
    55: "Kayaking",
    56: "Martial Arts",
    57: "Mountain Biking",
    59: "Powerlifting",
    60: "Rock Climbing",
    61: "Paddleboarding",
    62: "Triathlon",
    63: "Walking",
    64: "Surfing",
    65: "Elliptical",
    66: "Stairmaster",
    70: "Meditation",
    71: "Other",
    73: "Diving",
    74: "Operations - Tactical",
    75: "Operations - Medical",
    76: "Operations - Flying",
    77: "Operations - Water",
    82: "Ultimate",
    83: "Climber",
    84: "Jumping Rope",
    85: "Australian Football",
    86: "Skateboarding",
    87: "Coaching",
    88: "Ice Bath",
    89: "Commuting",
    90: "Gaming",
    91: "Snowboarding",
    92: "Motocross",
    93: "Caddying",
    94: "Obstacle Course Racing",
    95: "Motor Racing",
    96: "HIIT",
    97: "Spin",
    98: "Jiu Jitsu",
    99: "Manual Labor",
    100: "Cricket",
    101: "Pickleball",
    102: "Inline Skating",
    103: "Box Fitness",
    104: "Spikeball",
    105: "Wheelchair Pushing",
    106: "Paddle Tennis",
    107: "Barre",
    108: "Stage Performance",
    109: "High Stress Work",
    110: "Parkour",
    111: "Gaelic Football",
    112: "Hurling/Camogie",
    113: "Circus Arts",
    121: "Massage Therapy",
    125: "Watching Sports",
    126: "Assault Bike",
    127: "Kickboxing",
    128: "Stretching",
    230: "Table Tennis",
    231: "Badminton",
    232: "Netball",
    233: "Sauna",
    234: "Disc Golf",
    235: "Yard Work",
    236: "Air Compression",
    237: "Percussive Massage",
    238: "Paintball",
    239: "Ice Skating",
    240: "Handball"
}


class WhoopClient:
    def __init__(self, token) -> None:
        self.token = token

    def get_profile(self):
        return self.make_whoop_request(method="GET", url_="v1/user/profile/basic")

    def get_body_measurement(self):
        return self.make_whoop_request(method="GET", url_="v1/user/measurement/body")

    def get_cycle_by_id(self, cycle_id: str):
        return self.make_whoop_request(method="GET", url_=f"v1/cycle/{cycle_id}")

    def get_cycles(self):
        return self.make_paged_whoop_request(
            method="GET",
            url_="v1/cycle",
            params={"limit": 25},
        )

    def get_recovery_for_cycle(self, cycle_id: str):
        return self.make_whoop_request(
            method="GET", url_=f"v1/cycle/{cycle_id}/recovery"
        )

    def get_recoveries(self):
        return self.make_paged_whoop_request(
            method="GET",
            url_="v1/recovery",
            params={"limit": 25},
        )

    def get_sleep_by_id(self, sleep_id: str):
        return self.make_whoop_request(
            method="GET", url_=f"v1/activity/sleep/{sleep_id}"
        )

    def get_sleeps(self):
        return self.make_paged_whoop_request(
            method="GET",
            url_="v1/activity/sleep",
            params={"limit": 25},
        )

    def get_workout_by_id(self, workout_id: str):
        return self.make_whoop_request(
            method="GET", url_=f"v1/activity/workout/{workout_id}"
        )

    def get_workouts(self):
        return self.make_paged_whoop_request(
            method="GET",
            url_="v1/activity/workout",
            params={"limit": 25},
        )

    def make_paged_whoop_request(self, method, url_, params):
        response_data: list = []

        for i in range(5):
            response = self.make_whoop_request(
                method=method,
                url_=url_,
                params=params,
            )

            response_data += response["records"]

            if next_token := response["next_token"]:
                params["nextToken"] = next_token

            else:
                break

        return response_data

    def make_whoop_request(self, method, url_, params=None):
        api_call_headers = {"Authorization": "Bearer " + self.token}

        if method == "GET":
            api_call_response = requests.get(
                f"{REQUEST_URL}/{url_}", headers=api_call_headers, params=params
            )
        elif method == "POST":
            api_call_response = requests.post(
                f"{REQUEST_URL}/{url_}", headers=api_call_headers, params=params
            )
        else:
            raise ValueError("Invalid method")
        
        if api_call_response.status_code != 200:
            print(api_call_response)
            # raise ValueError("Invalid response code")

        return api_call_response.json()


# client.authenticate()


# auth_url = "https://api.prod.whoop.com/oauth/oauth2/auth"

# from authlib.integrations.requests_client import OAuth2Session

# from authlib.integrations.requests_client import OAuth2Session
# client = OAuth2Session(client_id, client_secret)

# oclient = OAuth2Session(client_id=CLIENT_ID, client_secret=CLIENT_SECRET )
# uri, state = oclient.create_authorization_url(auth_url)


# oclient.fetch_token(
#     token_url="https://api.prod.whoop.com/oauth/oauth2/token",
#     client_id=CLIENT_ID,
#     client_secret=CLIENT_SECRET,
# )

if __name__ == "__main__":

    TOKEN = "_5kze_ywT3EiCs9-gAFu7BoGVzR9LSef7so4e42I9vw.IkDnh5wXnQ9VAvBrbgwNv08tO0xZudGetcuy4ciY_HQ"
    wpc = WhoopClient(TOKEN)

    wpc.get_profile()

    print(wpc.get_workouts())

    print("xD")
