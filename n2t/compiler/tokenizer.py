from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from n2t import xml_helpers
from n2t.shared import BaseParser, WhiteSpaceStrategy


class TokenType(Enum):
    KEYWORD = 0
    SYMBOL = 1
    IDENTIFIER = 2
    INT_CONST = 3
    STRING_CONST = 4


@dataclass
class Token:
    content: str
    type: TokenType


token_xml_mapping = {
    TokenType.INT_CONST: "integerConstant",
    TokenType.SYMBOL: "symbol",
    TokenType.STRING_CONST: "stringConstant",
    TokenType.KEYWORD: "keyword",
    TokenType.IDENTIFIER: "identifier",
}


class JackTokenizer(BaseParser):
    and_or_symbols = {"&", "|"}
    op_symbols = {"+", "-", "<", ">", "=", "~"}.union(and_or_symbols)
    extended_op_symbols = {"*", "/"}
    all_op_symbols = op_symbols.union(extended_op_symbols)
    all_symbols = op_symbols.union({"{", "}", "(", ")", "[", "]", ".", ",", ";"}).union(extended_op_symbols)
    keywords = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean",
                "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"}

    @staticmethod
    def _jack_tokenizer(text: str) -> List[Token]:
        empty_space = " "
        splitter = JackTokenizer.all_symbols.union({empty_space})
        override = {'"', "'"}
        overriding_with = None
        tokens: List[Token] = []
        collector = ""

        def collector_finish(given_type: Optional[TokenType] = None):
            nonlocal collector
            evaluated_type = None
            if not given_type:
                # try keyword
                if collector in JackTokenizer.keywords:
                    evaluated_type = TokenType.KEYWORD
                else:
                    # try int const
                    try:
                        integer = int(collector)
                        if integer < 0 or integer > 32767:
                            raise Exception("Encountered int that is outside 0-32767")
                        evaluated_type = TokenType.INT_CONST
                    except ValueError:
                        # then assume identifier
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

    def get_xml(self) -> str:
        start = "<tokens>\n"
        end = "</tokens>\n"
        body = ""

        for token in self.get_all():
            xml_tag_text = token_xml_mapping[token.type]
            body += xml_helpers.formulate_line(xml_tag_text, token.content) + "\n"

        return start + body + end


def get_tokens_as_xml(code: str) -> str:
    tokenizer = JackTokenizer(code)
    return tokenizer.get_xml()
