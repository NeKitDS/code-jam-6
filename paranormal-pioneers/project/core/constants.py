from project.core.path import Path

# Lock exiting from env
CANNOT_EXIT_ENV = True

# Get root dir
ROOT = Path(__file__).parent.parent

# Set file system location
FILE_SYSTEM = ROOT / 'file_system'

# Set Bin folder location
BIN_DIR = FILE_SYSTEM / 'bin'
