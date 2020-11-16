import logging
import sys

LOG_LEVEL = [
    logging.CRITICAL,
    logging.ERROR,
    logging.WARNING,
    logging.INFO,
    logging.DEBUG
]

logger = logging.getLogger(__name__)
logFormat = '%(asctime)s - [%(levelname)s] %(message)s'
logFormatter = logging.Formatter(fmt=logFormat, datefmt='%Y-%m-%d %H:%M:%S')
logHandler = logging.StreamHandler(stream=sys.stdout)  # default
logHandler.setFormatter(fmt=logFormatter)
logger.addHandler(hdlr=logHandler)


def log(level):
    # ログレベルの設定
    logger.setLevel(level=level)

    # ログの出力
    logger.critical('%s - %s - %s', 'language', 'Python', 'Django')
    logger.error('%s - %s - %s', 'language', 'Ruby', 'Ruby on Rails')
    logger.warning('%s - %s - %s', 'language', 'PHP', 'Laravel')
    logger.info('%s - %s - %s', 'language', 'Java', 'Spring Framework')
    logger.debug('%s - %s - %s', 'language', 'Go', 'Echo')


def log_output():
    for level in LOG_LEVEL:
        print(f'===== {level} =====')
        log(level)


if __name__ == "__main__":
    log_output()
