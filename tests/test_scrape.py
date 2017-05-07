import maya_signatures.commands.scrape as scrape
import unittest
import os


class TestBase(unittest.TestCase):
    def setUp(self):
        super(TestBase, self).setUp()
        self.scraper = scrape.Scrape()


class TestScrape(TestBase):
    def test_instantiation(self):
        scrape.Scrape()

    def test_instantiation_with_command(self):
        scraper = scrape.Scrape('ls')
        self.assertEquals(scraper.stored_commands, ['ls'])

    def test_stored_commands(self):
        self.scraper.query('ls')
        self.assertEquals(self.scraper.stored_commands, ['ls'])

    def test_instantiation_with_commands(self):
        scraper = scrape.Scrape(['ls', 'group'])
        self.assertEquals(sorted(scraper.stored_commands), sorted(['ls', 'group']))

    def test_instantiation_with_command_and_run(self):
        scraper = scrape.Scrape('ls')
        scraper.run()
        self.assertEquals(scraper.stored_commands, ['ls'])

    def testquery_single(self):
        self.assertIsNone(self.scraper.query('joint'))

    def testquery_multiple(self):
        self.assertIsNone(self.scraper.query(['joint', 'group']))

    def test_reset_cache(self):
        scraper = scrape.Scrape('group')
        scraper.reset_cache()
        self.assertEquals(scraper.cached, {})

    def test_get_command_flags(self):
        self.scraper.query('group')
        self.scraper.get_command_flags('group')

    def test_build_command_stub(self):
        self.scraper.query('joint')
        stub = self.scraper.build_command_stub('joint')
        exec(compile(stub, '<string>', 'exec'))
        self.assertIn('joint', locals())

    def test_build_command_stub_shortname(self):
        self.scraper.query('joint')
        stub = self.scraper.build_command_stub('joint', shortname=True)
        exec(compile(stub, '<string>', 'exec'))
        self.assertIn('joint', locals())

    def test_build_command_stub_combined(self):
        self.scraper.query('joint')
        self.scraper.build_command_stub('joint', combined=True)

    def test_cache_file(self):
        self.scraper.query('joint')
        self.assertTrue(os.path.isfile(self.scraper.cache_file))
