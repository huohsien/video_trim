import os
import sys

def getch():
    """Read single character from standard input without echo."""
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def yes_or_no(question):
    c = ""
    print(question + " (y/n): ", end="", flush=True)
    while c not in ("y", "n"):
        c = getch().lower()
    return c == 'y'

def check_timestamp_format(time_str, at_beginning):
    # print("check if '{}' is timestamp".format(time_str))
    comps = time_str.split('_')
    # print("len(comps)= ", len(comps))
    len_comps = len(comps)

    if len_comps == 0:
        # print("$1")
        return False

    if len_comps > 3:
        # print("#1")
        return False

    for comp in comps:
        try:
            n = int(comp)
            if n >= 100:
                # print("#2")
                return False

        except ValueError:
            # print("@2")
            return False

    if len_comps < 3:
        if at_beginning:
            # print("@3")
            return True
        else:
            # print("@4")
            return False
    # print("#3")
    return True

def main():

    if len(sys.argv) == 2:
        print("\n")
        full_path = sys.argv[1]
        path, tail = os.path.split(sys.argv[1])
        name1 = tail[:-4]
        name_parts = name1.split('-')
        filename_parts = []
        timestamp_parts = []
        # print("name_parts= ", name_parts)
        for idx, name_part in enumerate(name_parts):
            if check_timestamp_format(name_part, idx == 0):
                timestamp_parts.append(name_part)
            else:
                filename_parts.append(name_part)
        filename = '-'.join(filename_parts)+'.mp4'
        start_time = 'N/A'
        end_time = 'N/A'
        if len(timestamp_parts) == 2:
            start_time = timestamp_parts[0]
            end_time = timestamp_parts[1]
            start_time = start_time.replace('_', ':')
            end_time = end_time.replace('_', ':')
        if len(timestamp_parts) == 1:
            end_time = timestamp_parts[0]
            end_time = end_time.replace('_', ':')

        output_filename = os.path.join(path, filename)
        print('Input file: {}'.format(full_path))
        print("File name: {}".format(filename))
        print('Start time: {}'.format(start_time))
        print('End time: {}'.format(end_time))
        print('Output file: {}'.format(output_filename))
        if start_time == 'N/A':
            cmd_str = "time ffmpeg -i \"{}\" -vcodec copy -acodec copy -to {} \"{}\"" \
                .format(full_path, end_time, output_filename)
        else:
            cmd_str = "time ffmpeg -i \"{}\" -vcodec copy -acodec copy -ss {} -to {} \"{}\"" \
                .format(full_path, start_time, end_time, output_filename)

        # print("cmd_str= {}".format(cmd_str))

        if not yes_or_no("Start trimming?"):
            os._exit(0)
        else:
            os.system(cmd_str)

if __name__ == "__main__":
    main()
