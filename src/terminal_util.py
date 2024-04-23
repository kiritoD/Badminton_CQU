import sys


def clear_lines(num_lines: int):
    # Move the cursor up 'num_lines' lines
    sys.stdout.write("\033[{}A".format(num_lines))
    # Clear the lines
    sys.stdout.write("\033[2K" * num_lines)
    # Move the cursor back to the beginning of the first cleared line
    sys.stdout.write("\033[{}G".format(0))
    sys.stdout.flush()


def clear_lines_from_b_to_u(num_lines: int = 1):
    for _i in range(num_lines, -1, -1):
        # Move the cursor up 'num_lines' lines
        sys.stdout.write("\033[1A")
        # Clear the lines
        sys.stdout.write("\033[2K")
    # Move the cursor back to the beginning of the first cleared line
    sys.stdout.write("\033[{}G".format(0))
