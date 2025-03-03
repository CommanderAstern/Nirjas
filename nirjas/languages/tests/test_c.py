#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
SPDX-License-Identifier: LGPL-2.1

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
'''

import unittest
import os
from nirjas.languages import c
from nirjas.binder import readSingleLine, readMultiLineDiff, contSingleLines


class CTest(unittest.TestCase):
    '''
    Test cases for C language.
    :ivar testfile: Location of test file
    '''
    testfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), "TestFiles/textcomment.c")

    def test_output(self):
        '''
        Check for the scan correctness.
        '''
        regex = r'''(?<![pst'"`]:)\/\/\s*(.*)'''
        syntax_start = "/*"
        syntax_end = '*/'
        comment_single = readSingleLine(self.testfile, regex)
        comment_multiline = readMultiLineDiff(self.testfile, syntax_start,
                                                syntax_end)
        comment_contSinglelines = contSingleLines(comment_single)
        self.assertTrue(comment_single)
        self.assertTrue(comment_multiline)
        self.assertTrue(comment_contSinglelines)

    def test_outputFormat(self):
        '''
        Check for the output format correctness.
        '''
        regex = r'''(?<![pst]:)\/\/\s*(.*)'''
        syntax_start = "/*"
        syntax_end = "*/"
        expected = c.cExtractor(self.testfile).get_dict()
        comment_single = readSingleLine(self.testfile, regex)
        comment_multiline = readMultiLineDiff(self.testfile, syntax_start,
                                              syntax_end)
        comment_contSinglelines = contSingleLines(comment_single)
        file = self.testfile.split("/")
        output = {
        "metadata": {
        "filename": file[-1],
        "lang": "C",
        "total_lines": comment_single[1],
        "total_lines_of_comments": comment_single[3] + comment_multiline[3],
        "blank_lines": comment_single[2],
        "sloc": comment_single[1] - (comment_single[3] + comment_multiline[3] + comment_single[2])
        },
        "single_line_comment": [],
        "cont_single_line_comment": [],
        "multi_line_comment": []
        }

        if comment_contSinglelines:
            comment_single = comment_contSinglelines[0]

        if comment_single:
            for i in comment_single[0]:
                output['single_line_comment'].append({"line_number":i[0], "comment": i[1]})

        if comment_contSinglelines:
            for idx, _ in enumerate(comment_contSinglelines[1]):
                output['cont_single_line_comment'].append({
                  "start_line": comment_contSinglelines[1][idx],
                  "end_line": comment_contSinglelines[2][idx],
                  "comment": comment_contSinglelines[3][idx]})

        if comment_multiline:
            for idx, _ in enumerate(comment_multiline[0]):
                output['multi_line_comment'].append({
                  "start_line": comment_multiline[0][idx],
                  "end_line": comment_multiline[1][idx],
                  "comment": comment_multiline[2][idx]})
        self.assertEqual(output, expected)

    def test_Source(self):
        '''
        Test the source code extraction.
        Call the source function and check if new file exists.
        '''
        name = "source.txt"
        newfile = c.cSource(self.testfile, name)

        self.assertTrue(newfile)
