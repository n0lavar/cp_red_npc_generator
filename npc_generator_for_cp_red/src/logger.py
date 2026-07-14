#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import logging
import sys


class LoggerLevelScope:
    def __init__(self, temp_level: int):
        self.temp_level = temp_level

    def __enter__(self):
        logger = logging.getLogger()
        self.initial_level = logger.getEffectiveLevel()
        logger.setLevel(max(self.temp_level, self.initial_level))

    def __exit__(self, exception_type, exception_value, traceback):
        logger = logging.getLogger()
        logger.setLevel(self.initial_level)


def is_debugger_active() -> bool:
    return hasattr(sys, 'gettrace') and sys.gettrace() is not None


def setup_logging(args: argparse.Namespace):
    if args.foundry_json:
        logging.disable(logging.CRITICAL)
    else:
        logging.basicConfig(level=logging.DEBUG if is_debugger_active() else logging.getLevelName(args.log_level),
                            format="%(message)s")
