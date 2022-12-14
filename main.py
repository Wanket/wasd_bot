from sys import exit

import inject

from app.app import App
from util.ilogger import ILogger


def main():
    err_code = App().run()

    logger = inject.instance(ILogger)

    if err_code != 0:
        logger.error(f"{__name__}: application exited with error code {err_code}")
    else:
        logger.info(f"{__name__}: application exited successfully")

    return err_code


if __name__ == "__main__":
    exit(main())
