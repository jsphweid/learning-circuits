import re
import os
from enum import Enum
from typing import List, Optional, NamedTuple

Command = str


class FileExtension(Enum):
    VM = ".vm"
    ASM = ".asm"
    JACK = ".jack"


class WhiteSpaceStrategy(Enum):
    ELIMINATE_ALL = 0
    MAX_ONE_IN_BETWEEN_WORDS = 1


class BaseParser:
    def __init__(self, raw_file_contents: str, white_space_strategy: WhiteSpaceStrategy):
        self._white_space_strategy = white_space_strategy
        self._commands = self.parse_commands(raw_file_contents)
        self._current_command_index = -1

    def current(self) -> Optional[Command]:
        return self._commands[self._current_command_index] if \
            0 <= self._current_command_index < len(self._commands) else None

    def has_more(self):
        return self._current_command_index + 1 < len(self._commands)

    def advance(self) -> Command:
        self._current_command_index += 1
        return self._commands[self._current_command_index]

    def parse_commands(self, file: str) -> List[Command]:
        ret = []
        for line in file.split("\n"):
            cleaned_line = self.clean_line(line)
            if cleaned_line:
                ret.append(cleaned_line)
        return ret

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
