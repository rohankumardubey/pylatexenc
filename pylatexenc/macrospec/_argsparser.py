# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
# 
# Copyright (c) 2019 Philippe Faist
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

from ._parsedargsbase import ParsedMacroArgs


# for Py3
_basestring = str

## Begin Py2 support code
import sys
if sys.version_info.major == 2:
    # Py2
    _basestring = basestring
## End Py2 support code




.............. TRASH THIS CLASS DEFINITION ..........................

class MacroStandardArgsParser(object):
    r"""
    Parses the arguments to a LaTeX macro.

    ................................. REDO DOC .......................


    This class parses a simple macro argument specification with a specified
    arrangement of optional and mandatory arguments.

    This class also serves as base class for more advanced argument parsers
    (e.g. for a ``\verb+...+`` macro argument parser).  In such cases,
    subclasses should attempt to provide the most suitable `argspec` (and
    `argnlist` for the corresponding :py:class:`ParsedMacroArgs`) for their use,
    if appropriate, or set them to `None`.


    Arguments:

      - `argspec`: must be a string in which each character corresponds to an
        argument.  The character '{' represents a mandatory argument (single
        token or LaTeX group) and the character '[' denotes an optional argument
        delimited by braces.  The character '\*' denotes a possible star char at
        that position in the argument list, a corresponding
        ``latexwalker.LatexCharsNode('*')`` (or `None` if no star) will be
        inserted in the argument node list.  For instance, the string '\*{[[{'
        would be suitable to specify the signature of the '\\newcommand' macro.

    .................................

        Currently, the argspec string may only contain the characters '\*', '{'
        and '['.

        The `argspec` may also be `None`, which is the same as specifying an
        empty string.

      - `optional_arg_no_space`: If set to `True`, then an optional argument
        cannot have any whitespace between the preceeding tokens and the '['
        character.  Set this to `True` in cases such as for ``\\`` in AMS-math
        environments, where AMS apparently introduced a patch to prevent a
        bracket on a new line after ``\\`` from being interpreted as the
        optional argument to ``\\``.
    
      - `args_math_mode`: Either `None`, or a list of the same length as
        `argspec`.  If a list is given, then each item must be `True`, `False`,
        or `None`.  The corresponding argument (cf. `argspec`) is then
        respectively parsed in math mode (`True`), in text mode (`False`), or
        with the mode unchanged (`None`).  If `args_math_mode` is `None`, then
        all arguments are parsed in the same mode as the current mode.

      - additional unrecognized keyword arguments are passed on to superclasses
        in case of multiple inheritance

    Attributes:

    .. py:attribute:: argspec

       Argument type specification provided to the constructor.

    .. py:attribute:: optional_arg_no_space

       See the corresponding constructor argument.

    .. py:attribute:: args_math_mode

       See the corresponding constructor argument.
    """

