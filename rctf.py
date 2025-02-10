from typing import Any, Dict, List
from urllib.parse import urljoin
import requests
from requests_toolbelt.sessions import BaseUrlSession  


class RCTF:
    session: requests.Session
    def __init__(self, endpoint: str, login_token: str):
        self.session = BaseUrlSession(urljoin(endpoint, "api/v1/"))

        if login_token is not None:
            login_resp = requests.post(
                urljoin(endpoint, "api/v1/auth/login"), json={"teamToken": login_token}
            ).json()
            if login_resp["kind"] == "goodLogin":
                auth_token = login_resp["data"]["authToken"]
                self.session.headers["Authorization"] = f"Bearer {auth_token}"
            else:
                raise ValueError(
                    f"Invalid login_token provided (reason: {login_resp['kind']})"
                )

    @staticmethod
    def assertResponseKind(response: Any, kind: str) -> None:
        if response["kind"] != kind:
            raise RuntimeError(f"Server error: {response['kind']}")

    def list_challenges(self) -> List[Dict[str, Any]]:
        r = self.session.get("challs").json()
        self.assertResponseKind(r, "goodChallenges")
        return r["data"]
    
    def list_solved_challenges(self) -> List[Dict[str, Any]]:
        r = self.session.get("challs").json()
        self.assertResponseKind(r, "goodChallenges")
        challs = r["data"]
        challs_solved = [dict(category=chall['category'], id=chall['id'], name=chall['name']) for chall in challs if chall['solves'] > 0 ]
        return challs_solved
    
    def first_solve(self , id) -> List[Dict[str, Any]]:
        params = {
        "limit": 1,
        "offset": 0
        }
        r = self.session.get("challs/"+ id +"/solves",params=params).json()
        self.assertResponseKind(r, "goodChallengeSolves")
        return r['data']['solves'][0]


