import logging
import subprocess, rumps, time
import lang_model as lm
from config_handler import config

### Logging ###

log_config = {
    "version": 1,
    "formatters": {
        "simple": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
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
        self.default_icon = "🌙"
        self.complete_icon = "✅"

        self.board = None
        self.last_board = None

    def calc_process(self, ind: str, repl=""):
        self.title = "🌀"
        self.board = self.board.replace(ind, repl)
        write_to_clipboard(str(eval(self.board)))
        self.title = self.complete_icon

    def ai_process(self, response_func, ind: str, repl=""):
        self.title = "🌀"
        if repl != None:
            if self.board.endswith("?||"):
                self.board = self.board.replace("?||", "?")
            else:
                self.board = self.board.replace(ind, repl)
        write_to_clipboard(response_func(self.board))
        self.title = self.complete_icon

    @rumps.timer(1)
    def check_clipboard(self, _):
        self.board = read_from_clipboard()
        if self.last_board == self.board:
            self.title = self.default_icon
            return

        self.last_board = self.board
        print(f"New Input: '{self.board}'")

        if "|||" in self.board:
            self.ai_process(lm.spellcheck, "|||")
        elif "?||" in self.board:
            self.ai_process(lm.general, "?||")
        elif "|..|" in self.board:
            self.ai_process(lm.insert, "|..|", None)
        elif "=||" in self.board:
            self.calc_process("=||")
        elif '||"' in self.board:
            self.ai_process(lm.quoted_instruct, '||"', None)
        else:
            print("No indicator present.")
            self.title = self.default_icon
        print()


if __name__ == "__main__":
    HandyIntelligence().run()
