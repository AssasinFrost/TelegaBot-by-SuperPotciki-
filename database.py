import sqlite3
import datetime


def autorization(userid, message):
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        now = datetime.datetime.now()
        date_string = now.strftime('%Y-%m-%d')
        try:
            cur.execute("""INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)""", (userid, 0, 1, date_string,
                                                                               message.from_user.first_name,
                                                                               message.from_user.username, 1))
        except:
            cur.execute("""INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)""", (userid, 0, 1, date_string,
                                                                               message.from_user.first_name, 'None', 1))
        con.commit()


def check_atz(userid):
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        res = cur.execute("""SELECT * FROM users WHERE userid = ?""", (userid,)).fetchall()
        if len(res) == 0:
            return True
        return False


def set_id_mess(userid, messid):
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        cur.execute("""INSERT INTO mess_rules VALUES(?, ?)""", (userid, messid))
        con.commit()


def get_id_mess(userid):
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        res = cur.execute("""SELECT messid FROM mess_rules WHERE userid = ?""", (userid,)).fetchone()[0]
        return res


def dell_id_mess(userid):
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        cur.execute("""DELETE FROM mess_rules WHERE userid = ?""", (userid,))
        con.commit()


def get_info(userid):
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        res = cur.execute("""SELECT * FROM users WHERE userid = ?""", (userid,)).fetchall()
        return res


def get_info_admin():
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        res = cur.execute("""SELECT username FROM users""").fetchall()
        return len(res), res[-1]


def ban(userid, state):
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        cur.execute("""UPDATE users
        SET state = ?
        WHERE userid = ?""", (state, userid))
        con.commit()


def users():
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        res = cur.execute("""SELECT userid FROM users""").fetchall()
        return res


def set_money(userid, update_count):
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        cur.execute("""
        UPDATE users
        SET money = ?
        WHERE userid = ?
        """, (update_count, userid))
        con.commit()


def add_money(userid, update_count):
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        money = cur.execute("""SELECT money FROM users
            WHERE userid = ? """, (userid,)).fetchone()
        update_count = int(update_count) + int(money[0])
        cur.execute("""
        UPDATE users
        SET money = ?
        WHERE userid = ?
        """, (update_count, int(userid)))
        con.commit()

def take_money(userid, update_count):
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        money = cur.execute("""SELECT money FROM users
            WHERE userid = ? """, (userid,)).fetchone()
        update_count = int(money[0] - int(update_count))
        cur.execute("""
        UPDATE users
        SET money = ?
        WHERE userid = ?
        """, (update_count, int(userid)))
        con.commit()

def lvlup(userid):
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        lvl = cur.execute("""SELECT lvl FROM users
                    WHERE userid = ? """, (userid,)).fetchone()[0]
        cur.execute("""
                UPDATE users
                SET lvl = ?
                WHERE userid = ?
                """, (int(lvl) + 1, userid))
        con.commit()