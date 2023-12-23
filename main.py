import subprocess, rumps
import logging, logging.config
import lang_model as lm
from config_handler import config

### Logging ###

log_config = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(asctime)s [%(levelname)s] %(name)s (%(lineno)d): %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": config["Application"]["LOGGING_LEVEL"],
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": config["Application"]["LOGGING_FILE"],
            "level": config["Application"]["LOGGING_LEVEL"],
            "formatter": "simple",
        },
    },
    "root": {
        "level": config["Application"]["LOGGING_LEVEL"],
        "handlers": ["console", "file"],
    },
}

# Configure the logging system
logging.config.dictConfig(log_config)

# Create a logger
logger = logging.getLogger(__name__)


def _is_logging_debug():
    root = logger.getLogger()
    return any(handler.level <= logger.DEBUG for handler in root.handlers)


def _format_time(seconds: int) -> str:
    m = seconds // 60
    h = seconds // 3600
    if seconds < 86400:
        return f"{h}:{m}:{seconds}"
    else:
        d = seconds // 86400
        return f"{d} days, {h}:{m}:{seconds}"


### Clipboard ###
def read_from_clipboard():
    return subprocess.check_output("pbpaste", env={"LANG": "en_US.UTF-8"}).decode(
        "utf-8"
    )


def write_to_clipboard(output):
    process = subprocess.Popen(
        "pbcopy", env={"LANG": "en_US.UTF-8"}, stdin=subprocess.PIPE
    )
    process.communicate(output.encode("utf-8"))


### RUMPS ###
class HandyIntelligence(rumps.App):
    def __init__(self):
        super(HandyIntelligence, self).__init__("🌙")
        logger.debug("RUMPS init")
        self.default_icon = "🌙"
        self.complete_icon = "✅"

        self.board = None
        self.last_board = None
        self._check_counter = 0  # Used only when debug logging

    def calc_process(self, board: str, ind: str, repl=""):
        logger.debug("Calc Process init")
        self.title = "🌀"
        self.board = board.replace(ind, repl)
        write_to_clipboard(str(eval(board)))
        self.title = self.complete_icon

    def ai_process(self, board: str, response_func, ind: str, repl=""):
        logger.debug("AI Process init")
        self.title = "🌀"
        if repl != None:
            self.board = board.replace(ind, repl)
        write_to_clipboard(response_func(board))
        self.title = self.complete_icon

    @rumps.timer(1)
    def check_clipboard(self, _):
        if _is_logging_debug():
            self._check_counter += 1
            if self._check_counter % 900 == 0:  # 15 Minutes
                logger.debug(
                    f"Check: #{self._check_counter}, Running for {_format_time(self._check_counter)}"
                )
        self.board = read_from_clipboard()
        if self.last_board == self.board:
            self.title = self.default_icon
            return

        self.last_board = self.board
        logger.info(f"New Input: '{self.board}'")

        match self.board:
            case s if "|||" in s:
                self.ai_process(s, lm.spellcheck, "")

            case s if "?||" in s:
                self.ai_process(s, lm.general, "?||")

            case s if "|..|" in s:
                self.ai_process(s, lm.insert, "|..|", None)

            case s if "=||" in s:
                self.calc_process(s, "=||")

            case s if '||"' in s:
                self.ai_process(s, lm.quoted_instruct, '||"', None)

            case _:
                logger.info("No indicator present.")
                self.title = self.default_icon

        print()


if __name__ == "__main__":
    HandyIntelligence().run()
