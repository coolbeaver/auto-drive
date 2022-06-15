def only_auth_user(cur, token=None):
    cur.execute(f"SELECT COUNT(*) FROM users WHERE token = ?", (token,))
    data_column = cur.fetchone()
    if 0 in data_column:
        return False
    else:
        return True
