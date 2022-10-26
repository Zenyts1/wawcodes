import random
from itertools import islice

useragent_c = 1000


def fake_useragent():
    with open("data/useragents.txt", "r") as f:
        n = random.randint(0, useragent_c - 1)
        return next(islice(f, n, n + 1))[:-1]