.............. TRASH THIS CLASS DEFINITION ..........................

    class Argument:
        def __init__(self, arg_parser=None, arg_no=None):
            self.arg_no = arg_no
            self.arg_parser = arg_parser


    def __init__(self, argspec=None, environment_body_parser=None, **kwargs):
        super(MacroStandardArgsParser, self).__init__(**kwargs)

        self.argspec = argspec

        # only used for environments
        self.environment_body_parser = environment_body_parser

        # # catch bugs, make sure that argspec is a string with only accepted chars
        # if not isinstance(self.argspec, _basestring) or \
        #    not all(x in '*[{' for x in self.argspec):
        #     raise TypeError(
        #         "argspec must be a string containing chars '*', '[', '{{' only: {!r}"
        #         .format(self.argspec)
        #     )

        # legacy attributes
        self.optional_arg_no_space = kwargs.pop('optional_arg_no_space', False)
        self.args_math_mode = kwargs.pop('args_math_mode', None)

        # non-documented attribute that makes us ignore any leading '*'.  We use
        # this to emulate pylatexenc 1.x behavior when using the MacrosDef()
        # function explicitly
        self._like_pylatexenc1x_ignore_leading_star = \
            kwargs.pop('_like_pylatexenc1x_ignore_leading_star', False)


        # iteration works both for strings and lists
        self.arguments = [
            self._arg_instance(j, a)
            for (j, a) in enumerate(self.argspec)
        ]

        if self._like_pylatexenc1x_ignore_leading_star:
            raise RuntimeError("_like_pylatexenc1x_ignore_leading_star: NOT YET IMPLEMENTED")

        if self.optional_arg_no_space:
            raise RuntimeError("optional_arg_no_space: NOT YET IMPLEMENTED")


    def _arg_instance(self, arg_no, this_arg_spec):
        if isinstance(this_arg_spec, MacroStandardArgsParser.Argument):
            this_argument = this_arg_spec
        elif callable(this_arg_spec):
            # already an argument parser instance
            this_argument = MacroStandardArgsParser.Argument(arg_no=arg_no,
                                                             arg_parser=this_arg_spec)
        elif isinstance(this_arg_spec, _basestring):

            argkwargs = {}
            if self.args_math_mode is not None and self.args_math_mode[arg_no] is not None:
                argkwargs['is_math_mode'] = self.args_math_mode[arg_no]

            this_argument = MacroStandardArgsParser.Argument(
                arg_no=arg_no,
                arg_parser=LatexStandardArgumentParser(this_arg_spec, **argkwargs)
            )
        else:
            raise ValueError("Invalid arg_spec={!r}".format(this_arg_spec))

        return this_argument


    def describe(self, token):
        if token.tok == 'macro':
            return '\\'+main_token.arg
        if token.tok == 'environment':
            return '\\begin{' + token.arg + '}'
        if token.tok == 'specials':
            return token.arg.specials_chars



    class _InstanceParser(object):
        def __init__(self, mstdargsobj, arguments, main_token, node_class, **kwargs):
            super(InstanceParser, self).__init__(**kwargs)
            self.mstdargsobj = mstdargsobj
            self.arguments = arguments
            self.main_token = main_token
            self.node_class = node_class

        def __call__(self, latex_walker, token_reader, parsing_state, **kwargs):

            argnlist = []

            for arg in self.arguments:
                arg_no, arg_parser = arg
                argnodes, carryover_info = latex_walker.parse_content(
                    arg_parser,
                    token_reader,
                    parsing_state,
                    open_context=(
                        "Argument #{} of ‘{}’".format(arg_no,
                                                      self.mstdargsobj.describe(main_token)),
                        token_reader.cur_pos()
                    )
                )
                if carryover_info is not None:
                    logger.warning(
                        "Parsing carry-over information (%r) ignored when parsing arguments!",
                        carryover_info
                    )
                argnlist.append( argnodes )

            parsed = ParsedMacroArgs(
                argspec=self.mstdargsobj.argspec,
                argnlist=argnlist,
                arguments=self.arguments,
            )

            if node_class.has_body:
                self.mstdargsobj.environment_body_parser.....

            return parsed, None
            


    def get_instance_parser(self, main_token, node_class, **kwargs):
        return _InstanceParser(mstdargsobj=self,
                               arguments=self.arguments,
                               main_token=main_token,
                               node_class=node_class,
                               **kwargs)
        


    # def parse_args(self, w, pos, parsing_state=None):
    #     r"""
    #     Parse the arguments encountered at position `pos` in the
    #     :py:class:`~pylatexenc.latexwalker.LatexWalker` instance `w`.

    #     You may override this function to provide custom parsing of complicated
    #     macro arguments (say, ``\verb+...+``).  The method will be called by
    #     keyword arguments, so the argument names should not be altered.

    #     The argument `w` is the :py:class:`pylatexenc.latexwalker.LatexWalker`
    #     object that is currently parsing LaTeX code.  You can call methods like
    #     `w.get_goken()`, `w.get_latex_expression()` etc., to parse and read
    #     arguments.

    #     The argument `parsing_state` is the current parsing state in the
    #     :py:class:`~pylatexenc.latexwalker.LatexWalker` (e.g., are we currently
    #     in math mode?).  See doc for
    #     :py:class:`~pylatexenc.latexwalker.ParsingState`.

    #     This function should return a tuple `(argd, pos, len)` where:

    #     - `argd` is a :py:class:`ParsedMacroArgs` instance, or an instance of a
    #       subclass of :py:class:`ParsedMacroArgs`.  The base `parse_args()`
    #       provided here returns a :py:class:`ParsedMacroArgs` instance.

    #     - `pos` is the position of the first parsed content.  It should be the
    #       same as the `pos` argument, except if there is whitespace at that
    #       position in which case the returned `pos` would have to be the
    #       position where the argument contents start.

    #     - `len` is the length of the parsed expression.  You will probably want
    #       to continue parsing stuff at the index `pos+len` in the string.
    #     """

    #     if parsing_state is None:
    #         parsing_state = w.make_parsing_state()

    #     argnlist = []

    #     if self.args_math_mode is not None and \
    #        len(self.args_math_mode) != len(self.argspec):
    #         raise ValueError("Invalid args_math_mode={!r} for argspec={!r}!"
    #                          .format(self.args_math_mode, self.argspec))

    #     def get_inner_parsing_state(j):
    #         if self.args_math_mode is None:
    #             return parsing_state
    #         amm = self.args_math_mode[j]
    #         if amm is None or amm == parsing_state.in_math_mode:
    #             return parsing_state
    #         if amm == True:
    #             return parsing_state.sub_context(in_math_mode=True)
    #         return parsing_state.sub_context(in_math_mode=False)

    #     p = pos

    #     if self._like_pylatexenc1x_ignore_leading_star:
    #         # ignore any leading '*' character
    #         tok = w.get_token(p)
    #         if tok.tok == 'char' and tok.arg == '*':
    #             p = tok.pos + tok.len

    #     for j, argt in enumerate(self.argspec):
    #         if argt == '{':
    #             (node, np, nl) = w.get_latex_expression(
    #                 p,
    #                 strict_braces=False,
    #                 parsing_state=get_inner_parsing_state(j)
    #             )
    #             p = np + nl
    #             argnlist.append(node)

    #         elif argt == '[':

    #             if self.optional_arg_no_space and p < len(w.s) and w.s[p].isspace():
    #                 # don't try to read optional arg, we don't allow space
    #                 argnlist.append(None)
    #                 continue

    #             optarginfotuple = w.get_latex_maybe_optional_arg(
    #                 p,
    #                 parsing_state=get_inner_parsing_state(j)
    #             )
    #             if optarginfotuple is None:
    #                 argnlist.append(None)
    #                 continue
    #             (node, np, nl) = optarginfotuple
    #             p = np + nl
    #             argnlist.append(node)

    #         elif argt == '*':
    #             # possible star.
    #             tok = w.get_token(p)
    #             if tok.tok == 'char' and tok.arg.startswith('*'):
    #                 # has star
    #                 argnlist.append(
    #                     w.make_node(latexwalker_types.LatexCharsNode,
    #                                 parsing_state=get_inner_parsing_state(j),
    #                                 chars='*', pos=tok.pos, len=1)
    #                 )
    #                 p = tok.pos + 1
    #             else:
    #                 argnlist.append(None)

    #         else:
    #             raise latexwalker_types.LatexWalkerError(
    #                 "Unknown macro argument kind for macro: {!r}".format(argt)
    #             )

    #     parsed = ParsedMacroArgs(
    #         argspec=self.argspec,
    #         argnlist=argnlist,
    #     )

    #     return (parsed, pos, p-pos)





    def __repr__(self):
        return '{}(argspec={!r}, optional_arg_no_space={!r}, args_math_mode={!r})'.format(
            self.__class__.__name__, self.argspec, self.optional_arg_no_space,
            self.args_math_mode
        )
    