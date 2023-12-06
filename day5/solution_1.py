import argparse
import math
import re


def process_input(f):
    # turns the text of the input file to a friendlier format:
    # returns: (seeds, all_mappings)
    # where seeds is a List[int] and all_mappings is List[List[tuple]]
    seeds = f.readline().split(':')[1]
    seeds = [int(s) for s in seeds.split()]

    # skip the next line, which is blank
    f.readline()
    all_mappings = []; mapping = []
    for line in f.readlines():
        # if the line has alpha, skip it
        if re.match(r'[a-zA-Z]', line): 
            continue
        elif len(line) < 2:
            # if the line is empty, we just finished a section --> convert mapping and add to all_mappings
            all_mappings.append(mapping)
            mapping = []
        else: # mapping line
            mapping.append(tuple(line.split()))

    # add the last mapping
    all_mappings.append(mapping)
    return seeds, all_mappings


def main(args):
    # assume all mappings are in order
    with open(args.input, 'r') as f:
        seeds, all_mappings = process_input(f)

        # check every single seed
        cur_min_location = math.inf
        for seed in seeds:
            # to do each conversion, start with the seed value, then add
            # every adjustment value in the mapping for each mapping in all_mappings
            # assume that the input is valid: there are no contradictory mappings
            # for the same src

            print (f"SEED: {seed}")
            seed_location = seed
            for mapping in all_mappings:
                for tup in mapping:
                    dest, src, rng = tup
                    dest = int(dest); src = int(src); rng = int(rng)
                    # check if the cur_loc is between src and src + rng - 1
                    if src <= seed_location and seed_location < src + rng:
                        adjustment = dest - src
                        seed_location += adjustment
                        break
                # print (f"current transformation: {seed_location}")

            if seed_location < cur_min_location:
                cur_min_location = seed_location

            # print ("="*50)

    print (f"Minimum location: {cur_min_location}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        help="input file to the question"
    )

    args = parser.parse_args()
    main(args)