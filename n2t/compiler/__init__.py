from n2t.compiler.compilation_engine import CompilationEngine
from n2t.compiler.tokenizer import JackTokenizer
from n2t.compiler.vm_writer import VMWriter


def compile_as_xml(code: str) -> str:
    tokenizer = JackTokenizer(code)
    engine = CompilationEngine(tokenizer)
    unit = engine.compile()
    return CompilationEngine.unit_as_xml(unit)


def compile_to_vm(code: str) -> str:
    tokenizer = JackTokenizer(code)
    engine = CompilationEngine(tokenizer)
    unit = engine.compile()
    return "\n".join(VMWriter(unit).get_lines_from_unit()) + "\n"
