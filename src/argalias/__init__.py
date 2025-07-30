from __future__ import annotations
from .__about__ import __version__
from typing import List, Tuple, Optional, Union
import sys
from itertools import chain

class ArgAliasSubstitution:
    canonical: List[str] # canonical name(s) (e.g. ["show"] or ["project", "show"])
    aliases: List[str] # aliases (e.g. ["sh", "s", "get"])
    prefix: List[str] # prefix (e.g. ["admin", "users"])

    def __init__(self, canonical: List[str], 
                 aliases: List[str], 
                 prefix: List[str] | None):
        self.canonical = canonical
        self.aliases = aliases
        self.prefix = prefix

    def check_prefix_el(self, arg: str, tpl: str) -> bool:
        """ return true if arg matches tpl """
        if tpl == '*':
            return True
        for pelem in tpl.split('|'):
            if pelem.strip() == arg:
                return True
        return False
            
    def iterate_args(self, args: List[str], skip_flags=False, nargs: dict = dict()):
        skip_next = 0
        for idx, arg in enumerate(args):
            if skip_next > 0:
                # skip this arg, it's argument to option
                skip_next -= 1
                continue

            if arg in nargs:
                skip_next = nargs[arg]
                continue

            if skip_flags and arg.startswith('-'):
                continue
            yield idx, arg

    def parse(self, args: List[str], skip_flags=False, nargs: dict = dict()) -> List[str]:
        """ return parsed args (with this substitution applied) """
        
        def iter_replace(args: List[str], aliases: List[str], canonical: List[str]):
            """ simple yield from canonical for each alias found in args """
            for arg in args:
                if arg in aliases:
                    yield from canonical
                else:
                    yield arg

        # if prefix not needed, just replace all occurences (if any)
        if self.prefix is None:
            # no prefix, replace all occurences            
            args = list(iter_replace(args, aliases=self.aliases, canonical=self.canonical))
            # args = [ self.canonical if arg in self.aliases else arg for arg in args ]
            return args


        ### main code, (prefix is given)

        args_filtered = list(self.iterate_args(args, skip_flags=skip_flags, nargs=nargs))

        # prefix is given                
        for  arg, prefix_el in zip(args_filtered, self.prefix):
            if not self.check_prefix_el(arg[1], prefix_el):
                return args            

        # prefix is ok, check aliases
        try:
            arg_idx = args_filtered[len(self.prefix)][0]
            arg_name = args_filtered[len(self.prefix)][1]
        except IndexError:
            # nothing to replace: no args after prefix or no args at all
            return args

        if arg_name in self.aliases:
            args[arg_idx:arg_idx+1] = self.canonical

        return args


    def __repr__(self):
        return(f"{self.prefix!r} {self.aliases!r} > {self.canonical!r}")


class ArgAlias:
    substitutions: List[ArgAliasSubstitution]

    def __init__(self):
        self.substitutions = list()
        self._skip_flags = False
        self._nargs = dict()

    def skip_flags(self, skip: bool = True):
        """ 
        flags (any arguments starting with -), will be skipped when checking prefix 
        e.g. alias "sh" with prefix ['project'] will match args: -v --long project sh        
        """
        self._skip_flags = skip

    def nargs(self, name: str, nargs: int = 1):
        """ let argalias know about option which accepts arguments """
        self._nargs[name] = nargs
        
    def alias(self, aliases: List[str], canonical: Union[str, List[str]], prefix: List[str] | str | None = None):

        """
            aliases: list of aliases, e.g. ["sh", "s", "get"]
            canonical: replacement for alias, e.g. "show" or ["project", "show"]
            prefix: alias will match only if prefix matches. 

            Special values for prefix:
            empty list or None (default) - alias will match only if it is fist argument (but see "skip_flags")
            "*" is equal to ['*'] = matches any argument, e.g. alias 'sh' with prefix '*' will match args "project sh" and "user sh"
            "**" is equal to any prefix at all. 
        """


        # sugar for canonical
        if isinstance(canonical, str):
            canonical = list([canonical])
        
        # sugar for prefix
        if prefix is None:
            prefix = list()
        elif prefix == '*':
            prefix = list(['*'])
        elif prefix == '**':
            # any prefix will match, NOTE: different meaning of prefix=None in this function and in ArgAliasSubstitution !
            prefix = None
                
        s = ArgAliasSubstitution(canonical=canonical, aliases=aliases, prefix=prefix)
        self.substitutions.append(s)

    def parse(self, args: Optional[List[str]] = None):
        argv_mode = False
        if args is None:
            argv_mode = True
            args = sys.argv[1:]
            position = 1


        for s in self.substitutions:
            args = s.parse(args, skip_flags=self._skip_flags, nargs=self._nargs)

        if argv_mode:
            sys.argv[1:] = args
        return args

