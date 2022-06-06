# -*- coding: utf-8 -*-
import logging

logging.basicConfig(level=logging.ERROR,
                    format='[%(name)s] [%(levelname)s] %(asctime)s | %(message)s',
                    datefmt='[%d:%b:%y %H:%M:%S]',
                    filename='log.txt')
logger = logging.getLogger("rolgroup")
