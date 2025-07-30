from argalias import ArgAlias, ArgAliasSubstitution, __version__
import sys

def test_repr():
    aas = ArgAliasSubstitution(['show'], ['s', 'sh'], None)
    aas_repr = repr(aas)
    assert aas_repr == "None ['s', 'sh'] > ['show']"

def test_argv():
    argv_backup = sys.argv
    sys.argv = ['script.py', 'sh', 'something']    
    aa = ArgAlias()
    aa.alias(['sh'], 'show')
    parsed = aa.parse()
    assert sys.argv == ['script.py', 'show', 'something']
    sys.argv = argv_backup

def test_anywhere():
    aa = ArgAlias()
    aa.skip_flags()
    aa.alias(['sh', 's', 'get'], 'show', prefix='**')

    parsed  = aa.parse(['show', 'hello', 'world'])
    assert parsed == ['show','hello', 'world']

    parsed  = aa.parse(['sh', 'hello', 'world'])
    assert parsed == ['show','hello', 'world']

    parsed  = aa.parse(['-v', 'sh', 'hello', 'world'])
    assert parsed == ['-v', 'show','hello', 'world']

    parsed  = aa.parse(['sh', '-v', 'hello', 'world'])
    assert parsed == ['show', '-v', 'hello', 'world']

    parsed  = aa.parse(['sh', 'hello', 's'])
    assert parsed == ['show','hello', 'show']

def test_alias_str():
    aa = ArgAlias()
    aa.skip_flags()
    aa.alias('sh', 'show')

    parsed  = aa.parse(['sh', 'hello', 'world'])
    assert parsed == ['show','hello', 'world']


def test_prefix0():
    aa = ArgAlias()
    aa.skip_flags()
    aa.alias(['sh', 's', 'get'], ["show"])

    parsed  = aa.parse(['show', 'hello', 'world'])
    assert parsed == ['show','hello', 'world']

    parsed  = aa.parse(['sh', 'hello', 'world'])
    assert parsed == ['show','hello', 'world']

    parsed  = aa.parse(['sh', '-v', 'hello', 'world'])
    assert parsed == ['show', '-v','hello', 'world']

    parsed  = aa.parse(['-v', 'sh', 'hello', 'world'])
    assert parsed == ['-v', 'show', 'hello', 'world']

    parsed  = aa.parse(['sh', 'hello', 's'])
    assert parsed == ['show','hello', 's']

    parsed  = aa.parse([])
    assert parsed == []


def test_nargs():
    aa = ArgAlias()
    aa.skip_flags()
    aa.nargs('--level')
    aa.nargs('--xy', nargs=2)
    aa.alias(['sh', 's', 'get'], ['show'])
    parsed  = aa.parse(['sh', '--level', '123', 'hello', 'world'])
    assert parsed == ['show', '--level', '123', 'hello', 'world']

    parsed  = aa.parse(['sh', '--xy', '11', '22', 'hello', 'world'])
    assert parsed == ['show', '--xy', '11', '22', 'hello', 'world']

    parsed  = aa.parse(['sh', '--level', '123', '--xy', '11', '22', 'hello', 'world'])
    assert parsed == ['show', '--level', '123', '--xy', '11', '22', 'hello', 'world']


def test_prefix1():
    aa = ArgAlias()
    aa.alias(['sh', 's', 'get'], ['show'], prefix=['section'])

    parsed  = aa.parse(['show', 'hello', 'world'])
    assert parsed == ['show','hello', 'world']

    parsed  = aa.parse(['section', 'sh', 'hello', 'world'])
    assert parsed == ['section', 'show','hello', 'world']

    parsed  = aa.parse(['section', 'sh', 'hello', 's'])
    assert parsed == ['section', 'show','hello', 's']


def test_prefix2():
    aa = ArgAlias()
    aa.alias(['sh', 's', 'get'], 'show', prefix=['section', 'subsection'])

    # must not be applied
    parsed  = aa.parse(['show', 'hello', 'world'])
    assert parsed == ['show','hello', 'world']

    # must be applied
    parsed  = aa.parse(['section', 'subsection', 'sh', 'hello', 'world'])
    assert parsed == ['section', 'subsection', 'show','hello', 'world']

    # must be applied once
    parsed  = aa.parse(['section', 'subsection', 'sh', 'hello', 'sh'])
    assert parsed == ['section', 'subsection', 'show','hello', 'sh']

def test_prefix_asterisk():
    aa = ArgAlias()
    aa.alias(['sh', 's', 'get'], ['show'], prefix='*')

    # must not be applied
    parsed  = aa.parse(['show', 'hello', 'world'])
    assert parsed == ['show','hello', 'world']

    # must be applied
    parsed  = aa.parse(['p1', 'sh', 'hello', 'world'])
    assert parsed == ['p1', 'show','hello', 'world']

    # must be applied once
    parsed  = aa.parse(['p1', 'sh', 'hello', 'sh'])
    assert parsed == ['p1', 'show','hello', 'sh']

def test_prefix_pipe():
    aa = ArgAlias()
    aa.alias(['sh', 's', 'get'], ['show'], prefix=['aaa | bbb'])

    # must not be applied
    parsed  = aa.parse(['show', 'hello', 'world'])
    assert parsed == ['show','hello', 'world']

    # must not be applied
    parsed  = aa.parse(['xxx', 'show', 'hello', 'world'])
    assert parsed == ['xxx', 'show','hello', 'world']

    # must be applied
    parsed  = aa.parse(['aaa', 'sh', 'hello', 'world'])
    assert parsed == ['aaa', 'show','hello', 'world']

    # must be applied
    parsed  = aa.parse(['bbb', 'sh', 'hello', 'world'])
    assert parsed == ['bbb', 'show','hello', 'world']

    # must be applied once
    parsed  = aa.parse(['aaa', 'sh', 'hello', 'sh'])
    assert parsed == ['aaa', 'show','hello', 'sh']


def test_useless():
    # not really useful tests
    # just to get higher coverate rate
    assert len(__version__)
    aa = ArgAlias()
    parsed = aa.parse([])
    assert parsed == []
