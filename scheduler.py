import logging
import schedule
import time
from scraping import perform_scraping
from logging_config import setup_logging

setup_logging()
logger = logging.getLogger('scraper_logger')

def scraping_routine():
    logger.info("Starting scraping routine...")
    perform_scraping() 
    logger.info("Scraping routine completed.")

scraping_routine()

# Schedule the execution every minute
schedule.every(1).minutes.do(scraping_routine)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    logger.info("Scraping scheduled tasks stopped by user.")

