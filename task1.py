from sys import argv
from binascii import  hexlify


def user_to_int(user_id):
    return int(hexlify(user_id.encode('utf8')), 16)


def myhashs(user_id):
    def h1(x):
        a1 = 66809
        b1 = 42443
        return a1 * x + b1

    def h2(x):
        a2 = 16811
        b2 = 56167
        return a2 * x + b2

    m = 69997  # len of bit array
    hash_result = []
    num_hashes = 50
    for i in range(1, num_hashes+1):
        hashed_postition = (h1(user_to_int(user_id)) + i * h2(user_to_int(user_id))) % m
        hash_result.append(hashed_postition)

    return hash_result


bit_array = [0 for i in range(69997)]
