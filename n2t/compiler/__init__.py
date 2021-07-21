from n2t.compiler.compilation_engine import CompilationEngine
from n2t.compiler.tokenizer import JackTokenizer


def compile_as_xml(code: str) -> str:
    tokenizer = JackTokenizer(code)
    engine = CompilationEngine(tokenizer)
    unit = engine.compile()
    return CompilationEngine.unit_as_xml(unit)


def compile_to_vm(code: str) -> str:
    tokenizer = JackTokenizer(code)
    engine = CompilationEngine(tokenizer)
    unit = engine.compile()
    print('unit', CompilationEngine.unit_as_xml(unit))
    return ""
