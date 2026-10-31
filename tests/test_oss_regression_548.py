import ast

import pytest

from pyflakes import checker, messages


@pytest.mark.parametrize(('source', 'builtins', 'expected'), (
    ("int = 42\ndel int\nx = int('42')\nprint(x)\n", (), ()),
    ("int = 42\ndel int\ndef parse():\n    return int('42')\n", (), ()),
    ("_ = lambda x: x\nlabel = _('Label')\ndel _\n_('Other')\n",
     ('_',), ()),
    ("_ = lambda x: x\ndel _\ndef translate():\n    return _('Other')\n",
     ('_',), ()),
    ("int = 42\ndel int\nclass C:\n    value = int('42')\n", (), ()),
    ("del int\nint('42')\n", (), (messages.UndefinedName,)),
    ("del __file__\nprint(__file__)\n", (), (messages.UndefinedName,)),
    ("value = 42\ndel value\nprint(value)\n",
     (), (messages.UndefinedName,)),
    ("int = 42\ndel int\ndel int\n", (), (messages.UndefinedName,)),
    ("print = None\ndel print\nprint >> 1\n",
     (), (messages.InvalidPrintSyntax,)),
))
def test_deleted_module_binding_reveals_builtin(source, builtins, expected):
    diagnostics = checker.Checker(ast.parse(source), builtins=builtins).messages
    assert tuple(type(message) for message in diagnostics) == expected, [
        str(message) for message in diagnostics
    ]
