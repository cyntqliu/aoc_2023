import argparse
import re

# three rules:
# if period, ignore. If we had a number accumulated at this point, and it's a part
#     add its value to sum. Regardless, set the running number back to 0
# if number, build up the current number (multiply current number by 10 then add new digit)
#     also, the number isn't part of a part, search the vincinity of the number. If,
#     adjacent to a symbol, mark it as being part of a part
# if symbol, we can also just ignore it for part 1 (do the same thing as period),
#     but we likely want a separate condition ready for part 2

def main(args):
    part_sum = 0
    with open(args.input, 'r') as f:
        # first preprocess everything into an array so we know the total number of lines
        parts_arr = f.readlines()

    num_lines = len(parts_arr)
    cur_num = 0
    is_part = False
    for row, line in enumerate(parts_arr):
        if cur_num and is_part: # add any end-of-line part numbers
            part_sum += cur_num
        cur_num = 0 # assume all numbers are on one line
        is_part = False
        for col, char in enumerate(line):
            if not(re.match(r'\d', char)): # either period or symbol
                if char == '.':
                    pass
                else:
                    pass

                if cur_num and is_part:
                    part_sum += cur_num

                cur_num = 0
                is_part = False
            else:
                cur_num = cur_num * 10 + int(char)
                # search in the vincinity of cur_num for symbols
                # if we aren't already part of a part
                up_valid = False
                down_valid = False
                left_valid = False
                right_valid = False
                if not(is_part):
                    if row > 0:
                        up_valid = True
                        # search up
                        if not(re.match(r'\d', parts_arr[row-1][col])) and parts_arr[row-1][col] != '.':
                            is_part = True
                    if row < num_lines - 1:
                        down_valid = True
                        # search down
                        if not(re.match(r'\d', parts_arr[row+1][col])) and parts_arr[row+1][col] != '.':
                            is_part = True
                    if col > 0:
                        left_valid = True
                        # search left
                        if not(re.match(r'\d', parts_arr[row][col-1])) and parts_arr[row][col-1] != '.':
                            is_part = True
                    if col < len(line) - 1:
                        right_valid = True
                        # search right
                        if not(re.match(r'\d', parts_arr[row][col+1])) and parts_arr[row][col+1] != '.':
                            is_part = True

                    # diagonals
                    if up_valid and left_valid:
                        if not(re.match(r'\d', parts_arr[row-1][col-1])) and parts_arr[row-1][col-1] != '.':
                            is_part = True
                    if up_valid and right_valid:
                        if not(re.match(r'\d', parts_arr[row-1][col+1])) and parts_arr[row-1][col+1] != '.':
                            is_part = True
                    if down_valid and left_valid:
                        if not(re.match(r'\d', parts_arr[row+1][col-1])) and parts_arr[row+1][col-1] != '.':
                            is_part = True
                    if down_valid and right_valid:
                        if not(re.match(r'\d', parts_arr[row+1][col+1])) and parts_arr[row+1][col+1] != '.':
                            is_part = True

    if cur_num and is_part: part_sum += cur_num
    # this isn't right and I am not sure why
    print (f"Sum of all part ids: {part_sum}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        help="input file to the question"
    )

    args = parser.parse_args()
    main(args)