# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test import Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

class WebTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(WebTest, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.timeout = 2

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(WebTest, cls).tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('admin')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('admin')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

        WebDriverWait(self.selenium, self.timeout).until(
            lambda driver: driver.find_element_by_tag_name('body')
        )
