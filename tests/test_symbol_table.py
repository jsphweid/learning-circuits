import pytest

from n2t.compiler.symbol_table import IdentifierKind, SymbolTable

class_scope_kinds = [IdentifierKind.STATIC, IdentifierKind.FIELD]
fn_scope_kinds = [IdentifierKind.VAR, IdentifierKind.ARG]
all_kinds = class_scope_kinds + fn_scope_kinds


@pytest.mark.parametrize("kind", all_kinds)
def test_symbol_table_initializes_correctly(kind):
    symbol_table = SymbolTable()
    assert symbol_table.var_count(kind) == 0


@pytest.mark.parametrize("kind", class_scope_kinds)
def test_symbol_table_works_with_class_scope(kind):
    symbol_table = SymbolTable()
    symbol_table.define("some_name", "some_type", kind)
    assert symbol_table.var_count(kind) == 1

    symbol_table.start_subroutine()

    # no other kind is in the table
    other_kinds = [k for k in all_kinds if k != kind]
    for k in other_kinds:
        assert symbol_table.var_count(k) == 0

    # `start_subroutine` doesn't wipe it out
    assert symbol_table.var_count(kind) == 1
    assert symbol_table.index_of("some_name") == 0
    assert symbol_table.type_of("some_name") == "some_type"
    assert symbol_table.kind_of("some_name") == kind


@pytest.mark.parametrize("kind", fn_scope_kinds)
def test_symbol_table_works_with_fn_scope(kind):
    symbol_table = SymbolTable()
    symbol_table.define("some_name", "some_type", kind)
    assert symbol_table.var_count(kind) == 1

    # no other kind is in the table
    other_kinds = [k for k in all_kinds if k != kind]
    for k in other_kinds:
        assert symbol_table.var_count(k) == 0

    symbol_table.start_subroutine()

    # `start_subroutine` wipes out everything
    assert symbol_table.var_count(kind) == 0
