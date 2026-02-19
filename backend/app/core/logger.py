import logging
import json
import asyncio
import sys
import re
from typing import Any

class WebSocketHandler(logging.Handler):
    def __init__(self, broadcaster: Any):
        super().__init__()
        self.broadcaster = broadcaster

    def emit(self, record):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return # No loop running, can't broadcast
            
        log_entry = self.format(record)
        status = getattr(record, "status", record.levelname)
        message = {
            "text": f"> {log_entry}",
            "status": status,
            "color": self.get_color(status)
        }
        
        if self.broadcaster:
            # Since logging might happen from a sync context, we need to handle the async broadcast
            try:
                loop.create_task(self.broadcaster(json.dumps(message)))
            except Exception:
                pass

    def get_color(self, levelname):
        colors = {
            "DEBUG": "text-gray-500",
            "INFO": "text-gray-400",
            "WARNING": "text-amber-400",
            "ERROR": "text-red-400",
            "CRITICAL": "text-red-600 font-bold",
            "PLAN": "text-blue-400",
            "SEARCH": "text-cyan-400",
            "CODE": "text-violet-400",
            "TEST": "text-green-400",
            "PR": "text-blue-400",
            "SUCCESS": "text-emerald-400",
            "FAIL": "text-rose-400",
            "WAIT": "text-gray-400"
        }
        return colors.get(levelname, "text-gray-400")

class StreamToLogger:
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        # Also write to original stream so we can see it in the terminal
        if self.log_level == logging.ERROR:
            sys.__stderr__.write(buf)
        else:
            sys.__stdout__.write(buf)

        for line in buf.rstrip().splitlines():
            line = line.strip()
            if not line: continue
            
            # Try to detect [STATUS] message pattern
            match = re.match(r'^\[([A-Z]+)\]\s+(.*)', line)
            if match:
                status = match.group(1)
                text = match.group(2)
                self.logger.log(self.log_level, text, extra={"status": status})
            else:
                self.logger.log(self.log_level, line)

    def flush(self):
        pass

def setup_websocket_logger(broadcaster: Any, redirect_stdout: bool = True):
    logger = logging.getLogger("sentinel")
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers
    if not any(isinstance(h, WebSocketHandler) for h in logger.handlers):
        handler = WebSocketHandler(broadcaster)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    if redirect_stdout:
        sys.stdout = StreamToLogger(logger, logging.INFO)
        sys.stderr = StreamToLogger(logger, logging.ERROR)
        
    return logger
