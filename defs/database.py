import sqlite3


def sign_db(cur, data):
    cur.execute(f"SELECT id, token, picture, block FROM users WHERE email = ? AND password = ?", data)
    data_column = cur.fetchone()
    if data_column is None:
        return False
    else:
        d = dict();
        d['id'] = data_column[0]
        d['token'] = data_column[1]
        d['picture'] = data_column[2]
        d['block'] = data_column[3]
        return d


def check_info(cur, data):
    cur.execute(f"SELECT picture, username, about, car, id FROM users WHERE id = ?", (data,))
    data_column = cur.fetchone()
    if data_column is None:
        return False
    else:
        d = dict();
        d['picture'] = data_column[0]
        d['username'] = data_column[1]
        d['about'] = data_column[2]
        d['car'] = data_column[3]
        d['mail'] = data_column[4]
        d['id'] = data_column[4]
        return d


def select_all_users(cur):
    cur.execute(f"SELECT  id, email, username, picture, about, car, block FROM users")
    data_column = cur.fetchall()
    return data_column


def check_block(cur, id):
    cur.execute(f"SELECT block FROM users WHERE id = ?", (id,))
    data_column = cur.fetchone()
    return data_column


def select_all_calc(cur):
    cur.execute(f"SELECT * FROM result_calc")
    data_column = cur.fetchall()
    return data_column


def select_all_posts(cur):
    cur.execute(f"SELECT * FROM posts")
    data_column = cur.fetchall()
    return data_column


def reg_db(cur, con, data):
    print(data[0])
    cur.execute(f"SELECT COUNT(*) FROM users WHERE username = ?", (data[0],))
    check_repetition_username = cur.fetchone()
    cur.execute(f"SELECT COUNT(*) FROM users WHERE email = ?", (data[1],))
    check_repetition_mail = cur.fetchone()
    if 0 in check_repetition_username and 0 in check_repetition_mail:
        cur.execute(f"INSERT INTO users(username, email, password, token) VALUES(?, ?, ?, ?)", data)
        con.commit()
        return True
    elif 0 not in check_repetition_username:
        return 'Rep_Name'
    elif 0 not in check_repetition_mail:
        return 'Rep_Mail'


def check_posts(cur, data):
    cur.execute(f"SELECT * FROM posts WHERE user = ?", (data,))
    data_column = cur.fetchall()
    print(data_column)
    if data_column is None:
        return False
    else:
        return data_column


def delete_post(cur, con, data):
    cur.execute("DELETE FROM posts WHERE id = ?", (data,))
    con.commit()
    return True


def create_post(cur, con, data):
    cur.execute(f"INSERT INTO posts(user, timestamp, text, photo) VALUES(?, ?, ?, ?)", data)
    con.commit()
    return True


def create_result(cur, con, data):
    cur.execute(f"INSERT INTO result_calc(ls, timestamp, price_ts, credit, time_credit, percent_credit, avg_cons,"
                f" price_benz, reg_go, col_reg, noreg_go, col_noreg, strah)"
                f"VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    con.commit()
    return True


def update_user(cur, con, set_data, data, id):
    cur.execute(f"UPDATE users SET {set_data} = '{data}' WHERE id = '{id}'")
    con.commit()
    return True
