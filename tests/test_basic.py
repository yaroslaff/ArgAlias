from argalias import ArgAlias, ArgAliasSubstitution
import sys

def test_repr():
    aas = ArgAliasSubstitution('show', ('s', 'sh'), None)
    aas_repr = repr(aas)
    assert aas_repr == "None show ('s', 'sh')"

def test_argv():
    sys.argv = ['script.py', 'sh', 'something']    
    aa = ArgAlias()
    aa.alias('show', 'sh',)
    parsed = aa.parse()
    assert sys.argv == ['script.py', 'show', 'something']

def test_anywhere():
    aa = ArgAlias()
    aa.alias('show', 'sh', 's', 'get')

    parsed  = aa.parse(['show', 'hello', 'world'])
    assert parsed == ['show','hello', 'world']

    parsed  = aa.parse(['sh', 'hello', 'world'])
    assert parsed == ['show','hello', 'world']

    parsed  = aa.parse(['sh', 'hello', 's'])
    assert parsed == ['show','hello', 'show']

def test_prefix0():
    aa = ArgAlias()
    aa.alias(['show'], 'sh', 's', 'get')

    parsed  = aa.parse(['show', 'hello', 'world'])
    assert parsed == ['show','hello', 'world']

    parsed  = aa.parse(['sh', 'hello', 'world'])
    assert parsed == ['show','hello', 'world']

    parsed  = aa.parse(['sh', 'hello', 's'])
    assert parsed == ['show','hello', 's']

def test_prefix1():
    aa = ArgAlias()
    aa.alias(['p1', 'show'], 'sh', 's', 'get')

    parsed  = aa.parse(['show', 'hello', 'world'])
    assert parsed == ['show','hello', 'world']

    parsed  = aa.parse(['p1', 'sh', 'hello', 'world'])
    assert parsed == ['p1', 'show','hello', 'world']

    parsed  = aa.parse(['p1', 'sh', 'hello', 's'])
    assert parsed == ['p1', 'show','hello', 's']


def test_prefix2():
    aa = ArgAlias()
    aa.alias(['p1', 'p2', 'show'], 'sh', 's', 'get')

    # must not be applied
    parsed  = aa.parse(['show', 'hello', 'world'])
    assert parsed == ['show','hello', 'world']

    # must be applied
    parsed  = aa.parse(['p1', 'p2', 'sh', 'hello', 'world'])
    assert parsed == ['p1', 'p2', 'show','hello', 'world']

    # must be applied once
    parsed  = aa.parse(['p1', 'p2', 'sh', 'hello', 'sh'])
    assert parsed == ['p1', 'p2', 'show','hello', 'sh']

def test_prefix_asterisk():
    aa = ArgAlias()
    aa.alias(['*', 'show'], 'sh', 's', 'get')

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
    aa.alias(['aaa | bbb', 'show'], 'sh', 's', 'get')

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
