#!/usr/bin/env python
#  -*- coding: utf-8 -*-


import unittest
import os
from metexpy.metexpy import *


def to_test_data(*args):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", *args)


class RenameTestCase(unittest.TestCase):

    def test_replace_substrings(self):
        names = ["CDP-DG(16:0/16:0)", "PE(18:0/18:2)"]
        names_results = ["CDP-DG(16:0/16:0)", "PE(18:0/18:2)"]
        for i in range(len(names)):
            self.assertEqual(replace_substrings(names[i]), names_results[i])

    def test_extract_fatty_acids(self):
        names = ["CDP-DG(16:0/16:0)", "PE(18:0/18:2)", "DG(11D3/11D3/0:0)"]
        names_results = [[], [], ["11D3", "11D3"]]
        for i in range(len(names)):
            self.assertEqual(extract_fatty_acids(names[i]), names_results[i])

    def test_sum_fatty_acid_chains(self):
        names = ["CDP-DG(16:0/16:0)", "PE(18:0/18:2)", "DG(11D3/11D3/0:0)"]
        names_results = [(32, 0), (36, 2), (0, 0)]
        for i in range(len(names)):
            facs = extract_fatty_acid_chains(names[i])
            self.assertEqual(sum_fatty_acid_chains(facs), names_results[i])

    def test_simplify(self):
        for db in ["hmdb", "lipidmaps"]:
            with open(to_test_data("{}_records.txt".format(db)), "r") as inp:
                inp.readline()
                for line in inp.read().splitlines():
                    line = line.split("\t")
                    if "unknown" not in line[1] and line[2] != "skip":
                        name_l_s = simplify(add_lyso(line[0]))
                        self.assertEqual(name_l_s, line[1])

    def test_add_lyso(self):
        names = ["PA(0:0/16:0)", "PA(0:0/18:2(9Z,12Z))", "PE(18:0/18:2)", "DG(11D3/11D3/0:0)"]
        names_results = ["LysoPA(16:0)", "LysoPA(18:2)", "PE(36:2)", "DG(11D3/11D3)"]
        for i in range(len(names)):
            self.assertEqual(simplify(add_lyso(names[i])), names_results[i])

if __name__ == '__main__':
    unittest.main()
