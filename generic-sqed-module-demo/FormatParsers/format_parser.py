def constraint(line):
    return line.find("CONSTRAINT") != -1

def comment(line):
    return line.find("#") != -1

def definition(line):
    return line.find("=") != -1

def field(line):
    return line[0] == "_"

def get_info(lines):
    info = {}
    inner_info = {}
    constraints = []
    name = None

    if constraint(lines[0]):
        while lines[0] != "\n":
            line = lines[0]
            constraints.append(line[len("CONSTRAINT")+1:-1])
            lines = lines[1:]

    if len(constraints) > 0:
        info["CONSTRAINT"] = constraints
        constraints = []

    while not len(lines) == 0 and not field(lines[0]):
        line = lines[0]

        if line == "\n":
            lines = lines[1:]

        elif constraint(line):
            constraints.append(line[len("CONSTRAINT")+1:-1])
            lines = lines[1:]

        elif not comment(line) and not definition(line):
            if not name is None:
                inner_info["CONSTRAINT"] = constraints
                info[name] = inner_info
            name = line
            name = name[0:-1]
            inner_info = {}
            constraints = []
            lines = lines[1:]

        elif not comment(line):
            req = line
            req_index = req.find("=")
            req_name = req[0:req_index-1]
            req = req[req_index+2:-1]
            inner_info[req_name] = req
            lines = lines[1:]

        else:
            lines = lines[1:]

    if not name is None:
        inner_info["CONSTRAINT"] = constraints
        info[name] = inner_info
        if not "CONSTRAINT" in info:
            info["CONSTRAINT"] = []
        return info
    else:
        inner_info["CONSTRAINT"] = constraints
        return inner_info

def parse_format(filename):
    f = open(filename, 'r')
    lines = f.readlines()

    while lines[0].find("SECTIONS") == -1:
        lines = lines[1:]

    format_sections = lines[0]
    sections_index = format_sections.find("=")
    format_sections = format_sections[sections_index+2:]
    format_sections = format_sections.split()

    format_dicts = {}

    i = 1
    j = 0
    for line in lines[1:]:
        if field(line):
            format_name = format_sections[j]
            format_dicts[format_name] = get_info(lines[i+1:])
            j += 1
        i += 1

    f.close()

    return format_sections, format_dicts

"""
s, r = parse_format("../FormatFiles/RV32M-ridecore_format.txt")
print(s)
print("\n")
for key in r:
    print(key)
    print(r[key])
    print("\n")
"""





