# Copyright (c) Stanford University
# 
# This source code is patent protected and being made available under the
# terms explained in the ../LICENSE-Academic and ../LICENSE-GOV files.

# Author: Mario J Srouji
# Email: msrouji@stanford.edu

def constraint(line):
    return line.find("CONSTRAINT") != -1

def comment(line):
    return line.find("#") != -1

def definition(line):
    return line.find("=") != -1

def field(line):
    return line[0] == "_"

# Main function for parsing data related to a specific section
def get_info(lines):
    info = {}
    inner_info = {}
    constraints = []
    name = None

    # Skip lines
    while (comment(lines[0]) or lines[0] == "\n"):
        lines = lines[1:]

    while constraint(lines[0]):
        line = lines[0]
        constraints.append(line[len("CONSTRAINT")+1:-1])
        lines = lines[1:]

    if len(constraints) > 0:
        info["CONSTRAINT"] = constraints
        constraints = []

    while (len(lines) > 0 and not field(lines[0])):
        line = lines[0]

        if (comment(line) or line == "\n"):
            lines = lines[1:]

        elif constraint(line):
            constraints.append(line[len("CONSTRAINT")+1:-1])
            lines = lines[1:]

        elif definition(line):
            req = line
            req_index = req.find("=")
            req_name = req[0:req_index-1]
            req = req[req_index+2:-1]
            if req_name in inner_info:
                if type(inner_info[req_name]) == type([]):
                    inner_info[req_name].append(req)
                else:
                    inner_info[req_name] = [inner_info[req_name], req]
            else:
                inner_info[req_name] = req
            lines = lines[1:]

        else:
            if not name is None:
                inner_info["CONSTRAINT"] = constraints
                info[name] = inner_info
            name = line
            name = name[0:-1]
            inner_info = {}
            constraints = []
            lines = lines[1:]

    if not name is None:
        inner_info["CONSTRAINT"] = constraints
        info[name] = inner_info
        if not "CONSTRAINT" in info:
            info["CONSTRAINT"] = []
        return info, lines
    else:
        inner_info["CONSTRAINT"] = constraints
        return inner_info, lines

# Main parsing function
def parse_format(filename):
    error = False
    try:
        # Read in all lines in format file
        f = open(filename, 'r')
        lines = f.readlines()
    except:
        print("ERROR: Could not open format file")
        error = True
        quit()

    try:
        # First field in file must define all sections in file
        while (comment(lines[0]) or (lines[0] == "\n") or lines[0].find("SECTIONS") == -1):
            lines = lines[1:]
        format_sections = lines[0]
        sections_index = format_sections.find("=")
        format_sections = format_sections[sections_index+2:]
        format_sections = format_sections.split()
    except:
        if len(lines) == 0:
            print("ERROR: Could not find SECTIONS in Format File")
        else:
            print("ERROR: Issue in parsing SECTIONS in format file")
        error = True
        quit()

    format_dicts = {}

    # go through each section in the format file
    # and gather the data by section name
    i = 0
    lines = lines[1:]
    while len(lines) > 0:
        line = lines[0]
        if (comment(line) or line == "\n"):
            lines = lines[1:]  
        elif field(line):
            try:
                format_name = format_sections[i]
                if not line[1:-1] in format_name:
                    print("CHECK: SECTIONS field "+format_name+" and actual section "+line[1:-1]+" not aligned.")
                    print("Please make sure to include "+line[1:-1]+" section in SECTIONS.")
                    raise Exception()
            except:
                print("ERROR: Please make sure to list all format file sections in SECTIONS")
                error = True
                quit()
            try :
                format_dicts[format_name], lines = get_info(lines[1:])
            except:
                print("ERROR: Issue while parsing the following section: "+line[1:-1])
                error = True
                quit()

            i += 1
        else:
            print("CHECK: Skipping a line that is not a comment but is in between sections")
            error = True
            lines = lines[1:]

    f.close()

    if error:
        print("MESSAGE: Parser encountered weird lines that were skipped.")
    else:
        print("MESSAGE: Format File was read in without any issues.")
    return format_sections, format_dicts

# Helps in debugging and viewing
# what the parser is outputting, 
# and how it structures the data
def parser_display(f):
    sections, info = parse_format(f)
    print(sections)
    print("\n")
    for key in info:
        print(key)
        print(info[key])
        print("\n")

#parser_display("../FormatFiles/RV32M-ridecore_format.txt")

