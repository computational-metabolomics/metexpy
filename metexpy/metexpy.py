#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re


def add_lyso(name):
    if name[0] == "P" and re.subn("[^0-9]0:0[^0-9]", '', name)[1] == 1:
        return "Lyso{}".format(name)
    return name

def sum_fatty_acid_chains(facs):
    a, b = 0, 0
    for fac in facs:
        a += int(fac[0])
        b += int(fac[1])
    return a, b


def extract_fatty_acid_chains(name: str, debug: bool = False):
    regex = r"([0-9]+:[0-9]+)"

    matches = list(re.finditer(regex, name, re.VERBOSE))
    if len(matches) > 0:

        fac = []
        for matchNum, match in enumerate(matches, start=1):
            if debug:
                print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum,
                                                                                    start=match.start(),
                                                                                    end=match.end(),
                                                                                    match=match.group()))
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                if debug:
                    print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                                                                                    start=match.start(groupNum),
                                                                                    end=match.end(groupNum),
                                                                                    group=match.group(groupNum)))
                db = match.group(groupNum).split(":")
                fac.append((int(db[0]), int(db[1])))
        return fac
    return []


def extract_fatty_acids(name: str, debug: bool = False):
    regex = r"([0-9]+[A-Z]+[0-9]+)"

    matches = re.finditer(regex, name, re.MULTILINE)
    names = []

    for matchNum, match in enumerate(matches, start=1):

        if debug:
            print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum,
                                                                                 start=match.start(),
                                                                                 end=match.end(),
                                                                                 match=match.group()))

        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            if debug:
                print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                                                                                 start=match.start(groupNum),
                                                                                 end=match.end(groupNum),
                                                                                 group=match.group(groupNum)))
            names.append(match.group(groupNum))
    return names


def replace_substrings(name: str, debug: bool = False):

    # https://regex101.com/
    regex_strs = [r"\[?(rac|cis-?\sand\strans-?|trans|cis|iso\d*|L,|D,|DL,|L-|D-|DL-)-?\s?\]?",
                  r"\(([A-Z]|[0-9A-Z,]{2,})\)[-\s]?"] # "PE-Cer(d14:2(/24:1(2OH))"

    for regex in regex_strs:

        matches = list(re.finditer(regex, name, re.MULTILINE | re.VERBOSE))

        if len(matches) > 0:
            for matchNum, match in enumerate(matches, start=1):

                if debug:
                    print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
                                                                                    end=match.end(), match=match.group()))
                for groupNum in range(0, len(match.groups())):
                    groupNum = groupNum + 1

                if debug:
                    print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                                                                                    start=match.start(groupNum),
                                                                                    end=match.end(groupNum),
                                                                                    group=match.group(groupNum)))
                name = name.replace(match.group(), "")
    return name


def simplify(name: str, repl: bool = True, debug: bool = False):

    if repl:
        name = replace_substrings(name)

    matches = list(re.finditer(r""".*(\([iaD1n0-9\,\:\-\(\)\[\]\/]{8,}\)).*""", name, re.MULTILINE | re.VERBOSE))

    if len(matches) == 1:
        # print(name==matches[0].group(), matches[0].group(), matches[0].groups())
        if matches[0].group() == name:
            if debug:
                print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=1,
                                                                                    start=matches[0].start(),
                                                                                    end=matches[0].end(),
                                                                                    match=matches[0].group()))
            between_brackets = matches[0].groups()[0]
            # re.sub('[iaD-]', '', between_brackets)
            facs = extract_fatty_acid_chains(between_brackets)
            sum_facs = sum_fatty_acid_chains(facs)
            fans = extract_fatty_acids(between_brackets)

            bb = []
            if sum_facs[0] != 0 or sum_facs[1] != 0:
                bb.append("{a}:{b}".format(a=sum_facs[0], b=sum_facs[1]))
            bb.extend(fans)
            between_brackets_after = "({})".format("/".join(map(str, bb)))
            name = name.replace(between_brackets, between_brackets_after)

    return name
#
#
# def main():
#
#     # name = "TG(10:0/21:0/a-13:0)"
#     # name = strip(name, debug=True)
#     # print(name)
#     # name = simplify(name, debug=True)
#     # print(name)
#
#     path_names = os.path.join("..", "tests", "data", "hmdb_examples.txt")
#     with open(path_names) as names:
#         names.readline()
#         for line in names.readlines():
#             name, result, notes = line.strip().split("\t")
#             name = replace_substrings(name)
#
#             print()
#             # print("NOTES:", notes)
#             print(name, result, simplify(name), result == simplify(name))
#
#
# if __name__ == '__main__':
#     main()
