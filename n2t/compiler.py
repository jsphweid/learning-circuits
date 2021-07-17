from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from n2t.shared import BaseParser, WhiteSpaceStrategy


class TokenType(Enum):
    KEYWORD = 0
    SYMBOL = 1
    IDENTIFIER = 2
    INT_CONST = 3
    STRING_CONST = 4


class JackKeyword(Enum):
    CLASS = 0
    METHOD = 1
    FUNCTION = 2
    CONSTRUCTOR = 3
    INT = 4
    BOOLEAN = 5
    CHAR = 6
    VOID = 7
    VAR = 8
    STATIC = 9
    FIELD = 10
    LET = 11
    DO = 12
    IF = 13
    ELSE = 14
    WHILE = 15
    RETURN = 16
    TRUE = 17
    FALSE = 18
    NULL = 19
    THIS = 20


class JackAnalyzer:
    def __init__(self):
        pass


@dataclass
class Token:
    content: str
    type: TokenType


class JackTokenizer(BaseParser):

    @staticmethod
    def _jack_tokenizer(text: str) -> List[Token]:
        symbols = {"{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"}
        keywords = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean",
                    "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"}
        empty_space = " "
        splitter = symbols.union({empty_space})
        override = {'"', "'"}
        overriding_with = None
        tokens: List[Token] = []
        collector = ""

        def collector_finish(given_type: Optional[TokenType] = None):
            nonlocal collector
            evaluated_type = None
            if not given_type:
                # try keyword
                if collector in keywords:
                    evaluated_type = TokenType.KEYWORD
                else:
                    # try int const
                    try:
                        integer = int(collector)
                        if integer < 0 or integer > 32767:
                            raise Exception("Encountered int that is outside 0-32767")
                        evaluated_type = TokenType.INT_CONST
                    except ValueError:
                        # assume identifier
                        evaluated_type = TokenType.IDENTIFIER

            if collector:
                tokens.append(Token(collector, given_type if given_type else evaluated_type))
                collector = ""

        for char in text:

            # We want quotes to be handled differently
            if overriding_with:
                if char == overriding_with:  # got to end of quote section
                    collector_finish(TokenType.STRING_CONST)
                    overriding_with = None
                else:  # still going with the override
                    collector += char
                continue
            if char in override:
                overriding_with = char
                continue

            # If it's a non-quote, then we can handle those cases here
            if char == "\n":
                pass
            elif char in splitter:
                collector_finish()
                if char != empty_space:
                    tokens.append(Token(char, TokenType.SYMBOL))
            else:
                collector += char
        return tokens

    def __init__(self, raw_file_contents: str):
        super().__init__(raw_file_contents,
                         WhiteSpaceStrategy.MAX_ONE_IN_BETWEEN_WORDS,
                         tokenizer=JackTokenizer._jack_tokenizer)

    def token_type(self) -> TokenType:
        return self.current().type

    def keyword(self) -> JackKeyword:
        if self.token_type() != TokenType.KEYWORD:
            raise Exception("Shouldn't call keyword() when token type is not KEYWORD")
        pass

    def symbol(self) -> str:
        if self.token_type() != TokenType.SYMBOL:
            raise Exception("Shouldn't call symbol() when token type is not SYMBOL")
        pass

    def identifier(self) -> str:
        if self.token_type() != TokenType.IDENTIFIER:
            raise Exception("Shouldn't call identifier() when token type is not IDENTIFIER")
        pass

    def int_val(self) -> str:
        if self.token_type() != TokenType.INT_CONST:
            raise Exception("Shouldn't call int_val() when token type is not INT_CONST")
        pass

    def string_val(self) -> str:
        if self.token_type() != TokenType.STRING_CONST:
            raise Exception("Shouldn't call string_val() when token type is not STRING_CONST")
        pass


def tokens_to_xml(tokens: List[Token]) -> str:
    start = "<tokens>\n"
    end = "</tokens>\n"
    body = ""

    mapping = {
        TokenType.INT_CONST: "integerConstant",
        TokenType.SYMBOL: "symbol",
        TokenType.STRING_CONST: "stringConstant",
        TokenType.KEYWORD: "keyword",
        TokenType.IDENTIFIER: "identifier",
    }

    def formulate_line(xml_tag_text: str, content: str) -> str:
        special_char_mapping = {
            "<": "&lt;",
            ">": "&gt;",
            "&": "&amp;",
        }
        formatted_content = special_char_mapping[content] if content in special_char_mapping else content
        return f"<{xml_tag_text}> {formatted_content} </{xml_tag_text}>"

    for token in tokens:
        xml_tag_text = mapping[token.type]
        body += formulate_line(xml_tag_text, token.content) + "\n"

    return start + body + end


def tokenize(code: str) -> List[Token]:
    tokenizer = JackTokenizer(code)
    tokens = []
    while tokenizer.has_more():
        token = tokenizer.advance()
        tokens.append(token)
    return tokens


class CompilationEngine:
    def __init__(self):
        pass
