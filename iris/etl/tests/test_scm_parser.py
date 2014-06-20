#pylint: skip-file
from iris.etl.parser import parse_blocks, parse_user


def test_empty_string():
    assert [] == parse_blocks('', None)


def test_ignore_empty_lines():
    content = '''

    D: Security

    M: Mark

    '''
    assert parse_blocks(content, 'D') == [
        {'D': 'Security', 'M': ['Mark']}
        ]


def test_multi_attrs():
    content = '''
    D: System
    M: Markus
    M: Mickey
    '''
    assert parse_blocks(content, 'D') == [
        {'D': 'System', 'M': ['Markus', 'Mickey']}
        ]


def test_syntax_error():
    content = '''
    M: Manson
    D: App Framework
    '''
    try:
        parse_blocks(content, 'D')
    except ValueError:
        pass
    else:
        assert False, "It must raise exception for syntax error"


def test_mapping():
    content = '''
    D: Native API
    '''
    assert parse_blocks(content, 'D', {'D': 'Domain'}) == [
        {'Domain': 'Native API'}
        ]


def test_mapping_not_found():
    content = '''
    D: Native API
    '''
    assert parse_blocks(content, 'D', {'M': 'Maintainer'}) == [
        {'D': 'Native API'}
        ]


def test_multi_blocks():
    content = '''
    D: App Framework
    M: Maggie
    D: System
    R: Ray
    D: Security
    '''
    assert parse_blocks(content, 'D') == [
        {'D': 'App Framework', 'M': ['Maggie']},
        {'D': 'System', 'R': ['Ray']},
        {'D': 'Security'}
        ]


def test_full_user():
    assert parse_user('John 5 <john5@music.com>') == (
        'john5@music.com', 'John', '5')


def test_only_email():
    assert parse_user('john5@music.com') == (
        'john5@music.com', '', '')


def test_only_email2():
    assert parse_user(' <john5@music.com>') == (
        'john5@music.com', '', '')


def test_no_email():
    assert parse_user('John 5') == (
        '', 'John', '5')


def test_only_first():
    assert parse_user('John') == (
        '', 'John', '')


def test_first_middle_last():
    assert parse_user('John William Lowery') == (
        '', 'John', 'William Lowery')


def test_first_middle_last_email():
    assert parse_user('John William Lowery <john5@music.com>') == (
        'john5@music.com', 'John', 'William Lowery')


def test_invalid_email():
    assert parse_user('John 5 <john5.>') == (
        '', 'John', '5')