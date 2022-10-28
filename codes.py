from event import Events
try:
    from db import Database
    #from replit import db
except:
    print("Error importing database 0")
    try:
        from replit import db
    except:
        print("Error importing database 1")
        db = []
    Database = None
import json
import os
import random
import re
import time

import fake_useragent
import requests


if Database is not None:
    db = Database()


#

if os.getenv("waw") is not None:
    Dauth = os.getenv("waw")
else:
    Dauth = input(
        "a discord token (from an account witch is on the Genshin Impact server, it can be an alt) : "
    )

#


m = re.compile(r" ([A-Z]|\d){12}")


if "used.json" in os.listdir():
    try:
        with open("used.json", "r") as f:
            used = json.load(f)
    except Exception as e:
        print("Error while loading used.json :", e)
else:
    print("used.json not found")
    used = []
    try:
        with open("used.json", "w") as f:
            json.dump(used, f)
    except Exception as e:
        print("Error while saving used.json :", e)


def add_cli(cli: dict) -> bool:
    if cli not in db:
        db.append(cli)
        return True
    return False


def find_codes(message: str) -> str:
    if message is None:
        return
    for x in m.finditer(message):
        x = x.group()[1:]
        if x not in used:
            yield x


def redeem_codes() -> None:
    print("A...")
    UA = fake_useragent.fake_useragent()
    Dheaders = {"User-Agent": UA, "Authorization": Dauth}
    Durl = "https://discord.com/api/v9/channels/740919586001518622"
    Gheaders = {}
    Gurl = "https://sg-hk4e-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkey?uid={uid}&region=os_euro&lang=en&cdkey={code}&game_biz=hk4e_global"
    messages = requests.get(Durl + "/messages?limit=100", headers=Dheaders)
    print(messages.status_code)
    try:
        messages = messages.json()
    except json.JSONDecodeError:
        print(messages.content)
        return
    except TypeError:
        if type(messages) == bytes:
            if not b"Access denied" in messages.content:
                print(messages.content)
            else:
                time.sleep(600)
        return
    for message in messages:
        try:
            for x in find_codes(message.get("content")):
                print(x)
                uids = {"success": [], "fail": [], "reasons": []}
                n = 0
                for cli in db:
                    Gheaders["User-Agent"] = fake_useragent.fake_useragent()
                    Gheaders["Cookie"] = cli["auth"]
                    try:
                        r = requests.get(
                            Gurl.replace("{uid}", cli["uid"]).replace("{code}", x),
                            headers=Gheaders,
                        )
                        response = r.json()
                        r_message = response.get("message", "")
                        if "OK" in r_message:
                            uids["success"].append(cli["uid"])
                        else:
                            uids["fail"].append(cli["uid"])
                            uids["reasons"].append(r_message)
                        if n < 1:
                            print(cli["uid"], r.status_code, r.content)
                        if response["retcode"] in [-2001, -2003]:
                            n += 1
                    except Exception as e:
                        print("a", e)
                    time.sleep(random.uniform(5, 7))
                used.append(x)
                event.trigger("End", x, uids)
        except Exception as e:
            print("b", e)
    try:
        with open("used.json", "w") as f:
            json.dump(used, f)
    except Exception as e:
        print("Error while saving used.json :", e)


event = Events("End")
