import re
import os
from enum import Enum
from typing import List, Optional, NamedTuple, Callable, TypeVar, Any


class FileExtension(Enum):
    VM = ".vm"
    ASM = ".asm"
    JACK = ".jack"


class WhiteSpaceStrategy(Enum):
    ELIMINATE_ALL = 0
    MAX_ONE_IN_BETWEEN_WORDS = 1


def default_tokenizer_fn(text: str) -> List[str]:
    return text.split("\n") if text else []


# NOTE on the `Any`... Maybe Python can do better than this?
class BaseParser:
    def __init__(self,
                 raw_file_contents: str,
                 white_space_strategy: WhiteSpaceStrategy,
                 tokenizer: Callable[[str], List[Any]] = default_tokenizer_fn):
        self._white_space_strategy = white_space_strategy
        self._cleaned_contents = self.clean_file(raw_file_contents)
        self._tokens = tokenizer(self._cleaned_contents)
        self._current_index = -1

    def current(self) -> Optional[Any]:
        return self._tokens[self._current_index] if \
            0 <= self._current_index < len(self._tokens) else None

    def has_more(self):
        return self._current_index + 1 < len(self._tokens)

    def advance(self) -> Any:
        self._current_index += 1
        return self._tokens[self._current_index]

    def clean_file(self, file: str) -> str:
        # TODO: needs to handle multiline comments...
        file = self.remove_multiline_comments(file)
        ret = []
        for line in file.split("\n"):
            cleaned_line = self.clean_line(line)
            if cleaned_line:
                ret.append(cleaned_line)
        return "\n".join(ret)

    def remove_multiline_comments(self, file: str) -> str:
        while True:
            start_index = file.find("/*")
            end_index = file.find("*/")
            if start_index < 0 and end_index < 0:
                break
            elif start_index >= 0 and end_index >= 0:
                file = file[0:start_index] + file[end_index + 2:]
            else:
                # TODO: create better error
                raise Exception("Improper multiline comment...")
        return file

    def clean_line(self, line: str):
        mostly_cleaned = line.split("//")[0].replace("\t", "")
        if self._white_space_strategy == WhiteSpaceStrategy.ELIMINATE_ALL:
            return mostly_cleaned.replace(" ", "")
        elif self._white_space_strategy == WhiteSpaceStrategy.MAX_ONE_IN_BETWEEN_WORDS:
            return re.sub('\s+', ' ', mostly_cleaned).strip()
        else:
            raise NotImplementedError


class File(NamedTuple):
    filename: str
    contents: str

    @property
    def filename_extensionless(self):
        return "".join(self.filename.split(".")[0:-1])


def read_file_to_str(path: str) -> str:
    with open(path, "r") as f:
        contents = f.read()
    return contents


def get_documents_from_path(path: str, file_extension: FileExtension) -> List[File]:
    ret: List[File] = []
    # if path is dir, read all file_extension.value files
    # if path is file, then assume it's a single file_extension.value file
    if os.path.isdir(path):
        # for now, just get files that are direct children of the dir
        for filename in os.listdir(path):
            parsed_extension = f".{filename.split('.')[-1]}"
            if file_extension.value in filename and parsed_extension == file_extension.value:
                this_path = f"{path}/{filename}"
                ret.append(File(filename, read_file_to_str(this_path)))
    else:
        filename = path.split("/")[-1]
        ret.append(File(filename, read_file_to_str(path)))
    return ret
