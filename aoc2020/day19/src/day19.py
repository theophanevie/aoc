import sys
from typing import TextIO, Dict, Tuple, List
import re
from collections import defaultdict

rulestype = Dict[str, Tuple[bool, List[str]]]

def parse(inputfile: TextIO) -> Tuple[rulestype, List[str]]:
    """
    construct a dict [ruleid : (isfinal, list of ruleid or final letter)
    and the list of msgs
    """
    
    rules = {}
    for line in inputfile:
        line = line.strip()
        if line == "":
            break

        pos = line.find(':')

        split = [letter for letter in re.split(' |\"', line[pos + 1:]) if letter != '']
        rules[line[:pos]] = (len(split) == 1 and line.find("\"") != -1, split)

    msgs = [line.strip() for line in inputfile]

    return rules, msgs
    

def buildregexp_(rules : rulestype, rule, seen):
    """
    recursively build the regex with match all rules
    """
    seen[rule] += 1

    # if these two rules are seen too many times stop the recursion
    if seen[rule] > 50 and rule in ['8', '11']:
        return ''

    # return the final letter
    if rules[rule][0]:
        return rules[rule][1][0]

    regexp = '('
    for rule in rules[rule][1]:
        if rule == '|':
            regexp += '|'
        else:
            regexp += buildregexp_(rules, rule, seen)
    
    return regexp + ')'


def buildregexp(rules) -> str:
    """
    build the regex with match all rules
    """
    seen = defaultdict(lambda: 0)

    regexp = ''
    for rule in rules['0'][1]:
        regexp += buildregexp_(rules, rule, seen)

    return regexp


def check_firstpart(filename: str) -> int:
    with open(filename,'r') as inputfile:
        rules, msgs = parse(inputfile)

    r = re.compile(buildregexp(rules))

    cpt = 0
    for msg in msgs:

        res = r.match(msg)

        if res and res.group(0) == msg:
            cpt += 1

    return cpt

def check_secondpart(filename: str) -> int:
    return check_firstpart(filename)

if __name__ == "__main__":
    print(f"firstpart {check_firstpart(sys.argv[1])}")
    print(f"secondpart {check_secondpart(sys.argv[1])}")
