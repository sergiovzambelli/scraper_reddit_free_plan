import logging
import logging.config
import os

def setup_logging(default_level=logging.INFO):
    """Setup logging configuration."""
    log_file = os.getenv('LOG_FILE', 'scraping_log.txt')
    
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'file': {
                'class': 'logging.FileHandler',
                'filename': log_file,
                'formatter': 'standard',
                'level': default_level,
            },
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': default_level,
            },
        },
        'loggers': {
            'scraper_logger': {
                'handlers': ['file', 'console'],
                'level': default_level,
                'propagate': False,
            },
        },
    }

    logging.config.dictConfig(logging_config)

