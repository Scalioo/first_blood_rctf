
from db import database 
from rctf import RCTF
import requests
import time
from dotenv import load_dotenv
import os


ANNOUNCEMENT = ":drop_of_blood: First blood for **{challenge}** from the **{category}** category goes to **{user}** !!! :drop_of_blood:"




def announce_to_discord(db , discord : str , challenge , already_in):
    res = requests.post(discord, json={
            "content": ANNOUNCEMENT.format(challenge=challenge["name"], category=challenge["category"] ,user=challenge["first_blood"])
        }, timeout=5)
    if res.status_code in [200, 204]:
        db.add_first_blood_to_db(challenge)
        already_in.append(challenge)
        print(ANNOUNCEMENT.format(challenge=challenge["name"],category=challenge["category"], user=challenge["first_blood"]))


def announce(db , rctf , discord:str):
    challs = rctf.list_solved_challenges()
    already_in = db.fetch_first_bloods_from_db()
    ids_already_in = {item['id'] for item in already_in}
    not_announced_challenges = [item for item in challs if item['id'] not in ids_already_in]

    for chall in not_announced_challenges:
        user = rctf.first_solve(chall['id'])
        chall['first_blood'] = user['userName']
        announce_to_discord(db,discord,chall,already_in)




def main():
    load_dotenv()
    token = os.getenv("TOKEN")
    url = os.getenv("URL")
    discord = os.getenv("DISCORD")
    timeout = int(os.getenv("TIMEOUT" , 30))
    db_name = os.getenv("DB" , "solves.db")

    if None in (token, url, discord):
        raise ValueError("One or more required environment variables are missing: TOKEN, URL, DISCORD")

    db = database(db_name)
    rctf = RCTF(url , token)

    while True :
        announce(db , rctf , discord)
        time.sleep(timeout)



if __name__ == "__main__":
    main()




