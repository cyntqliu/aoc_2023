import argparse
import math
import re


def process_input(f):
    # turns the text of the input file to a friendlier format:
    # returns: (seeds, all_mappings)
    # where seeds is a List[tuple[int, int]] and all_mappings is List[List[tuple]]
    seeds = f.readline().split(':')[1]
    seeds = [int(s) for s in seeds.split()]
    seeds = [(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]

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
            t = tuple(int(num) for num in line.split())
            mapping.append(t)

    # add the last mapping
    all_mappings.append(mapping)
    return seeds, all_mappings


def check_overlap(interval_1_start, interval_1_rng, interval_2_start, interval_2_rng):
    return (interval_1_start <= interval_2_start and interval_2_start < interval_1_start + interval_1_rng) or \
                (interval_2_start <= interval_1_start and interval_1_start < interval_2_start + interval_2_rng)


def main(args):
    # assume all mappings are in order
    with open(args.input, 'r') as f:
        seeds, all_mappings = process_input(f)

        # procedure:
        # for every seed range, check for overlaps --> convert to dest ranges
        # do this iteratively for each set of mappings.
        # Note that the initial seed range can be interpreted as a list of src ranges
        # with length 1
        min_location = math.inf
        for seed_range in seeds:
            cur_ranges = [seed_range]

            for midx, mapping in enumerate(all_mappings):
                dest_ranges = []
                for cur_rng in cur_ranges:
                    src_start, src_rng = cur_rng
                    identity_mapped_sections = [cur_rng]
                    # check, for all mappings, if any overlap with the cur_rng
                    
                    for tup in mapping:
                        dest_map, src_map, rng_map = tup
                        if (check_overlap(src_start, src_rng, src_map, rng_map)):
                            adjustment = dest_map - src_map
                            # adjustment range starts at max(src_map, src_start) and ends at 
                            # min(src_start + src_rng, src_map + rng_map). Inside that range, everything is offset by
                            # adjustment
                            pre_converted_start = max(src_map, src_start)
                            dest_rng = min(src_start + src_rng, src_map + rng_map) - pre_converted_start
                            dest_start = pre_converted_start + adjustment
                            dest_ranges.append((dest_start, dest_rng))

                            # update the identity_mapped_section to not include the new non-identity-mapped section
                            # do this by checking the exact nature of the overlap

                            # 5 cases: adjustment range deletes the left side of section,
                            # adjustment range deletes the right side of section,
                            # adjustment range contains the entire section, the section contains
                            # the entire adjustment range, or no overlap

                            new_identity_sections = []
                            for section in identity_mapped_sections:
                                section_start, section_rng = section
                                if (pre_converted_start <= section_start):
                                    if (
                                        pre_converted_start + dest_rng > section_start and \
                                        pre_converted_start + dest_rng < section_start + section_rng
                                    ):
                                        new_identity_sections.append( # delete the left side, which is included in the adjustment range
                                            (pre_converted_start + dest_rng,
                                            (section_start + section_rng) - (pre_converted_start + dest_rng))
                                        )
                                    elif (
                                        pre_converted_start + dest_rng >= section_start + section_rng
                                    ): # full overlap, skip to the next section
                                        continue
                                elif (section_start < pre_converted_start):
                                    if ( # note: if we are here, there is no full overlap
                                        section_start + section_rng > pre_converted_start # check for any overlap
                                    ): 
                                        new_identity_sections.append( # delete the right side
                                            (section_start, pre_converted_start - section_start)
                                        )
                                        # we do not need to check full overlap again, but now we need to check
                                        # if the section contains the entire adjustment range -- add an extra
                                        # new identity section on the right
                                        if pre_converted_start + dest_rng < section_start + section_rng:
                                            new_identity_sections.append(
                                                (pre_converted_start + dest_rng,
                                                (section_start + section_rng) - (pre_converted_start + dest_rng))
                                            )
                            identity_mapped_sections = new_identity_sections
                    dest_ranges.extend(identity_mapped_sections) # account for all possible values in the current range
                
                cur_ranges = dest_ranges
                print (f"current ranges: {cur_ranges} at mapping level {midx}")

            # the minimum location is a starting location in one of the final ranges
            min_location = min(min_location, min([rng[0] for rng in cur_ranges]))

    print (f"Minimum location: {min_location}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        help="input file to the question"
    )

    args = parser.parse_args()
    main(args)