import importlib
from typing import Dict, List, Optional

from project.core.command import Command
from project.core.utils import OSException

# Set bin and terminal path
BIN_PATH = 'project.file_system.bin'
Terminal = 'project.terminal.Terminal'


class Parser:
    def __init__(self) -> None:
        # Setup initial commands listing
        self._commands: Dict[str, Command] = {}

    def list_commands(self) -> List[Command]:
        """
        Get list of commands
        :return:
        """
        return list(self._commands.values())

    def get_command(self, name: str) -> Optional[Command]:
        """
        Get command from commands listing
        :param name:
        :return:
        """
        return self._commands.get(name)

    def add_command(self, command: Command) -> None:
        """
        Add command to commands listing
        :param command:
        :return:
        """
        self._commands[command.name] = command

    def load_command(self, module: str, char: str = '.') -> None:
        """
        Load command to parser
        :param module:
        :param char:
        :return:
        """
        # Get path of command
        path: str = make_path(module)

        # Try to import command by path that requested, raise ImportError when command don't exist
        try:
            module = importlib.import_module(path)  # type: ignore
        except ImportError:
            return print(f'Could not load command: {module!r}.')

        # Check does command module have setup function, else return and print out info
        if not hasattr(module, 'setup'):
            return print(f'Command module does not have setup function: {module!r}.')

        # Setup module
        module.setup(self)

    def execute(self, string: str, term: Terminal) -> None:
        """
        Execute command by searching from commands. Raise OSException when can't find command.
        :param string:
        :param term:
        :return:
        """
        # Generate arguments list
        args: List[str] = string.split()

        # Check if arguments list is empty. If this is, return.
        if not args:
            return

        # Get commands
        commands = self._commands

        # Get current command
        command_name = args.pop(0)

        # Check if command in commands listing and if it is, execute
        if command_name in commands:
            return commands.get(command_name).execute(term=term, args=args)

        # When can't find command, raise error
        raise OSException(f'error: could not execute string: {string!r}')


def make_path(module: str) -> str:
    """
    Generate path of provided module
    :param module:
    :return:
    """
    return ('.').join(BIN_PATH.split('.') + module.split('.'))
