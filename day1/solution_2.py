import argparse
import re


word_to_num = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

def main(args):
    input_file = args.input
    file = open(input_file, 'r')

    total = 0
    # for idx, line in enumerate(file):
    for line in file:
        # can assume every line is valid and has no zeroes

        # the following does not work on its own because it only gets non-overlapping patterns
        # as a result, a pattern like twone will only result in "two"
        # all_digits = re.findall(r'\d|one|two|three|four|five|six|seven|eight|nine', line)

        # to overcome this, we can search for the first digit from left to right,
        # then search for the last digit from right to left
        first_digit = re.search(r'\d|one|two|three|four|five|six|seven|eight|nine', line)[0]
        last_digit = re.search(r'\d|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin', line[::-1])[0]
        last_digit = last_digit[::-1]

        if len(first_digit) > 1:
            first_digit = word_to_num[first_digit]
        if len(last_digit) > 1:
            last_digit = word_to_num[last_digit]
        num = int(first_digit + last_digit)
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
