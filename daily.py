import requests
import random
import json
import time
import logs

from db import Database

db = Database()

def get_daily_reward(cookies):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Cache-Control": "max-age=0",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Cookie": cookies,
    }
    response = requests.post(
        "https://hk4e-api-os.mihoyo.com/event/sol/sign?act_id=e202102251931481&lang=en-us",
        headers=headers,
        data=json.dumps({"act_id": "e202102251931481"}, ensure_ascii=False),
    )
    logs.log_daiy(response)
    return response.content


def daily():
    for i in db:
        get_daily_reward(i["auth"])
        time.sleep(random.uniform(5, 7))
