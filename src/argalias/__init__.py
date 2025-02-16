from __future__ import annotations
from .__about__ import __version__
from typing import List, Tuple, Optional, Union
import sys

MAX_STAGE = 2

class ArgAliasSubstitution:
    stage: int #  processed first
    canonical: str # canonical name (e.g. "show")
    aliases: List[str] # aliases (e.g. ["sh", "s", "get"])
    prefix: List[List[str]] # prefixes (e.g. [["person"], ["project"]])

    def __init__(self, canonical: str, 
                 aliases: Tuple[str], 
                 prefix: List[str]):
        self.canonical = canonical
        self.aliases = aliases
        self.prefix = prefix
        self.stage = self.calculate_stage()


    def calculate_stage(self):            
        # No prefix - latest stage
        if self.prefix is None:
            return 2

        if '*' in self.prefix:
            return 1

        return 0

    def check_prefix_el(self, tpl: str, arg: str):
        if tpl == '*':
            return True
        for pelem in tpl.split('|'):
            if pelem.strip() == arg:
                return True
        return False

    def match(self, args: List[str]):
        """ check if args matches this substitution """
        if self.prefix is None:
            return any(al in args for al in self.aliases)

        # prefix is given (maybe empty list)
        for p, arg in zip(self.prefix, args):
            if not self.check_prefix_el(p, arg):
                return False
        
        # is alias found after prefix in args?
        # print("retany", self.canonical, self.aliases, args)
        # print("prefix:", self.prefix)
        
        if len(self.prefix) >= len(args):
            return False

        return any(al in args[len(self.prefix)] for al in self.aliases)
            

    def parse(self, args: List[str]) -> List[str]:
        """ return parsed args (with this substitution applied) """
        if not self.match(args):
            return args

        # match! now we will replace
        if self.prefix is None:
            # no prefix, replace all occurences

            def replace_arg(arg):
                return self.canonical if arg in self.aliases else arg

            args = [ replace_arg(arg) for arg in args ]
            return args

        # prefix is given
        args[len(self.prefix)] = self.canonical

        return args


    def __repr__(self):
        return(f"{self.prefix!r} {self.canonical} {self.aliases!r}")


class ArgAlias:
    substitutions: List[ArgAliasSubstitution]

    def __init__(self):
        self.substitutions = list()

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

        for stage in range(MAX_STAGE + 1):
            for s in self.substitutions:
                if s.stage == stage:
                    args = s.parse(args)

        if argv_mode:
            sys.argv[1:] = args
        return args



#aa = ArgAlias()
#aa.alias("show", "get", "sh", "s")
#aa.alias(["person", "create"],"cr", "c")
#aa.alias(["project", "create"],"cr", "c")
# nars = aa.parse(["person", "sh"])
