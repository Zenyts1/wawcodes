import sqlite3
from more_itertools import ilen


def to_cli(values):
    return {"uid": values[0], "auth": values[1]}


def prev_th(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except sqlite3.ProgrammingError:
            return func(Database(self.db_path), *args, **kwargs)

    return wrapper


class Database:
    def __init__(self, db_path="./data/db.sqlite"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.init_table()
        self.len_ = ilen(self.__iter__())
        # self.prev_th()

    def init_table(self):
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS db (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            uid TEXT,
            auth TEXT,
            sid INTEGER,
            ena INTEGER DEFAULT 1
        )"""
        )
        self.conn.commit()

    @prev_th
    def append(self, item):
        self.cursor.execute(
            """
        INSERT OR IGNORE INTO db (uid, auth, sid) VALUES (?,?,?)""",
            (item["uid"], item["auth"], self.len_),
        )
        self.conn.commit()
        self.len_ += 1

    @prev_th
    def __getitem__(self, key):
        if key < 0:
            key += self.__len__()
        # key += 1
        return to_cli(
            self.cursor.execute(
                """
        SELECT uid, auth FROM db WHERE sid=? AND ena>0""",
                (key,),
            ).fetchone()
        )

    @prev_th
    def __setitem__(self, key, value):
        if key < 0:
            key += self.__len__()
        # key += 1
        self.cursor.execute(
            """
        UPDATE db SET uid=?, auth=? WHERE sid=? AND ena>0""",
            (value["uid"][0], value["auth"][0], key),
        )
        self.conn.commit()

    @prev_th
    def __delitem__(self, key):
        if key < 0:
            key += self.__len__()
        # key += 1
        self.cursor.execute("""UPDATE db SET ena=0 WHERE sid=? AND ena>0""", (key,))
        self.cursor.execute("""UPDATE db SET sid=sid-1 WHERE sid>? AND ena>0""", (key,))
        self.conn.commit()
        self.len_ -= 1

    @prev_th
    def __contain__(self, item):
        return (
            self.cursor.execute(
                """SELECT sid FROM db WHERE uid=?""", (item["uid"],)
            ).fetchone()
            is not None
        )

    @prev_th
    def __add__(self, other):
        if type(other) == dict:
            self.append(other)
            return self

    @prev_th
    def __iter__(self):
        return map(
            to_cli, self.cursor.execute("""SELECT uid, auth FROM db WHERE ena>0""")
        )

    @prev_th
    def insert(self, index, item):
        self.cursor.execute(
            """INSERT OR IGNORE INTO db (uid, auth, sid) VALUES (?,?,?)""",
            (item["uid"], item["auth"], index),
        )
        self.cursor.execute(
            """UPDATE db SET sid=sid+1 WHERE sid>? and AND ena>0""", (index,)
        )
        self.conn.commit()
        self.len_ += 1

    @prev_th
    def clear(self):
        self.cursor.execute("""UPDATE db SET ena=0 WHERE ena>0""")
        # self.cursor.execute('''DELETE FROM db''')
        self.conn.commit()
        self.len_ = 0

    @prev_th
    def enumerate(self):
        return map(
            lambda x: (x[0], to_cli((x[1], x[2]))),
            self.cursor.execute("""SELECT sid, uid, auth FROM db WHERE ena>0"""),
        )

    @prev_th
    def __str__(self):
        return str(
            list(
                map(
                    to_cli,
                    self.cursor.execute("""SELECT uid, auth FROM db WHERE ena>0"""),
                )
            )
        )

    @prev_th
    def __repr__(self):
        return (
            "authDatabase("
            + str(self.cursor.execute("""SELECT * FROM db""").fetchall())
            + ")"
        )

    @prev_th
    def __len__(self):
        return self.len_

    def refresh(self):
        self.__init__(self.db_path)

    # def prev_th(self):
    #     ft = type(self.__init__)
    #     for x in dir(self):
    #         nx = getattr(self, x)
    #         if type(nx) == ft:
    #             print(x, nx)
    #             self.__setattr__(x, prev_th(nx))


if __name__ == "__main__":
    from threading import Thread

    def test():
        db.append({"uid": "2", "auth": "3"})

    db = Database()
    db.append({"uid": "1", "auth": "2"})
    Thread(target=test).start()
    # db.append({"uid": "2", "auth": "3"})
    db.append({"uid": "3", "auth": "4"})
    print(db)
    del db[1]
    print(db)
    print(list(db.enumerate()))
    db.clear()
    # for x in db:
    # print(x)
