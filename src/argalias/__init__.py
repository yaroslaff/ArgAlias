from __future__ import annotations
from .__about__ import __version__
from typing import List, Tuple, Optional, Union
import sys



class ArgAliasSubstitution:
    canonical: str # canonical name (e.g. "show")
    aliases: List[str] # aliases (e.g. ["sh", "s", "get"])
    prefix: List[List[str]] # prefixes (e.g. [["person"], ["project"]])

    def __init__(self, canonical: str, 
                 aliases: Tuple[str], 
                 prefix: List[str]):
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
        
        # if prefix not needed, just replace all occurences (if any)
        if self.prefix is None:
            # no prefix, replace all occurences

            args = [ self.canonical if arg in self.aliases else arg for arg in args ]
            return args

        args_filtered = list(self.iterate_args(args, skip_flags=skip_flags, nargs=nargs))

        # prefix is given                
        for  arg, prefix in zip(args_filtered, self.prefix):
            if not self.check_prefix_el(arg[1], prefix):
                return args
            

        # prefix is ok, check aliases
        try:
            arg_idx = args_filtered[len(self.prefix)][0]
            arg_name = args_filtered[len(self.prefix)][1]
        except IndexError:
            # nothing to replace: no args after prefix or no args at all
            return args

        if arg_name in self.aliases:
            args[arg_idx] = self.canonical

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
        self._skip_flags = skip

    def nargs(self, name: str, nargs: int = 1):
        """ let argalias know about option which accepts arguments """
        self._nargs[name] = nargs
        
    def alias(self, name: Union[str, List[str]], *aliases: List[str]):
        if isinstance(name, str):
            canonical = name
            prefix = None
        else:
            # canonical is last element, prefixes are all but last
            canonical = name[-1]    
            prefix = name[:-1]

        s = ArgAliasSubstitution(canonical=canonical, aliases=list(aliases), prefix=prefix)
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

