from argparse import ArgumentParser, Namespace
from types import FunctionType
from typing import Any, Callable, List, Optional, Tuple, Union

from project.core.utils import OSException

Function = Callable[[Any], Any]
Terminal = 'project.terminal.Terminal'


class PatchedParser(ArgumentParser):
    def exit(self, status: int = 0, message: str = '') -> None:
        """
        Raise OSException with message of exit
        :param status:
        :param message:
        :return:
        """
        raise OSException(message.strip('\n'))


class Option:
    def __init__(self, func: Callable, *args: Any, **kwargs: Any) -> None:
        if not isinstance(func, FunctionType):
            raise TypeError(f'Expected function, got type {type(func).__name__}.')

        self._func = func
        self._args = args
        self._kwargs = kwargs

    def __repr__(self) -> str:
        return f'<Option func={self._func} args={self._args} kwargs={self._kwargs}>'

    def _call(self, *args: Any, **kwargs: Any) -> Any:
        """
        Call function with args and kwargs.
        :param args:
        :param kwargs:
        :return:
        """
        return self._func(*args, **kwargs)

    def _expose_to(self, parser: ArgumentParser) -> None:
        parser.add_argument(*self._args, **self._kwargs)


def option(*args: Any, **kwargs: Any) -> Function:
    """
    Return wrapper function
    :param args:
    :param kwargs:
    :return:
    """
    def wrapper(f: Function) -> Option:
        """
        Return Option of function (f)
        :param f:
        :return:
        """
        return Option(f, *args, **kwargs)

    return wrapper


def setup_parser(**kwargs) -> PatchedParser:
    """
    Setup parser and and add -h and --help arguments for help messages.
    :param kwargs:
    :return:
    """
    # Update add_help kwarg, set it False
    kwargs.update(add_help=False)

    # Get parser
    parser = PatchedParser(**kwargs)

    # Add help argument to parser
    parser.add_argument(
        '-h', '--help', action='store_true', default=False,
        help='Show help on how to use a command.'
    )

    # Return parser
    return parser


class Command:
    def __init__(self, name: Optional[str] = None) -> None:
        self._opt: List[Option] = []
        self._parser: PatchedParser = setup_parser(prog=name, description=self.doc)

        self._name: str = (
            self.__class__.__name__ if name is None else name
        )

        self._make_args()

    def __repr__(self) -> str:
        return f'<Command {self.name}>'

    @property
    def doc(self) -> Optional[str]:
        """
        Return documentation string
        :return:
        """
        return self.__class__.__doc__

    @property
    def parser(self) -> ArgumentParser:
        """
        Return command parser
        :return:
        """
        return self._parser

    @property
    def name(self) -> str:
        """
        Return name of command
        :return:
        """
        return self._name

    def execute(
        self, term: Terminal, args: Union[str, List[str], Tuple[str]] = ()
    ) -> Any:
        """
        Execute command
        :param term:
        :param args:
        :return:
        """
        ns: Namespace = self._parse(args)

        if not ns.help:

            for option in self._opt:
                option._call(self, ns=ns, term=term)

            return self.main(ns=ns, term=term)

        else:
            return self.format_help()

    def format_help(self) -> str:
        """
        Return formatted help message.
        :return:
        """
        return self.parser.format_help().replace('\n\n', '\n').strip('\n')

    def main(self, ns: Namespace, term: Terminal) -> Any:
        pass

    def _parse(self, args: Union[str, List[str]]) -> Namespace:
        """
        Arguments Parser. Convert arguments to list when they are string.
        :param args:
        :return:
        """
        if isinstance(args, str):
            args: List[str] = args.split()

        return self._parser.parse_args(args)

    def _make_args(self) -> None:
        """
        Arguments Handler
        :return:
        """
        for entry in (self.__class__.__dict__):
            maybe_option = getattr(self, entry)
            if isinstance(maybe_option, Option):
                maybe_option._expose_to(self._parser)
                self._opt.append(maybe_option)
