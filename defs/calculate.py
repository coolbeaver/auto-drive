def calc_credit(sum, percent, term):
    return int((sum * (percent / 100) * (1 + (percent / 100)) ** term) / (12 * ((1 + (percent / 100)) ** term - 1)))


def calc_osago(ls):
    return int((4102 * 1.64 * 0.46 * 1.96 * (ls / 100) * 1))


def calc_oil(avg, price, reg, col_reg, noreg, col_noreg):
    return int(((((reg * col_reg) + (noreg * col_noreg)) / 100) * avg) * price)


def calc_nalog(ls):
    if ls <= 100:
        ns = 24
    elif 100 < ls <= 150:
        ns = 35
    elif 150 < ls <= 200:
        ns = 50
    elif 200 < ls <= 250:
        ns = 75
    elif 250 < ls:
        ns = 150
    return int(ls * ns * (12 / 12))
