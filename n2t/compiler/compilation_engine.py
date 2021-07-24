from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Any, Set

from n2t import xml_helpers
from n2t.compiler.tokenizer import TokenType, Token, token_xml_mapping, JackTokenizer


class WrapperType(Enum):
    SubroutineDeclaration = 0
    SubroutineBody = 1
    VariableDeclaration = 2
    Statements = 3
    LetStatement = 4
    DoStatement = 5
    ClassVariableDeclaration = 6
    ReturnStatement = 7
    ParameterList = 8
    IfStatement = 9
    Expression = 10
    Class = 11
    Term = 12
    ExpressionList = 13
    WhileStatement = 14


unit_xml_mapping = {
    WrapperType.SubroutineDeclaration: "subroutineDec",
    WrapperType.SubroutineBody: "subroutineBody",
    WrapperType.VariableDeclaration: "varDec",
    WrapperType.Statements: "statements",
    WrapperType.LetStatement: "letStatement",
    WrapperType.DoStatement: "doStatement",
    WrapperType.ClassVariableDeclaration: "classVarDec",
    WrapperType.ReturnStatement: "returnStatement",
    WrapperType.ParameterList: "parameterList",
    WrapperType.IfStatement: "ifStatement",
    WrapperType.WhileStatement: "whileStatement",
    WrapperType.Expression: "expression",
    WrapperType.Class: "class",
    WrapperType.Term: "term",
    WrapperType.ExpressionList: "expressionList",
}


@dataclass
class Unit:
    type: WrapperType
    children: List[Any]  # NOTE: can't type because recursive nature...


