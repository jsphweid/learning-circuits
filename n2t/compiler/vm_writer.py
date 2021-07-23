from typing import List, Union

from n2t.compiler.symbol_table import SymbolTable, IdentifierKind
from n2t.compiler.compilation_engine import Unit, WrapperType, CompilationEngine
from n2t.compiler.tokenizer import Token, TokenType, JackTokenizer
from n2t.compiler.vm_line_writer import VMLineWriter, Segment, Command

function_types = {"function", "method", "constructor"}
return_types = {"integer", "void"}  # TODO: add more


class VMWriter:
    _class_name: str
    _symbol_table: SymbolTable
    _vm_line_writer: VMLineWriter
    _top_level_unit: Unit
    _if_increment: int
    _while_increment: int

    def __init__(self, top_level_unit: Unit):
        assert top_level_unit.children[0].content == "class"
        assert top_level_unit.children[1].type == TokenType.IDENTIFIER
        assert top_level_unit.children[2].content == "{"

        self._symbol_table = SymbolTable()
        self._vm_line_writer = VMLineWriter()
        self._class_name = top_level_unit.children[1].content
        self._top_level_unit = top_level_unit
        self._if_increment = 0
        self._while_increment = 0

    def get_lines_from_unit(self) -> List[str]:
        self._handle_unit(self._top_level_unit)
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

    @staticmethod
    def _kind_to_segment_type(kind: IdentifierKind) -> Segment:
        if kind == IdentifierKind.ARG:
            return Segment.ARGUMENT
        elif kind == IdentifierKind.FIELD:
            return Segment.THIS
        elif kind == IdentifierKind.STATIC:
            return Segment.STATIC
        elif kind == IdentifierKind.VAR:
            return Segment.LOCAL

    def _content_to_command(self, content: str) -> Command:
        if content == "=":
            return Command.EQ
        elif content == "+":
            return Command.ADD
        elif content == "-":
            return Command.SUB
        elif content == "~":
            return Command.NEG
        elif content == ">":
            return Command.GT
        elif content == "<":
            return Command.LT
        elif content == "&":
            return Command.AND
        elif content == "|":
            return Command.OR
        elif content == "!":
            return Command.NOT
        else:
            raise NotImplementedError

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

    def _handle_variable_declaration(self, unit: Unit) -> int:
        keyword = unit.children[0]
        var_type = unit.children[1]
        num_variables_declared = 0

        for identifier in [token for token in unit.children[2:] if token.type == TokenType.IDENTIFIER]:
            num_variables_declared += 1
            self._symbol_table.define(
                identifier.content,
                var_type.content,
                VMWriter._identifier_kind_from_keyword(keyword.content))

        return num_variables_declared

    def _handle_string_const(self, token: Token) -> None:
        assert token.type == TokenType.STRING_CONST
        self._vm_line_writer.write_push(Segment.CONSTANT, len(token.content))
        self._vm_line_writer.write_call("String.new", 1)
        for char in token.content:
            self._vm_line_writer.write_push(Segment.CONSTANT, ord(char))
            self._vm_line_writer.write_call("String.appendChar", 2)

    def _handle_term(self, unit: Unit) -> None:
        assert unit.type == WrapperType.Term

        if len(unit.children) == 1:
            child = unit.children[0]
            if child.type == TokenType.IDENTIFIER:
                segment_type = self._kind_to_segment_type(self._symbol_table.kind_of(child.content))
                self._vm_line_writer.write_push(segment_type, self._symbol_table.index_of(child.content))
            elif child.type == TokenType.INT_CONST:
                self._vm_line_writer.write_push(Segment.CONSTANT, int(child.content))
            elif child.type == TokenType.KEYWORD:
                if child.content == "this":
                    self._vm_line_writer.write_push(Segment.POINTER, 0)
                elif child.content == "true":
                    # TODO: why do we push 0 then do not instead of pushing 1...?
                    self._vm_line_writer.write_push(Segment.CONSTANT, 0)
                    self._vm_line_writer.write_arithmetic(Command.NOT)
                elif child.content in "false":
                    self._vm_line_writer.write_push(Segment.CONSTANT, 0)
                else:
                    raise NotImplementedError
            elif child.type == TokenType.STRING_CONST:
                self._handle_string_const(child)
            else:
                raise NotImplementedError
        elif isinstance(unit.children[1], Token) and unit.children[1].content == ".":
            # it's 100% a function call of some kind
            self._handle_call_fn(unit.children)
        elif len(unit.children) == 2 and \
                isinstance(unit.children[0], Token) and unit.children[0].content in {"~", "-"} and \
                unit.children[1].type == WrapperType.Term:
            self._handle_term(unit.children[1])
            self._vm_line_writer.write_arithmetic(Command.NOT if unit.children[0].content == "~" else Command.NEG)
        elif isinstance(unit.children[0], Token) and unit.children[0].content == "(":
            # it's just an inner expression...
            self._handle_expression(unit.children[1])
        else:
            raise NotImplementedError

    def _handle_expression(self, unit: Unit) -> None:
        assert unit.type == WrapperType.Expression

        # if expression follows these forms, recurse
        if len(unit.children) == 3 and \
                unit.children[0].type == WrapperType.Term and \
                unit.children[1].type == TokenType.SYMBOL and \
                unit.children[1].content in JackTokenizer.all_op_symbols and \
                unit.children[2].type == WrapperType.Term:
            self._handle_term(unit.children[0])
            self._handle_term(unit.children[2])
            if unit.children[1].content in JackTokenizer.extended_op_symbols:
                method_name = "multiply" if unit.children[1].content == "*" else "divide"
                self._vm_line_writer.write_call(f"Math.{method_name}", 2)
            else:
                self._vm_line_writer.write_arithmetic(self._content_to_command(unit.children[1].content))
            return
        elif len(unit.children) == 2 and \
                unit.children[0].content == "-" and unit.children[0].content in JackTokenizer.op_symbols and \
                unit.children[1].type == WrapperType.Term:
            self._handle_term(unit.children[1])
            self._vm_line_writer.write_arithmetic(Command.NEG)
            return

        for child in unit.children:
            if child.type == WrapperType.Term:
                self._handle_term(child)

    def _handle_expression_list(self, unit: Unit) -> int:
        expression_count = 0
        for child in unit.children:
            if child.type == WrapperType.Expression:
                self._handle_expression(child)
                expression_count += 1
        return expression_count

    def _handle_if_statement(self, unit: Unit) -> None:
        inc = self._if_increment
        self._if_increment += 1

        # it goes `expression` `statements` if NO else
        # it goes `expression` `statements` `statements` if there IS an else
        # where expression is `if (expression)`, first statements is if True, second statements is if False
        self._handle_expression(next(c for c in unit.children if c.type == WrapperType.Expression))
        statements_blocks = [c for c in unit.children if c.type == WrapperType.Statements]
        assert len(statements_blocks) <= 2
        has_else = len(statements_blocks) == 2

        self._vm_line_writer.write_if(f"IF_TRUE{inc}")
        self._vm_line_writer.write_goto(f"IF_FALSE{inc}")
        self._vm_line_writer.write_label(f"IF_TRUE{inc}")

        # there is always at least one `statements`
        self._handle_statements(statements_blocks[0])

        if has_else:
            self._vm_line_writer.write_goto(f"IF_END{inc}")

        self._vm_line_writer.write_label(f"IF_FALSE{inc}")

        if has_else:
            self._handle_statements(statements_blocks[1])
            self._vm_line_writer.write_label(f"IF_END{inc}")

    def _handle_while_statement(self, unit: Unit) -> None:
        inc = self._while_increment
        self._while_increment += 1
        # while statements always have an `expression` followed by `statements`
        self._vm_line_writer.write_label(f"WHILE_EXP{inc}")
        self._handle_expression(next(c for c in unit.children if c.type == WrapperType.Expression))
        self._vm_line_writer.write_arithmetic(Command.NOT)
        self._vm_line_writer.write_if(f"WHILE_END{inc}")
        self._handle_statements(next(c for c in unit.children if c.type == WrapperType.Statements))
        self._vm_line_writer.write_goto(f"WHILE_EXP{inc}")
        self._vm_line_writer.write_label(f"WHILE_END{inc}")

    def _handle_return_statement(self, unit: Unit) -> None:
        # TODO: for now assume we always return 0 (because that's the minimum I guess)
        expressions = [c for c in unit.children if c.type == WrapperType.Expression]
        if len(expressions) == 0:
            self._vm_line_writer.write_push(Segment.CONSTANT, 0)
        elif len(expressions) == 1:
            self._handle_expression(expressions[0])
        else:
            raise NotImplementedError
        self._vm_line_writer.write_return()

    def _handle_call_fn(self, children: List[Union[Unit, Token]]):
        # fn calls are like one of these:
        # 1. `Game.run();` -- static method
        # 2. `game.run();` -- object/instance method (another class)
        # 3. `draw();` -- local object/instance method?

        # if it's not `.`, we need hidden arg BUT it's not going to exist in symbol table

        arg_count = 0

        # TODO: refactor this so it reads nicer
        if children[1].content == ".":  # it's either 1 or 2
            identifier = children[0].content

            # if it exists in the symbol table, then it needs to be pushed as a hidden first arg
            if self._symbol_table.exists(identifier):
                arg_count += 1
                segment_type = self._kind_to_segment_type(self._symbol_table.kind_of(identifier))
                self._vm_line_writer.write_push(segment_type, self._symbol_table.index_of(identifier))

            # since we're calling a different object function, the type will be part of the name
            p = self._symbol_table.type_of(identifier) if self._symbol_table.exists(identifier) else identifier
            fn_name = f"{p}.{children[2].content}"
        else:  # it's like 3
            arg_count += 1
            self._vm_line_writer.write_push(Segment.POINTER, 0)
            fn_name = f"{self._class_name}.{children[0].content}"

        expression_list = next(item for item in children if item.type == WrapperType.ExpressionList)
        expression_count = self._handle_expression_list(expression_list)

        self._vm_line_writer.write_call(fn_name, arg_count + expression_count)

    def _handle_do_statement(self, unit: Unit) -> None:
        self._handle_call_fn(unit.children[1:])
        self._vm_line_writer.write_pop(Segment.TEMP, 0)

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
        segment_type = self._kind_to_segment_type(kind)
        self._vm_line_writer.write_pop(segment_type, self._symbol_table.index_of(unit.children[1].content))

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
            elif child.type == WrapperType.WhileStatement:
                self._handle_while_statement(child)

    def _handle_subroutine_body(self, unit: Unit) -> None:
        pass

    def _handle_blahblahblah(self, unit: Unit) -> None:
        pass

    def _handle_parameter_list(self, unit: Unit) -> None:
        for i, child in enumerate(unit.children):
            if child.type == TokenType.IDENTIFIER:
                self._symbol_table.define(child.content, unit.children[i - 1].content, IdentifierKind.ARG)

    def _handle_unit_children(self, children: List[Unit]) -> None:
        pass

    def _handle_subroutine_declaration(self, unit: Unit) -> None:
        self._if_increment = 0
        self._while_increment = 0
        is_method = unit.children[0].content == "method"
        self._symbol_table.start_subroutine(is_method=is_method)

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
                var_dec_count += self._handle_variable_declaration(thing)

        # make declaration for function
        self._vm_line_writer.write_fn(name, var_dec_count)

        if unit.children[0].content == "constructor":
            # allocate memory for instance
            field_count = self._symbol_table.var_count(IdentifierKind.FIELD)
            self._vm_line_writer.write_push(Segment.CONSTANT, field_count)
            self._vm_line_writer.write_call("Memory.alloc", 1)
            self._vm_line_writer.write_pop(Segment.POINTER, 0)
        elif is_method:
            # assign hidden variable (instance) to pointer for proper context
            self._vm_line_writer.write_push(Segment.ARGUMENT, 0)
            self._vm_line_writer.write_pop(Segment.POINTER, 0)
            self._symbol_table.define("something", "anything", IdentifierKind.ARG)

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
