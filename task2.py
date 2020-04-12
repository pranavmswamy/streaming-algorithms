# FLAJOLET MARTIN ALGORITHM
from binascii import hexlify
from sys import argv
from blackbox import BlackBox
from time import time
from random import randint


def user_to_int(user_id):
    return int(hexlify(user_id.encode('utf8')), 16)


def myhashs(user_id):
    # Converting a string user_id to an int number,
    # Then passing that int number through two hash fns h1 and h2
    # Combining the results as h1(x) + i * h2(x)
    # Converting that combined result into a binary number and storing it.

    p = 943661897

    def h(x):
        a1 = randint(1, 959803989)
        b1 = randint(1, 959803989)
        return (a1 * x + b1) % p

    hash_result = []
    num_hashes = 500  # change it in f_m func also if you change it here.
    for _ in range(1, num_hashes + 1):
        hash_result.append(h(user_to_int(user_id)))

    return hash_result


def hash_to_trailing_zeroes(hash_array):
    trailing_zeroes = []
    # converting to 64 bits binary number
    for hash_num in hash_array:
        hashed_binary_num = f'{hash_num:016b}'
        # extracting the number of trailing zeroes
        # print("Number: ", hashed_binary_num)
        num_trailing_zeroes = len(hashed_binary_num) - len(hashed_binary_num[:].rstrip("0"))
        # print("Num of trailing zeroes: ", num_trailing_zeroes)
        if num_trailing_zeroes >= 11:
            trailing_zeroes.append(0)
        else:
            trailing_zeroes.append(num_trailing_zeroes)

    return trailing_zeroes


def flajolet_martin(stream_users):
    num_hashes = 500  # change in myhashs func also if you change it here.

    max_trailing_zeroes = [0] * num_hashes
    for user in stream_users:
        hashes = myhashs(user)
        trailing_zeroes = hash_to_trailing_zeroes(hashes)

        for i in range(len(max_trailing_zeroes)):
            if trailing_zeroes[i] > max_trailing_zeroes[i]:
                max_trailing_zeroes[i] = trailing_zeroes[i]

    # at this point I'll have all max trailing zeroes after going through all users and all hash functions - in max_\
    # trailing_zeroes.
    # print("Max trailing zeroes = ", max_trailing_zeroes)
    estimates = [2 ** r for r in max_trailing_zeroes]

    # combine all r's to one single R and return it.
    # print("Estimates = ", estimates)
    #print(estimates)
    split_num = 4
    avg_list = [sum(estimates[i:i + split_num]) / split_num for i in range(0, len(estimates), split_num)]
    # print("Avg list = ", sorted(avg_list))

    # return median of avg_list
    return (avg_list[len(avg_list)//2] + avg_list[len(avg_list)//2 + 1]) // 2


def driver():
    bx = BlackBox()
    num_of_asks = 30
    results = []



    for i in range(num_of_asks):
        stream_users = bx.ask("users.txt", 300)
        ground_truth = set()
        for user in stream_users:
            ground_truth.add(user)
        estimation = flajolet_martin(stream_users)
        results.append((i, len(ground_truth), estimation))

    sum_estimations = 0
    sum_ground_truth = 0
    for i in results:
        print(i)
        sum_ground_truth += i[1]
        sum_estimations += i[2]

    print("Final Result = ", i[2]/i[1])


driver()
