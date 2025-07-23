# logging_config.py
import logging
import os

def setup_logger(log_file="custom_logging/logs/robot_simulator.log", level=logging.DEBUG):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Root logger setup
    logging.basicConfig(
        level=level,
        handlers=[file_handler]
    )