class CompilationEngine:
    _tokens: List[Token]

    def __init__(self, tokenizer: JackTokenizer):
        # TODO: it feels weird passing the parser then resetting it
        # TODO: it may make more sense for the token advance/retreat functionality to be split off
        tokenizer.reset()

        tokens = tokenizer.get_all()
        if not len(tokens):
            raise Exception("No tokens to compile...")
        if len(tokens) < 5 or (not tokens[0].type == TokenType.KEYWORD and tokens[0].content == "class"):
            raise Exception("Everything must be wrapped in a valid class...")

        self._tokenizer = tokenizer

    def compile(self) -> Unit:
        # excepts beginning `class Name {` and end `}`
        first = self._tokenizer.advance()
        second = self._tokenizer.advance()
        third = self._tokenizer.advance()
        if not first.content == "class" or not second.type == TokenType.IDENTIFIER or not third.content == "{":
            raise Exception("Class not correctly formed.")

        children = [first, second, third]

        # a class can have class var declarations or subroutine declarations
        while self._tokenizer.has_more():
            next_token = self._tokenizer.advance()
            if next_token.content in {"static", "field"}:
                children.append(self._compile_class_var_declaration(next_token))
            elif next_token.content in {"function", "method", "constructor"}:
                children.append(self._compile_subroutine_declaration(next_token))
            elif next_token.content == "}":
                if self._tokenizer.has_more():
                    next_token = self._tokenizer.advance()
                    raise Exception("Compiler didn't stick the landing... Found another token:", next_token)
                children.append(next_token)

        return Unit(WrapperType.Class, children)

    def _compile_class_var_declaration(self, first_token: Token) -> Unit:
        # first_token is expected to be the static/field keyword
        # ends in ; symbol
        children = [first_token]

        while True:
            next_token = self._tokenizer.advance()
            if next_token.content == ";":
                children.append(next_token)
                break
            else:
                children.append(next_token)

        return Unit(WrapperType.ClassVariableDeclaration, children)

    def _compile_subroutine_declaration(self, first_token: Token) -> Unit:
        # first_token is expected to be the function keyword
        # expects a return type, identifier, parameter list, body
        children = [first_token]
        return_type = self._tokenizer.advance()
        identifier = self._tokenizer.advance()
        parameter_list_start = self._tokenizer.advance()
        children.extend([return_type, identifier, parameter_list_start])
        parameter_list_children = []
        while True:
            next_token = self._tokenizer.advance()
            if next_token.content == ")":
                children.append(self._compile_parameter_list(parameter_list_children))
                children.append(next_token)
                break
            else:
                parameter_list_children.append(next_token)

        # TODO: why pass in first one out of tradition
        children.append(self._compile_subroutine_body(self._tokenizer.advance()))
        return Unit(WrapperType.SubroutineDeclaration, children)

    def _compile_subroutine_body(self, first_token: Token) -> Unit:
        # first_token is expected to be the { symbol
        # body can be virtually anything for now (if not weakly typed, it'd probably be picky here?)
        children = [first_token]

        while True:
            next_token = self._tokenizer.advance()
            if next_token.content == "var":
                children.append(self._compile_variable_declaration(next_token))
            else:
                self._tokenizer.retreat()
                children.extend(self._get_children_in_body_with_closing_brace())
                break

        return Unit(WrapperType.SubroutineBody, children)

    def _get_children_in_body_with_closing_brace(self, first_token: Optional[Token] = None) -> List:
        # TODO: type return
        children: List[Any] = [first_token] if first_token else []
        thing = False
        while True:
            next_token = self._tokenizer.advance()
            if next_token.content == "}" and thing:
                children.append(next_token)
                break
            else:
                self._tokenizer.retreat()
                children.append(self._compile_statements())
            thing = True
        return children

    def _compile_statements(self) -> Unit:
        children = []
        while True:
            next_token = self._tokenizer.advance()
            if next_token.content == "return":
                children.append(self._compile_return_statement(next_token))
            elif next_token.content == "let":
                children.append(self._compile_let_statement(next_token))
            elif next_token.content == "do":
                children.append(self._compile_do_statement(next_token))
            elif next_token.content == "if":
                children.append(self._compile_if_statement(next_token))
            elif next_token.content == "while":
                children.append(self._compile_while_statement(next_token))
            elif next_token.content == "}":
                self._tokenizer.retreat()
                break
            else:
                raise NotImplementedError(f"Wasn't ready to handle {next_token} when compiling statements")

        return Unit(WrapperType.Statements, children=children)

    def _compile_while_statement(self, first_token: Token) -> Unit:
        # first_token is expected to be `while`, second is `(`
        # TODO: similar to IF, combine? only thing different is `else` in the `while True:`
        # TODO: some of this logic should definitely be abstracted though
        children = [first_token, self._tokenizer.advance()]  # `while (`

        while True:
            next_token = self._tokenizer.advance()
            if next_token.content == ")":
                children.append(next_token)
                break
            else:
                children.append(self._compile_expression(next_token, {")"}))

        while True:
            next_token = self._tokenizer.advance()
            if next_token.content == "{":
                children.append(next_token)
                children.extend(self._get_children_in_body_with_closing_brace())
            else:
                self._tokenizer.retreat()
                break
        return Unit(WrapperType.WhileStatement, children)

    def _compile_if_statement(self, first_token: Token) -> Unit:
        # first_token is expected to be `if`, second is `(`
        children = [first_token, self._tokenizer.advance()]  # `if (`

        while True:
            next_token = self._tokenizer.advance()
            if next_token.content == ")":
                children.append(next_token)
                break
            else:
                children.append(self._compile_expression(next_token, {")"}))

        while True:
            next_token = self._tokenizer.advance()
            if next_token.content == "{":
                children.append(next_token)
                children.extend(self._get_children_in_body_with_closing_brace())
            elif next_token.content == "else":
                children.append(next_token)
            else:
                self._tokenizer.retreat()
                break
        return Unit(WrapperType.IfStatement, children)

    def _compile_let_statement(self, first_token: Token) -> Unit:
        # first_token is expected to be `let`
        # next tokens are identifier, `=` symbol, then an expression, ending in `;`
        # but it can also be assigning using array index as well
        children = [first_token]
        identifier = self._tokenizer.advance()
        if self._tokenizer.peak().content == "[":
            children.append(identifier)
            children.append(self._tokenizer.advance())  # add [
            self._tokenizer.advance()
            children.append(self._compile_expression(self._tokenizer.peak(), {"]"}))  # TODO: first arg stupid
            children.append(self._tokenizer.advance())  # add ]
            children.append(self._tokenizer.advance())  # add =
        else:
            assignment_symbol = self._tokenizer.advance()
            children.extend([identifier, assignment_symbol])

        while True:
            next_token = self._tokenizer.advance()
            if next_token.content == ";":
                children.append(next_token)
                break
            else:
                children.append(self._compile_expression(next_token, {";"}))

        return Unit(WrapperType.LetStatement, children)

    def _compile_expression(self, first_token: Token, end_symbols: Set[str]) -> Unit:
        # TODO: do we really need first_token???
        children = []
        self._tokenizer.retreat()
        while True:
            next_token = self._tokenizer.advance()
            peaked_token = self._tokenizer.peak()
            if next_token.content in end_symbols:
                self._tokenizer.retreat()
                break
            elif next_token.content == "(":
                children.append(self._compile_term(next_token, {")"}, include=True))
            elif self._tokenizer.previous().content == "(" and next_token.content in {"~", "-"}:
                if peaked_token.content == "(":
                    children.append(self._compile_term(next_token, {")"}, include=True))
                else:
                    children.append(self._compile_term(next_token, {peaked_token.content}, include=True))
            elif peaked_token.content == ".":
                # function call whose term ends with included `)`
                children.append(self._compile_term(next_token, {")"}, include=True))
            elif peaked_token.content == "(":
                # expression whose term ends with included `)`
                children.append(next_token)
                children.append(self._compile_term(self._tokenizer.advance(), {")"}, include=True))
            elif peaked_token.content == "[":
                # array index whose term ends with included `]`
                children.append(self._compile_term(next_token, {"]"}, include=True))
            elif next_token.type != TokenType.SYMBOL and peaked_token.type == TokenType.SYMBOL:
                children.append(self._compile_term(next_token, {peaked_token.content}))
            else:
                children.append(next_token if next_token.type == TokenType.SYMBOL else self._compile_term(next_token))
        return Unit(WrapperType.Expression, children)

    def _compile_term(self, first_token: Token, end_symbols: Set[str] = {";", ")", ","}, include=False) -> Unit:
        children = [first_token]
        while True:
            if first_token.content in end_symbols:
                break
            next_token = self._tokenizer.advance()
            if len(children) == 1 and first_token.content in {"~", "-"}:
                if next_token.content == "(":
                    children.append(self._compile_term(next_token, {")"}, include=True))
                else:
                    children.append(self._compile_term(next_token, {next_token.content}))
                break
            elif next_token.content in end_symbols:
                if include:
                    children.append(next_token)
                else:
                    self._tokenizer.retreat()
                break
            elif next_token.content == "[":
                children.extend([next_token, self._compile_expression(self._tokenizer.advance(), {"]"})])
            elif len(children) == 1 and first_token.content == "(":
                children.append(self._compile_expression(next_token, {")"}))
            elif next_token.content == "(":
                children.extend([next_token, self._compile_expression_list()])
            else:
                children.append(next_token)
        return Unit(WrapperType.Term, children)

    def _compile_do_statement(self, first_token: Token) -> Unit:
        # first_token is expected to be a `do` keyword while the second is an identifier
        children = [first_token, self._tokenizer.advance()]
        third = self._tokenizer.advance()  # `(` or `.`
        children.append(third)
        if third.content == ".":
            fourth = self._tokenizer.advance()  # identifier
            fifth = self._tokenizer.advance()  # ( list
            children.extend([fourth, fifth])

        # TODO: this doesn't seem right, should be parameter, not expression?
        children.append(self._compile_expression_list())
        children.append(self._tokenizer.advance())  # )

        last_token = self._tokenizer.advance()
        assert last_token.content == ";", f"Expected last token of do statement to be a `;` but was {last_token.content}"
        children.append(last_token)
        return Unit(WrapperType.DoStatement, children)

    def _compile_return_statement(self, first_token: Token) -> Unit:
        # first_token is expected to be the return keyword
        # for now, assume no return, but TODO: fix it later
        children = [first_token]
        while True:
            next_token = self._tokenizer.advance()
            if next_token.content == ";":
                children.append(next_token)
                break
            else:
                children.append(self._compile_expression(next_token, {";"}))
        # TODO: this is like the variable declaration...
        return Unit(WrapperType.ReturnStatement, children)

    def _compile_variable_declaration(self, first_token: Token) -> Unit:
        # first_token is expected to be the var keyword
        # for now, body is expected to be terminal atoms, TODO: not realistic
        children = [first_token]
        while True:
            next_token = self._tokenizer.advance()
            children.append(next_token)
            if next_token.content == ";":
                break
        return Unit(WrapperType.VariableDeclaration, children)

    @staticmethod
    def _compile_parameter_list(tokens: List[Token]) -> Unit:
        # For now, just return tokens
        return Unit(WrapperType.ParameterList, children=tokens)

    def _compile_expression_list(self) -> Unit:
        children = []
        while True:
            next_token = self._tokenizer.advance()
            if next_token.content == ")":
                self._tokenizer.retreat()
                break
            elif next_token.content == ",":
                children.append(next_token)
            else:
                children.append(self._compile_expression(next_token, {")", ","}))
        return Unit(WrapperType.ExpressionList, children)

    @staticmethod
    def unit_as_xml(unit: Unit, level=0) -> str:
        xml_tag_text = unit_xml_mapping[unit.type]
        content = ""
        content += f"{' ' * level}<{xml_tag_text}>\n"
        for child in unit.children:
            if isinstance(child, Unit):
                content += CompilationEngine.unit_as_xml(child, level + 2)
            elif isinstance(child, Token):
                line = xml_helpers.formulate_line(token_xml_mapping[child.type], child.content)
                content += f"{' ' * (level + 2)}{line}\n"
            else:
                raise NotImplementedError
        content += f"{' ' * level}</{xml_tag_text}>\n"
        return content
