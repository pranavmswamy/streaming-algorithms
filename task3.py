# RESERVOIR SAMPLING
from sys import argv
from blackbox import BlackBox
from time import time
import random


def driver():
    random.seed(553)
    reservoir = [0] * 100
    sequence_no = 0
    num_of_asks = int(argv[3])
    stream_size = int(argv[2])
    bx = BlackBox()
    results = []

    for _ in range(num_of_asks):
        stream_users = bx.ask(str(argv[1]), stream_size)
        for user in stream_users:
            sequence_no += 1
            if sequence_no <= 100:
                reservoir[sequence_no - 1] = user
            else:
                # reservoir full.
                # choose to keep user with prob 100 / sequence_no.
                p_keep_user = random.randint(0, 100000) % sequence_no
                if p_keep_user < 100:
                    # have to keep user.
                    # replace one elt in reservoir with uniform prob.
                    position_to_replace = random.randint(0, 100000) % 100
                    reservoir[position_to_replace] = user

            if sequence_no % 100 == 0:
                results.append(str(
                    str(sequence_no) + "," + reservoir[0] + "," + reservoir[20] + "," + reservoir[40] + "," + reservoir[
                        60] + "," + reservoir[80]))

    return results


start_time = time()
reservoir_snapshot = driver()

for i in reservoir_snapshot:
    print(i)

with open(str(argv[4]), "w") as file:
    file.write("seqnum,0_id,20_id,40_id,60_id,80_id")
    for line in reservoir_snapshot:
        file.write("\n")
        file.write(line)
    file.close()

print("Time taken:", time() - start_time, "s")
