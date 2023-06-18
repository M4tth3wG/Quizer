import os
from pathlib import Path

DEFAULT_DIRECTORY = Path(os.path.dirname(os.path.realpath(__file__))).joinpath('Quizzes')
GUI_RESOURCES = Path(os.path.dirname(os.path.realpath(__file__))).joinpath('gui_resources')