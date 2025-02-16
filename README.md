# ArgAlias
Aliases for arguments in Python CLI utilities (supports argparse, Typer, Click, and similar tools).

This tool is for those who sometimes prefer to type `p sh X` instead of `project show X`.

You configure which *canonical* CLI arguments you expect, and what aliases are allowed (e.g. for the canonical argument "show" good aliases are "sh" and "get").

If a canonical name is configured with a prefix, aliases will be resolved only if they follow configured prefix from the first argument.

*Simplify your CLI! Add ArgAlias to your argparse, Click, or Typer project in 10 minutes!*

## Installation
~~~
pip3 install argalias
~~~

## How to use
When you add aliases, the first element is either a `str` (the canonical name to which the alias will be resolved to) or a `List[str]` containing prefixes with canonical name.

Each element in the prefix list can be either a simple string (a parameter), `*` (matches any value of parameter) or values separated by the `|` symbol.

~~~python
from argalias import ArgAlias

aa = ArgAlias()

# The script expects "show" parameter anywhere, and it can be aliased as "sh", "s" or even "get"
aa.alias("show", "get", "sh", "s")

# The script expects "employee" as the first parameter, can be aliased as "emp" or "e" 
aa.alias(["employee"], "emp", "e")

# same for "project"
aa.alias(["project"], "proj", "p")

# The script expects "create" parameter after "employee" or "project". Can be aliased as "cr" or "c"
aa.alias(["employee|project", "create"], "cr", "c")

# The script expects "delete" as the second parameter after any parameter, can be aliased as "del" or "d"
aa.alias(["*", "delete"], "del", "d")
aa.parse()
# sys.argv now has all aliases resolved, e.g. "sh" resolved to "show"
print(sys.argv)
~~~

You can find examples using [argparse](examples/argparse), [Click](examples/click), and [Typer](examples/typer) in [examples/](examples/).

Results:
~~~
p sh Something -> project show Something
project cr Mayhem -> project create Mayhem
~~~

These aliases will not be replaced:
~~~
sh emp John ("sh" resolved to "show" but "emp" not resolved: not a first argument)
zzz cr xxx ("cr" not resolved: not after employee or project)
aaa bbb del ("del" not resolved: prefix is "aaa", "bbb" - two elements, not matching "*")
~~~

Might be replaced incorrectly:
~~~
project create sh (You want to create a project named "sh", but "sh" will be replaced with "show" because the alias does not specify any prefix requirements.)
~~~
