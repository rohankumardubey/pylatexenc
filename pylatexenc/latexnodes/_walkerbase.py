# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
# 
# Copyright (c) 2021 Philippe Faist
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#


# Internal module. Internal API may move, disappear or otherwise change at any
# time and without notice.

from __future__ import print_function, unicode_literals


class LatexWalkerBase(object):
    def __init__(self, **kwargs):
        super(LatexWalkerBase, self).__init__(**kwargs)

    def parse_content(self, parser, token_reader=None, parsing_state=None,
                      open_context=None, **kwargs):
        raise RuntimeError("LatexWalkerBase subclasses must reimplement parse_content()")

    def make_node(self, node_class, **kwargs):
        raise RuntimeError("LatexWalkerBase subclasses must reimplement make_node()")

    def make_nodes_collector(self,
                             token_reader,
                             parsing_state,
                             **kwargs):
        raise RuntimeError(
            "LatexWalkerBase subclasses must reimplement make_nodes_collector()")


    def check_tolerant_parsing_ignore_error(self, exc):
        r"""
        You can inspect the exception object `exc` and decide whether or not to
        attempt to recover from the exception (if you want to be tolerant to
        parsing errors).

        Return the exception object if it should be raised, or return None if
        recovery should be attempted.
        """
        return exc
