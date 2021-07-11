import re
from enum import Enum
from typing import List, Optional

Command = str


class WhiteSpaceStrategy(Enum):
    ELIMINATE_ALL = 0
    MAX_ONE_IN_BETWEEN_WORDS = 1


class BaseParser:
    def __init__(self, raw_file_contents: str, white_space_strategy: WhiteSpaceStrategy):
        self._white_space_strategy = white_space_strategy
        self._commands = self.parse_commands(raw_file_contents)
        self._current_command_index = -1

    def current_command(self) -> Optional[Command]:
        return self._commands[self._current_command_index] if \
            0 <= self._current_command_index < len(self._commands) else None

    def has_more_commands(self):
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
