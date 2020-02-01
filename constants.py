MOODY_2_OBLIGOR = {
    'A1-A3': 3,
    'Aa1-Aa3': 2,
    'B1 +': 12,
    'B1 -': 13,
    'B2': 14,
    'B3': 15,
    'Ba1': 7,
    'Ba2 +': 8,
    'Ba2 -': 9,
    'Ba3 +': 10,
    'Ba3 -': 11,
    'Baa1': 4,
    'Baa2': 5,
    'Baa3': 6,
    'C-D': 19,
    'Ca': 18,
    'Caa1': 16,
    'Caa2-Caa3': 17
}

def to_tier(fa_r,ob_r):
    if fa_r == 'A' or fa_r == 'B':
        if ob_r <= 16:
            return 0
        else:
            return 4
    elif fa_r == 'C':
        if ob_r <= 7:
            return 0
        elif ob_r > 7 and ob_r <= 14:
            return 1
        elif ob_r == 15:
            return 3
        else:
            return 4
    elif fa_r == 'D':
        if ob_r <= 6:
            return 0
        elif ob_r > 6 and ob_r <= 14:
            return 1
        elif ob_r == 15:
            return 3
        else:
            return 4
    elif fa_r == 'E':
        if ob_r <= 6:
            return 0
        elif ob_r > 6 and ob_r <= 13:
            return 1
        elif ob_r == 14:
            return 2
        elif ob_r == 15:
            return 3
        else:
            return 4
    elif fa_r == 'F' or fa_r == 'G':
        if ob_r <= 5:
            return 0
        elif ob_r > 5 and ob_r <= 12:
            return 1
        elif ob_r > 12 and ob_r <= 14:
            return 2
        elif ob_r == 15:
            return 3
        else:
            return 4
    elif fa_r == 'H':
        if ob_r <= 5:
            return 0
        elif ob_r > 5 and ob_r <= 11:
            return 1
        elif ob_r > 11 and ob_r <= 14:
            return 2
        elif ob_r == 15:
            return 3
        else:
            return 4
    elif fa_r == 'I' or fa_r == 'J':
        if ob_r <= 4:
            return 0
        elif ob_r > 4 and ob_r <= 11:
            return 1
        elif ob_r > 11 and ob_r <= 14:
            return 2
        elif ob_r == 15:
            return 3
        else:
            return 4
    elif fa_r == 'K' or fa_r == 'L' or fa_r == 'M':
        if ob_r <= 4:
            return 0
        elif ob_r > 4 and ob_r <= 10:
            return 1
        elif ob_r > 10 and ob_r <= 14:
            return 2
        elif ob_r == 15:
            return 3
        else:
            return 4
    elif fa_r == 'O':
        if ob_r <= 3:
            return 0
        elif ob_r > 3 and ob_r <= 10:
            return 1
        elif ob_r > 10 and ob_r <= 14:
            return 2
        elif ob_r == 15:
            return 3
        else:
            return 4
    elif fa_r == 'Q' or  fa_r == 'S' or  fa_r == 'T':
        if ob_r <= 3:
            return 0
        elif ob_r > 3 and ob_r <= 9:
            return 1
        elif ob_r > 9 and ob_r <= 14:
            return 2
        elif ob_r == 15:
            return 3
        else:
            return 4
