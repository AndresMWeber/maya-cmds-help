from . import commands
from .commands.scrape import Scrape

__all__ = ['commands', 'cli']
__version__ = '0.1.0'

cache = None
scraper = None


def scrape(maya_commands):
    global scraper
    global cache
    if scraper is None:
        scraper = Scrape()
        cache = scraper.cached

    scraper.query(maya_commands)
