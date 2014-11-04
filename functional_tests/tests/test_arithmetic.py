#!/usr/bin/env python3
# coding: utf-8

"""functional tests for the arithmetic module
"""

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import unittest
from django.test import LiveServerTestCase
import time


def sleep_a_bit():
    time.sleep(0)


class MyLiveServerTestCase(LiveServerTestCase):

    def assertAreNotInPage(self, text_list):
        for text in text_list:
            self.assertNotIn(text, self.browser.page_source)

    def assertAreInPage(self, text_list):
        for text in text_list:
            self.assertIn(text, self.browser.page_source)


class VisitorTest(MyLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.server_url = self.live_server_url
        # self.server_url = "http://django.amk.uni-obuda.hu/django"

    def tearDown(self):
        self.browser.quit()

    def test_surfing_on_the_page(self):
        self.browser.get(self.server_url + '/arithmetic/')
        self.browser.set_window_size(1024, 700)

        coding_link = self.browser.find_element_by_partial_link_text(
            'Kódolás gyak')

        sleep_a_bit()
        coding_link.click()

        self.assertTrue(
            self.browser.current_url.endswith('coding/random/exercise/'))

        self.browser.get(self.server_url + '/arithmetic/')

        decoding_link = self.browser.find_element_by_partial_link_text(
            "Dekódolás")

        sleep_a_bit()
        decoding_link.click()

        solution_link = self.browser.find_element_by_xpath(
            "//input[@value='Megoldás']")

        sleep_a_bit()
        solution_link.click()
        headers = ["<th>{}</th>".format(text) for text
                   in ["Jel", "alsó határ", "felső határ", "valószínűség"]]
        self.assertAreInPage(headers)


if __name__ == "__main__":
    unittest.main(warnings="ignore")
