from typing import List

from n2t.compiler.symbol_table import SymbolTable, IdentifierKind
from n2t.compiler.compilation_engine import Unit, WrapperType, CompilationEngine
from n2t.compiler.tokenizer import Token, TokenType
from n2t.compiler.vm_line_writer import VMLineWriter, Segment

function_types = {"function", "method", "constructor"}
return_types = {"integer", "void"}  # TODO: add more


class VMWriter:
    _class_name: str
    _symbol_table: SymbolTable
    _vm_line_writer: VMLineWriter
    _top_level_unit: Unit
    _if_increment: int

    def __init__(self, top_level_unit: Unit):
        assert top_level_unit.children[0].content == "class"
        assert top_level_unit.children[1].type == TokenType.IDENTIFIER
        assert top_level_unit.children[2].content == "{"

        self._symbol_table = SymbolTable()
        self._vm_line_writer = VMLineWriter()
        self._class_name = top_level_unit.children[1].content
        self._top_level_unit = top_level_unit
        self._if_increment = 0

    def get_lines_from_unit(self) -> List[str]:
        result = self._handle_unit(self._top_level_unit)
        print('returning answer but...')
        print('_symbol_table', self._symbol_table)
        return self._vm_line_writer.get_lines()

    @staticmethod
    def _identifier_kind_from_keyword(keyword: str) -> IdentifierKind:
        if keyword == "static":
            return IdentifierKind.STATIC
        elif keyword == "field":
            return IdentifierKind.FIELD
        elif keyword == "var":
            return IdentifierKind.VAR
        else:
            raise NotImplementedError("Can't derive kind from keyword:", keyword)

    def _handle_parameters_declaration(self, parameter_list: Unit) -> None:
        assert parameter_list.type == WrapperType.ParameterList
        temp = []
        for i, child in enumerate(parameter_list.children):
            if (i + 2) % 3 == 0:  # append
                var_type, name = temp
                self._symbol_table.define(name, var_type, IdentifierKind.ARG)
                temp = []
            if (i + 1) % 3 == 0:  # ignore, because it's a comma
                assert child.content == ","
            temp.append(child.content)

    def _handle_variable_declaration(self, unit: Unit) -> None:
        # TODO: are all ClassVariableDeclaration STATIC?
        assert len(unit.children) == 4  # static boolean test;
        keyword, var_type, identifier, _ = unit.children
        self._symbol_table.define(
            identifier.content,
            var_type.content,
            VMWriter._identifier_kind_from_keyword(keyword.content))

    def _handle_term(self, unit: Unit) -> None:
        assert unit.type == WrapperType.Term

        if len(unit.children) == 1:
            identifier = unit.children[0]
            assert identifier.type == TokenType.IDENTIFIER
            kind = self._symbol_table.kind_of(identifier.content)
            assert kind == IdentifierKind.VAR  # TODO: is this right? for `local`?
            self._vm_line_writer.write_push(Segment.LOCAL, self._symbol_table.index_of(identifier.content))

        elif unit.children[1].content == ".":
            # it's 100% a function call of some kind
            print('----------CompilationEngine.unit_as_xml(unit)', CompilationEngine.unit_as_xml(unit))
            raise Exception("llool")

    def _handle_expression(self, unit: Unit) -> None:
        assert unit.type == WrapperType.Expression

        for child in unit.children:
            if child.type == WrapperType.Term:
                self._handle_term(child)

    def _handle_expression_list(self, unit: Unit) -> None:
        pass

    def _handle_if_statement(self, unit: Unit) -> None:
        # For now, assume that it goes `expression` `statements` `statements`
        # where expression is `if (expression)`, first statements is if True, second statements is if False
        self._handle_expression(next(c for c in unit.children if c.type == WrapperType.Expression))
        self._vm_line_writer.write_if(f"IF_TRUE{self._if_increment}")
        self._vm_line_writer.write_goto(f"IF_FALSE{self._if_increment}")
        self._vm_line_writer.write_label(f"IF_TRUE{self._if_increment}")
        self._vm_line_writer.write_goto(f"IF_END{self._if_increment}")
        self._vm_line_writer.write_label(f"IF_FALSE{self._if_increment}")
        self._vm_line_writer.write_label(f"IF_END{self._if_increment}")

        self._if_increment += 1

    def _handle_return_statement(self, unit: Unit) -> None:
        # TODO: for now assume we always return 0 (because that's the minimum I guess)
        self._vm_line_writer.write_push(Segment.CONSTANT, 0)
        self._vm_line_writer.write_return()

    def _handle_do_statement(self, unit: Unit) -> None:
        # do statements are either like:
        # 1. `do Game.run();` -- class method
        # 2. `do game.run();` -- object/instance method (another class)
        # 3. `do draw();` -- local object/instance method?
        if unit.children[2].content == ".":  # it's either 1 or 2
            # TODO: handle 1
            # for now assume 2
            # find variable, prep arguments (on 2, 1st is always `game` ref), then run
            identifier = unit.children[1].content
            kind = self._symbol_table.kind_of(identifier)
            assert kind == IdentifierKind.VAR, "Was either not VAR or didn't exist at all because Not Implemented"
            self._vm_line_writer.write_push(Segment.LOCAL, self._symbol_table.index_of(identifier))
            expression_list = next(item for item in unit.children if item.type == WrapperType.ExpressionList)
            self._handle_expression_list(expression_list)

            # since we're calling a different object function, the type will be part of the name
            fn_name = f"{self._symbol_table.type_of(identifier)}.{unit.children[3].content}"
            self._vm_line_writer.write_call(fn_name, 1)  # TODO: assumes 1 arg

            # TODO: assume it ain't storing the result
            self._vm_line_writer.write_pop(Segment.TEMP, 0)
        else:
            raise NotImplementedError

    def _handle_let_statement(self, unit: Unit) -> None:
        assert unit.type == WrapperType.LetStatement

        # let statement has before and after `=`
        # after `=` is always an expression then `;`
        # for now assume that = is after keyword and identifier
        assert unit.children[2].content == "="
        assert unit.children[3].type == WrapperType.Expression
        assert unit.children[4].type == TokenType.SYMBOL

        self._handle_expression(unit.children[3])

        # the first half creates a pop to the location of the identifier
        # TODO: simplify this pattern?
        kind = self._symbol_table.kind_of(unit.children[1].content)
        assert kind == IdentifierKind.VAR  # TODO: is this right? for `local`?
        self._vm_line_writer.write_pop(Segment.LOCAL, self._symbol_table.index_of(unit.children[1].content))

    def _handle_statements(self, unit: Unit) -> None:
        for child in unit.children:
            if child.type == WrapperType.LetStatement:
                self._handle_let_statement(child)
            elif child.type == WrapperType.DoStatement:
                self._handle_do_statement(child)
            elif child.type == WrapperType.ReturnStatement:
                self._handle_return_statement(child)
            elif child.type == WrapperType.IfStatement:
                self._handle_if_statement(child)

    def _handle_subroutine_body(self, unit: Unit) -> None:
        pass

    def _handle_blahblahblah(self, unit: Unit) -> None:
        pass

    def _handle_parameter_list(self, unit: Unit) -> None:
        pass

    def _handle_unit_children(self, children: List[Unit]) -> None:
        pass

    def _handle_subroutine_declaration(self, unit: Unit) -> None:
        self._symbol_table.start_subroutine()
        assert isinstance(unit.children[0], Token) and unit.children[0].content in function_types
        assert isinstance(unit.children[2], Token) and unit.children[2].type == TokenType.IDENTIFIER
        name = f"{self._class_name}.{unit.children[2].content}"

        body = next(c for c in unit.children if c.type == WrapperType.SubroutineBody)
        assert body, f"Subroutine `{name}` has no body!"

        # process parameter list, which only modifies symbol table
        parameter_list = next(c for c in unit.children if c.type == WrapperType.ParameterList)
        self._handle_parameter_list(parameter_list)

        # process variable declarations, this only modifies symbol table
        var_dec_count = 0
        for thing in body.children:
            if isinstance(thing, Unit) and thing.type == WrapperType.VariableDeclaration:
                var_dec_count += 1
                self._handle_variable_declaration(thing)

        # make declaration for function
        var_decs = [c for c in body.children if c.type == WrapperType.VariableDeclaration]
        num_var_decs = len(var_decs)
        self._vm_line_writer.write_fn(name, num_var_decs)

        # then handle statements
        statements = next(c for c in body.children if c.type == WrapperType.Statements)
        self._handle_statements(statements)

    def _handle_unit(self, unit: Unit) -> None:
        for child in unit.children:
            if isinstance(child, Unit):
                if child.type == WrapperType.ClassVariableDeclaration:
                    self._handle_variable_declaration(child)
                elif child.type == WrapperType.SubroutineDeclaration:
                    self._handle_subroutine_declaration(child)
                elif child.type == WrapperType.Statements:
                    self._handle_statements(child)

            elif isinstance(child, Token):
                pass
