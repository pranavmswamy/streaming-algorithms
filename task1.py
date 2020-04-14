# BLOOM FILTER
from sys import argv
from binascii import hexlify
from blackbox import BlackBox
from time import time


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
    num_hashes = 10  # change in driver() func also if you change it here.
    for i in range(1, num_hashes + 1):
        hashed_position = (h1(user_to_int(user_id)) + i * h2(user_to_int(user_id))) % m
        hash_result.append(hashed_position)

    return hash_result


def bloom_filter(bit_array, stream_users, previous_users):
    """
    :param bit_array: bit array for bloom filter
    :param stream_users: list of user_ids (string).
    :param previous_users: set of previously seen users
    :return: list storing index of data batch and false positive rate for that batch of data.
    """
    false_positive = 0
    true_negative = 0
    for user in stream_users:
        already_set_count = 0
        positions_to_set = myhashs(user)
        found_true_negative = False

        for position in positions_to_set:
            if bit_array[position] == 0:
                bit_array[position] = 1
                previous_users.add(user)
                found_true_negative = True
            else:
                already_set_count += 1

        if found_true_negative:
            true_negative += 1

        if already_set_count == len(positions_to_set):
            # user already seen before | could be false positive.
            if user not in previous_users:  # false positive.
                false_positive += 1
                previous_users.add(user)  # adding false positive user to set of previous seen users.

    return false_positive / (false_positive + true_negative)


def driver():
    bx = BlackBox()
    num_of_asks = int(argv[3])
    stream_size = int(argv[2])
    fpr = []
    bit_array = [0 for _ in range(69997)]
    previous_users = set()

    for i in range(num_of_asks):
        stream_users = bx.ask(str(argv[1]), stream_size)
        batch_fpr = bloom_filter(bit_array, stream_users, previous_users)
        fpr.append((i, batch_fpr))

    for f in fpr:
        print(f)

    with open(str(argv[4]), "w") as file:
        file.write("Time,FPR")
        for f in fpr:
            file.write("\n" + str(f[0]) + "," + str(f[1]))
        file.close()


start_time = time()
driver()
print("Time taken = ", time() - start_time, "s")
