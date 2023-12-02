import argparse
import re

def main(args):
    input_file = args.input
    file = open(input_file, 'r')

    total = 0
    for line in file:
        # can assume every line is valid
        all_digits = re.findall(r'\d', line)
        num = int(all_digits[0] + all_digits[-1])
        total += num

    print (f"calibration value: {total}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        help="input file to the question"
    )

    args = parser.parse_args()
    main(args)
