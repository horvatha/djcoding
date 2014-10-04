#!/usr/bin/env python3
# coding: utf-8

"""functional_test for Test Driven Program Development by Harry Percival
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


class NewVisitorTest(MyLiveServerTestCase):
    """TestGroup"""

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.server_url = self.live_server_url

    def tearDown(self):
        self.browser.quit()

    def test_surfing_on_the_page(self):
        self.browser.get(self.server_url + '/sources/')
        # self.browser.get("http://django.arek.uni-obuda.hu/django/sources")
        self.browser.set_window_size(1024, 700)

        self.assertIn('Források elemzése', self.browser.title)

        firstitem = self.browser.find_element_by_id("id_item1")
        sleep_a_bit()
        firstitem.click()

        default_href = self.browser.find_element_by_id("id_link1")
        self.assertIn("A:00 B:01 C:10 D:11", default_href.text)

        appearing_texts = ['<th>Kód', 'üzenet']
        disappearing_texts = ['A:00 B:01 C:10 D:11']
        self.assertAreNotInPage(appearing_texts)

        sleep_a_bit()
        default_href.click()

        self.assertAreInPage(appearing_texts)
        self.assertAreNotInPage(disappearing_texts)

        appearing_texts = ["djangoproject.com", "webkeretrendszer", "github"]
        self.assertAreNotInPage(appearing_texts)

        about_link = self.browser.find_element_by_partial_link_text("oldalról")
        sleep_a_bit()
        about_link.click()

        self.assertAreInPage(appearing_texts)

        appearing_texts = ["mailto", "elerhetoseg.htm", "írja"]
        self.assertAreNotInPage(appearing_texts)

        about_link = self.browser.find_element_by_partial_link_text("Kapcsolat")
        sleep_a_bit()
        about_link.click()

        appearing_texts = ["Eltérő valószínűségű jelekből", "Kenobi"]
        self.assertAreNotInPage(appearing_texts)

        home_link = self.browser.find_element_by_link_text("Főoldal")
        sleep_a_bit()
        home_link.click()

        self.assertAreInPage(appearing_texts)

        kenobi_source_link = \
            self.browser.find_element_by_partial_link_text("Kenobi")
        sleep_a_bit()
        kenobi_source_link.click()

        kenobi_code_link = \
            self.browser.find_element_by_partial_link_text("D:000101")
        sleep_a_bit()
        kenobi_code_link.click()

        kenobi_chain_link = \
            self.browser.find_element_by_partial_link_text("lánc")

        appearing_texts = ["hibamentes"]
        self.assertAreNotInPage(appearing_texts)

        sleep_a_bit()
        kenobi_chain_link.click()

        self.assertAreInPage(appearing_texts + ["<table"])

        self.assertIn("sources/3/1/0/", self.browser.current_url)

        # TODO see the test below
        # chain_with_error = \
        #     self.browser.find_element_by_partial_link_text(
        #         "Fix forrás és hibás csatorna")

        # appearing_texts = [
        #     '<tr><td>10</td><td><span class="match">I_LOVE_</span>',
        #     '<tr><td>32</td><td><span class="match">0000',
        # ]
        # self.assertAreNotInPage(appearing_texts)

        # chain_with_error.click()

        # self.assertAreInPage(appearing_texts)

        chain_with_error_correction = \
            self.browser.find_element_by_partial_link_text("hibajavítás")

        chain_with_error_correction.click()

    # TODO It works in a way I can not recreate manually
    def test_visitor_can_click_on_source_with_error_button(self):
        self.browser.get(self.server_url + '/sources/3/1/0/')
        chain_with_error = \
            self.browser.find_element_by_partial_link_text(
                "Fix forrás és hibás csatorna")

        appearing_texts = [
            '<tr><td>10</td><td><span class="match">I_LOVE_</span>',
            '<tr><td>32</td><td><span class="match">0000',
        ]
        self.assertAreNotInPage(appearing_texts)

        chain_with_error.click()

        self.assertAreInPage(appearing_texts)

    def test_layout_and_styling(self):
        self.browser.get(self.server_url + "/sources/")
        width, height = 1024, 768
        self.browser.set_window_size(width, height)

        main_div = self.browser.find_element_by_class_name('jumbotron')
        self.assertAlmostEqual(
            main_div.location['x'] + main_div.size['width']/2,
            width/2,
            delta=2
        )


class ChangeChainTest(MyLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.server_url = self.live_server_url
        self.browser.get(self.server_url + '/sources/1/1/0/')

    def tearDown(self):
        self.browser.quit()

    def test_visitor_can_change_channel(self):
        self.assertAreInPage(["A:1/4 B:1/4 C:1/4 D:1/4", "hibamentes csatorna"])
        inputbox = self.browser.find_element_by_id('id_channel_change')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         "Változtatáshoz csatornaleíró és Újsor.")
        inputbox.send_keys('8\n')
        self.assertAreInPage(["8 hibával"])

    def test_visitor_can_change_source(self):
        inputbox = self.browser.find_element_by_id('id_source_change')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         "Változtatáshoz forrásleíró és Újsor.")
        inputbox.send_keys('A:1/2 B:1/4 C:1/8 D:1/8\n')
        self.assertAreInPage(["A:1/2 B:1/4 C:1/8 D:1/8"])


if __name__ == "__main__":
    unittest.main(warnings="ignore")
