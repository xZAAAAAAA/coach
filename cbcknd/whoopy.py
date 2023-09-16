import requests



REQUEST_URL = "https://api.prod.whoop.com/developer"




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
