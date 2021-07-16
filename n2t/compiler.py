from n2t.shared import BaseParser, WhiteSpaceStrategy


class JackAnalyzer:
    def __init__(self):
        pass


class JackTokenizer(BaseParser):
    def __init__(self, raw_file_contents: str):
        super().__init__(raw_file_contents, WhiteSpaceStrategy.MAX_ONE_IN_BETWEEN_WORDS)


class CompilationEngine:
    def __init__(self):
        pass
