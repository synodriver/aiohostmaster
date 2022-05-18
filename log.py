# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter("[%(asctime)s in %(module)s.%(funcName)s] %(message)s %(levelname)s"))
logger.addHandler(handler)


def main():
    logger.debug("debug")
    logger.warning("warning")


if __name__ == "__main__":
    main()
