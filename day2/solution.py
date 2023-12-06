import argparse
import math

from collections import defaultdict


def process_line(line):
    # for each game, return
    # output like [{"red": num_red, "green": num_green, "blue": num_blue}, ..., {}]
    line = line.split(':')[-1] # ignore game number, we can get that info from line index anyways

    draws = line.split(';')
    output = []
    for draw in draws:
        draw_dict = defaultdict(lambda: 0) # default to 0
        color_info = draw.split(',')
        for info in color_info: # assume no redundant colors
            count, color = info.split()
            draw_dict[color] = int(count)
        output.append(draw_dict)

    return output


def main(args):
    elf_bag = {"red": 12, "green": 13, "blue": 14}

    with open(args.input, 'r') as f:
        sum_games = 0
        sum_powers = 0

        for idx, line in enumerate(f):
            freq_dicts = process_line(line)
            min_bag = defaultdict(lambda: 0)

            is_valid = True
            for d in freq_dicts:
                # compare red/green/blue counts to bag
                if (
                    d["red"] > elf_bag["red"] or \
                    d["green"] > elf_bag["green"] or \
                    d["blue"] > elf_bag["blue"]
                ):
                    is_valid = False

                # compute the min bag needed for this game to be valid
                min_bag["red"] = max(min_bag["red"], d["red"])
                min_bag["green"] = max(min_bag["green"], d["green"])
                min_bag["blue"] = max(min_bag["blue"], d["blue"])
            
            if is_valid:
                sum_games += idx + 1
            
            sum_powers += min_bag["red"] * min_bag["green"] * min_bag["blue"]

    print (f"Sum of game ids: {sum_games}")
    print (f"Sum of game powers: {sum_powers}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        help="input file to the question"
    )

    args = parser.parse_args()
    main(args)
