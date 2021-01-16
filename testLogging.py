#!/usr/bin/env python


import logging
import logging.config

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers':{
        'console': {
            'class' : 'logging.StreamHandler',
            'formatter': 'standard',
            'level'   : 'INFO',
            'stream'  : 'ext://sys.stdout'
        },
        'file': {
            'class' : 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': 'logconfig.log',
            'maxBytes': 1024,
            'backupCount': 3
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        }
    }
})

LOG = logging.getLogger('testlogger')

LOG.info('INFO log')
