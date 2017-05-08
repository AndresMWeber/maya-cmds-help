from . import commands
from .commands.scrape import Scrape
from . import version

__version__ = version.__version__
__all__ = ['version', 'commands', 'cli']

CACHE = None
SCRAPER = None


def scrape(maya_commands):
    """ Generic entry point for ease of use, returns maya_signatures.commands.scrape.Scraper(<input>).query
    :param maya_commands: Commands to query and return
    :return: 
    """
    global SCRAPER
    global CACHE
    if SCRAPER is None:
        SCRAPER = Scrape()
        CACHE = SCRAPER.cached

    SCRAPER.query(maya_commands)
