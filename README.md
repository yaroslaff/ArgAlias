# ArgAlias

[![Run tests and upload coverage](https://github.com/yaroslaff/ArgAlias/actions/workflows/main.yml/badge.svg)](https://github.com/yaroslaff/ArgAlias/actions/workflows/main.yml) [![codecov](https://codecov.io/gh/yaroslaff/ArgAlias/graph/badge.svg?token=3DUNW2SH81)](https://codecov.io/gh/yaroslaff/ArgAlias)

Aliases for arguments in Python CLI utilities (supports argparse, Typer, Click, and similar tools).

This tool is for those who agree that `p sh X` is shorter then `project show X`.

You configure which *canonical* CLI arguments you expect, and what aliases are allowed (e.g. for the canonical argument "show" good aliases are "sh" and "get").

If a canonical name is configured with a prefix, aliases will be resolved only if they follow configured prefix from the first argument.

*Add aliases to your argparse, Click, or Typer project in 10 minutes!*

## Installation
~~~
pip3 install argalias
~~~

## How to use
When you add aliases, the first element is either a `str` (the canonical name to which the alias will be resolved to) or a `List[str]` containing prefixes with canonical name.

Each element in the prefix list can be either a simple string (a parameter), `*` (matches any value of parameter) or values separated by the `|` symbol.

`alias` is main method, it expects 3 arguments: list of aliases, canonical namd and prefix (default: None, which means alias will be applied to first argument)

~~~python
from argalias import ArgAlias

aa = ArgAlias()

# The script expects "employee" as the first parameter, can be aliased as "emp" or "e" 
aa.alias(["emp", "e"], "employee")

# same for "project"
aa.alias(["proj", "p"], "project")

# or even simpler (if only one alias)
aa.alias("p", "project")

# The script expects "show" parameter anywhere, and it can be aliased as "sh", "s" or even "get"
# Be careful with '**' because: script.py sh character sh holmes 
# will be (possible wrongly) translated to: script.py show character show holmes 
aa.alias(['sh', 's', 'get'], "show", prefix="**")


# The script expects "create" parameter after "employee" or "project". Can be aliased as "cr" or "c"
# Note: this rule should go AFTER p=project and e=employee rules, otherwise real prefix "p" will not match required prefix "project"
aa.alias(["cr", "c"], "create", prefix=["employee|project"])

# The script expects "delete" as the second parameter after any parameter, can be aliased as "del" or "d"
# pr del X, employee d X and even anything d X will work.
aa.alias(["del", "d"], "delete", prefix="*")
aa.parse()
# sys.argv now has all aliases resolved, e.g. "sh" resolved to "show"
print(sys.argv)

# now all aliases in sys.argv are resolved and you can do your argparse or click or typer parsing
~~~

You can find examples using [argparse](examples/argparse), [Click](examples/click), and [Typer](examples/typer) in [examples/](examples/).

Results:
~~~
p sh Something -> project show Something
project cr Mayhem -> project create Mayhem
~~~

These aliases will not be replaced:
~~~
sh emp John ("sh" resolved to "show" but "emp" will not be resolved: not a first argument)
zzz cr xxx ("cr" will not be resolved: not after employee or project)
aaa bbb del ("del" will not be resolved: prefix is "aaa", "bbb" - two elements, but "*" matches only one element)
~~~

Might be replaced incorrectly:
~~~
project create sh (You want to create a project named "sh", but "sh" will be replaced with "show" because the alias does not specify any prefix requirements.)
~~~

## Optional arguments
Optional arguments can make a problems while checking prefixes, e.g. `script.py -v p del X` will not match `["project"]` prefix, because first argument is "-v", not "p". Here `skip_flags()` and `nargs()` comes to help.  

~~~python
# with skip_flags ArgAlias will ignore any unknown arguments starting with "-", e.g. "-v", or  "--some-option"
aa.skip_flags()

# this will ignore --xy 11 22 
aa.nargs('--xy', nargs=2)

# this will ginore --level 123 (default value for nargs is 1)
aa.nargs('--level')
~~~

## Replacing alias to many words
You can replace alias into many words, just assign `canonical` a list.

~~~python
aa.alias(["ml", "mls"], ["metrics", "list"])
~~~

now `script.py ml` will be replaced to `script.py metrics list`


See [argparse_ex1.py](examples/argparse/argparse_ex1.py) for a real example. You do not need to use `skip_flags` or `nargs`:
1. If you replace parameter anywhere in args (like "show" in example above), not using prefix.
2. If options will go after alias (e.g. `script.py project del X --verbose`)
3. If you do not use options at all (e.g. no `-v` or `--verbose` or `--level DEBUG`)
