from enum import Enum

token = "5147701461:AAGXQC2w_h0nKIKS8r--3GEY8KsS4Rh8T64"
db_file = "database.vdb"


class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_CHOOSE = "1"
    S_ENTER_FILM = "2"
    S_ENTER_TRUE_FILM = "3"
    S_ENTER_COMMAND = "4"
    S_END = "5"
