LOGGING_CONFIG = {
    "version": 1,  
    "disable_existing_loggers": False, 
    "formatters": {
        "standard": {  
            "format": "%(asctime)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": { 
            "class": "logging.StreamHandler", 
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"] 
    },
}