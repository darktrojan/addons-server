# -*- coding: utf-8 -*-
from django import test

from nose.tools import eq_

import amo
from addons.models import Addon
from files.models import File
from versions.models import Version


class TestFile(test.TestCase):
    """
    Tests the methods of the File model.
    """

    fixtures = ('base/addon_3615', 'base/addon_5579')

    def test_get_absolute_url(self):
        f = File.objects.get(id=67442)
        url = f.get_absolute_url(amo.FIREFOX, src='src')
        expected = ('/firefox/downloads/file/67442/'
                    'delicious_bookmarks-2.1.072-fx.xpi?src=src&confirmed=1')
        assert url.endswith(expected), url

    def test_latest_url(self):
        # With platform.
        f = File.objects.get(id=74797)
        base = '/en-US/firefox/downloads/latest/'
        expected = base + '{0}/platform:3/addon-{0}-latest.xpi'
        eq_(expected.format(f.version.addon_id), f.latest_xpi_url())

        # No platform.
        f = File.objects.get(id=67442)
        expected = base + '{0}/addon-{0}-latest.xpi'
        eq_(expected.format(f.version.addon_id), f.latest_xpi_url())

    def test_eula_url(self):
        f = File.objects.get(id=67442)
        eq_(f.eula_url(), '/addon/3615/eula/67442')

    def test_generate_filename(self):
        f = File.objects.get(id=67442)
        eq_(f.generate_filename(), 'delicious_bookmarks-2.1.072-fx.xpi')

    def test_generate_filename_platform_specific(self):
        f = File.objects.get(id=67442)
        f.platform_id = amo.PLATFORM_MAC.id
        eq_(f.generate_filename(), 'delicious_bookmarks-2.1.072-fx-mac.xpi')

    def test_generate_filename_many_apps(self):
        f = File.objects.get(id=67442)
        f.version.compatible_apps = (amo.FIREFOX, amo.THUNDERBIRD)
        eq_(f.generate_filename(), 'delicious_bookmarks-2.1.072-fx+tb.xpi')

    def test_generate_filename_ja(self):
        f = File()
        f.version = Version(version='0.1.7')
        f.version.compatible_apps = (amo.FIREFOX,)
        f.version.addon = Addon(name=u' フォクすけといっしょ')
        eq_(f.generate_filename(),
            u'\u30d5\u30a9\u30af\u3059\u3051\u3068\u3044\u3063\u3057\u3087'
            '-0.1.7-fx.xpi')
