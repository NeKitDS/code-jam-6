from project.core.api import SimpleBoot
from project.core.terminal import IOTerminal


if __name__ == "__main__":
    api = SimpleBoot().start()
    terminal = IOTerminal(api)
    terminal.start()
