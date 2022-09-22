import os

blu="\033[01;94m"
g="\033[01;92m"
y="\033[01;93m"
p="\033[01;95m"
r="\033[01;91m"
cy="\033[01;96m"
w="\033[01;97m"
u="\033[04m"
ru="\033[24m"
cl="\033[00m"

bblu="\033[44m"
blbl="\033[104m"
br="\033[41m"
blr="\033[101m"
bg="\033[42m"
blg="\033[102m"
by="\033[43m"
bly="\033[103m"
bp="\033[45m"
blp="\033[105m"
bc="\033[46m"
blcy="\033[106m"

bld="\033[01m"
f="\033[02m"
i="\033[03m"
u="\033[04m"
bl="\033[05m"
rev="\033[07m"
hid="\033[08m"

rb="\033[21m"
rf="\033[22m"
ri="\033[23m"
ru="\033[24m"
rbl="\033[25m"
rr="\033[27m"
rh="\033[28m"

blank_line = f"{hid}blank{rh}"
sps = f"{hid} .{rh}"
spe = f"{hid}. {rh}"
sp3 = f"{hid} s {rh}"
sp4 = f"{hid} sp {rh}"
sp5 = f"{hid} spa {rh}"
color_swap = False

colors_and_effects = [blu,g,y,p,r,cy,w,cl,bblu,blbl,br,blr,bg,blg,by,bly,bp,blp,bc,blcy,bld,f,i,u,bl,rev,hid,rb,rf,ri,ru,rbl,rr,rh]
special_characters = chars = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "+", "=", "[", "]", "{", "}", "|", "\\", ";", "\"", "'", ",", ".", "/", "?", "<", ">", "`", "~", ":", " "]

char_line = f"{p}"
for char in special_characters:
    char_line += f" {char} "

def run_commands(*args):
    [os.system(command) for command in args]


def add_lines(*lines):
    [print(line) for line in lines]


def add_lines_to_file(*lines):
    file = []
    [file.append(f"{line}\n") for line in lines]
    return file


def insert_at_next(contents, entry, *lines):
    index = contents.index(entry) + 1
    [contents.insert(index, line) for line in lines]


def replace_line(contents, entry, *lines):
    index= contents.index(entry)
    contents.remove(entry)
    [contents.insert(index, line) for line in lines]


def update_section(remove_lines, contents, entry, *lines):
    index = contents.index(entry)
    while remove_lines > 0:
        del contents[index]
        remove_lines -= 1
    [contents.insert(index, line) for line in lines]


def rabbit_list(dictionary):
    needs_rabbit = []
    for key in dictionary.keys():
        if key not in needs_rabbit:
            needs_rabbit.append(key)
    for value in dictionary.values():
        for service in value:
            if service not in needs_rabbit:
                needs_rabbit.append(service)
    return needs_rabbit


def box_top(size, col1, col2):
    if size == "small":
        add_lines(
            "\n",
            f"           {col1}                                                          {cl}",
            f"           {col1}  {col2}                                                      {col1}  {cl}",
        )
    if size == "large":
        add_lines(
        "\n",
        f"  {col1}                                                                            {cl}",
        f"  {col1}  {col2}                                                                        {col1}  {cl}",
        )


def box_bottom(size, col1, col2):
    if size == "small":
        add_lines(
            f"           {col1}  {col2}                                                      {col1}  {cl}",
            f"           {col1}                                                          {cl}",
            "\n"
        )
    if size == "large":
        add_lines(
            f"  {col1}  {col2}                                                                        {col1}  {cl}",
            f"  {col1}                                                                            {cl}",
            "\n"
        )


def multiple_lines_in_box(size, col1, col2, *lines):
    for line in lines:
        line_in_box(size, col1, col2, line)


def swap(color_swap):
    return not color_swap


def message_box(size, col1, col2, *lines):
    box_top(size, col1, col2)
    multiple_lines_in_box(size, col1, col2, *lines)
    box_bottom(size, col1, col2)


def swapping_box(size, col1, col2, *lines, color_swap=color_swap):
    if color_swap:
        col1, col2 = col2,col1
    box_top(size, col1, col2)
    multiple_lines_in_box(size, col1, col2, *lines)
    box_bottom(size, col1, col2)


def get_adjustments(word):
    adjusted_length = len(word)
    adjustment = 0
    for item in colors_and_effects:
        if item in word:
            updated_word = word[:]
            factor = 0
            while item in updated_word:
                index = updated_word.index(item)
                updated_word = updated_word[index + len(item):]
                factor += 1
            adjustment += len(item) * factor
            adjusted_length -= len(item) * factor
    return adjustment, adjusted_length


def line_in_box(size, col1, col2, string):
    space = " "
    if size == "small":
        start = f"           {col1}  {col2}  {cl}{y}{space}{space}"
        limit = 48
    else:
        start = f"  {col1}  {col2}  {cl}{y}{space}{space}"
        limit = 66
    end = f"{col2}  {col1}  {cl}"
    array = string.split()
    total_adjustment = 0
    total = 0
    next_line = []
    full_block = []
    for i, word in enumerate(array):
        adjustment, adjusted_length = get_adjustments(word)
        if adjusted_length > limit - 2:
            long_word = word
            adjustment_lw, adjusted_length_lw = get_adjustments(long_word)
            while adjusted_length_lw > limit -2:
                start_index = limit - 2
                index = start_index
                word_piece = long_word[:index]
                adjustment_wp, adjusted_length_wp = get_adjustments(word_piece)
                while adjusted_length_wp < limit - 2:
                    if long_word[index + 1] == '\x1b':
                        ind = index + 1
                        steps = 1
                        ch = long_word[ind]
                        while ch != "m":
                            ind += 1
                            steps += 1
                        index += steps + 1
                        word_piece = long_word[:index]
                        adjustment_wp, adjusted_length_wp = get_adjustments(word_piece)
                    else:
                        index += 1
                        word_piece = long_word[:index]
                        adjustment_wp, adjusted_length_wp = get_adjustments(word_piece)
                full_block.append(f"{word_piece}  ")
                long_word = long_word[index:]
                adjustment_lw, adjusted_length_lw = get_adjustments(long_word)
            word = long_word
            adjustment, adjusted_length = get_adjustments(word)
        if total + adjusted_length > limit - 2:
            line = " ".join(next_line)
            remainder = limit + total_adjustment - len(line)
            for n in range(remainder):
                line = line + space
            full_block.append(line)
            total_adjustment = adjustment
            total = adjusted_length + 1
            next_line = []
            next_line.append(word)
            if i == len(array) - 1:
                line = " ".join(next_line)
                remainder = limit + total_adjustment - len(line)
                for i in range(remainder):
                    line = line + space
                full_block.append(line)
        else:
            total += adjusted_length + 1
            total_adjustment += adjustment
            next_line.append(word)
            if i == len(array) - 1:
                line = " ".join(next_line)
                remainder = limit + total_adjustment - len(line)
                for n in range(remainder):
                    line = line + space
                full_block.append(line)
    for line in full_block:
        new_string = f"{start}{line}{end}"
        line = new_string
        print(line)