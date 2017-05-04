# maya_signatures/commands/scrape.py
"""The maya online help command signature scraping command."""

from six import iteritems
import requests
import tempfile
import json
import shutil
import os
from .base import Base
from .cache import KeyMemoized
from bs4 import BeautifulSoup


class Scrape(Base):
    BASEURL = 'http://help.autodesk.com/cloudhelp/{MAYAVERSION}/ENU/Maya-Tech-Docs/CommandsPython/'
    EXTENSION = 'html'
    URL_BUILDER = '{BASEURL}{COMMAND}.{EXT}'
    CACHE_FILE = '%s.json' % __name__.split('.')[-1]
    FUNCTION_SET = {}

    def __init__(self, *args, **kwargs):
        super(Scrape, self).__init__(*args, **kwargs)
        self.depth = self.kwargs.get('--depth', 1)
        self.maya_version = self.kwargs.get('--mayaversion', ['2017'])[0]
        self.command_signatures = {}
        self.run()

    @property
    def stored_commands(self):
        return list(self.command_signatures)

    def get_command_flags(self, command):
        return zip(list(self.command_signatures[command]),
                   [self.command_signatures[command][flag]['short'] for flag in self.command_signatures[command]])

    def run(self):
        self.read_tempfile()
        self.store_commands()
        self.write_tempfile()
        return self.command_signatures

    def build_url(self, command):
        return self.URL_BUILDER.format(BASEURL=self.BASEURL.format(MAYAVERSION=self.maya_version),
                                       COMMAND=command,
                                       EXT=self.EXTENSION)

    def build_command_stub(self, command, shortname=False, combined=False):
        lut = {'boolean': 'bool', 'string': 'str', 'int': 'int'}
        kwargs = []
        shortname = False if combined else shortname

        for k, v in iteritems(self.command_signatures[command]):
            flag = k if not shortname else v['short']
            if combined:
                flag += '(%s)' % v['short']
            kwargs.append('{FLAG}={TYPE}'.format(FLAG=flag, TYPE=lut[v['data_type']]))
        signature = ', '.join(kwargs)
        return 'def {CMD}(*args, {SIG}):\n\tpass'.format(CMD=command, SIG=signature)

    def store_commands(self):
        for maya_command in self.kwargs.get('MAYA_CMDS', []):
            url = self.build_url(maya_command)
            self.command_signatures[maya_command] = self.scrape_command(self, url)

    def reset_cache(self):
        open(self.CACHE_FILE, 'w').close()

    def write_tempfile(self):
        f = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
        f.write(json.dumps(self.scrape_command.cache, ensure_ascii=False, indent=4, sort_keys=True))
        file_name = f.name
        f.close()
        shutil.copy(file_name, self.CACHE_FILE)
        print("wrote out tmp file %s" % os.path.join(os.getcwd(), self.CACHE_FILE))

    def read_tempfile(self):
        with open(self.CACHE_FILE, ) as data_file:
            try:
                data = json.load(data_file)
            except ValueError:
                data = {}
        print('Successfully loaded json data, loading into cache...')
        self.scrape_command.cache = data

    @KeyMemoized
    def scrape_command(self, maya_command_url):
        print('Trying to find command for web page: \n\t%s' % maya_command_url)
        web_page_data = requests.get(maya_command_url)
        soup_data = BeautifulSoup(web_page_data.content, 'html.parser')

        raw_flag_table = self.parse_flag_table(soup_data)
        flags = self.compile_flag_table(raw_flag_table)
        return flags

    @classmethod
    def parse_synopsis(cls, soup_code_object):
        synopses = []
        for child in [child for child in soup_code_object.children]:
            synopses.append(unicode(child) if not hasattr(child, 'string') else child.string)
        return synopses

    @classmethod
    def parse_flag_table(cls, soup_code_object):
        signature_table = [table for table in soup_code_object.body.find_all('table')
                           if 'Long name (short name)' in unicode(table.find_all('tr'))][0]

        data = []
        for table_row in signature_table.find_all('td'):
            # This is a ghetto way of checking whether it's the right row we want...but it works.
            if table_row.attrs.get('colspan') is None:
                text = str(table_row.text.strip()).replace('\n', ' ')
                # Might need refactoring later depending on how they format their flags/descriptions, but we'll see
                if len(text.split('(')) == 2 and not ' ' in text:
                    text = [t.replace(')', '') for t in text.split('(')]
                    data += text
                elif text:
                    data.append(text)

        return [data[x:x + 4] for x in range(0, len(data), 4)]

    @staticmethod
    def compile_flag_table(flag_data_set):
        flags = {}
        for flag_data in flag_data_set:
            name, short, data_type, description = flag_data
            flags[name] = {'short': short, 'data_type': data_type, 'description': description}

        return flags
