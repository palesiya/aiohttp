import logging
import json
import traceback


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "datetime": self.formatTime(record, "%Y-%m-%dT%H:%M:%S.%s"),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if record.exc_info:
            log_record["exception"] = traceback.format_exc()
        return json.dumps(log_record)
