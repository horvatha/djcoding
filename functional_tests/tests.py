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


class NewVisitorTest(LiveServerTestCase):
    """TestGroup"""

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_sources(self):
        self.browser.get(self.live_server_url + '/sources/')
        self.assertIn('Források elemzése', self.browser.title)
        firstitem = self.browser.find_element_by_id("id_item1")
        firstitem.click()
        default_href = self.browser.find_element_by_id("id_link1")
        self.assertIn("A:00 B:01 C:10 D:11", default_href.text)

        # The button is large enought to click it easily.
        # self.assertGreater(default_href.size['height'], 99)

        self.assertAreNotInPage(['<th>Kód', 'üzenet'])
        default_href.click()

        self.assertAreInPage(['<th>Kód', 'üzenet'])
        self.assertNotIn("A:00 B:01 C:10 D:11", self.browser.page_source)

        # edit_code_href = self.browser.find_element_by_id("edit_code")
        # edit_code_href.click()

        # # TODO edit the codes
        # back_href = self.browser.find_element_by_id("go_back")
        # back_href.click()
        # sleep_a_bit()

        self.fail("Finish the test!")

    def assertAreNotInPage(self, text_list):
        for text in text_list:
            self.assertNotIn(text, self.browser.page_source)

    def assertAreInPage(self, text_list):
        for text in text_list:
            self.assertIn(text, self.browser.page_source)

    # def test_can_start_a_list_and_retrieve_it_later(self):
    #     self.browser.get(self.live_server_url)
    #     self.assertIn('To-Do', self.browser.title)
    #     header_text = self.browser.find_element_by_tag_name('h1').text
    #     self.assertIn('To-Do', header_text)
    #     inputbox = self.browser.find_element_by_id('id_new_item')
    #     self.assertEqual(inputbox.get_attribute('placeholder'),
    #                      'Enter a to-do item')
    #     sleep_a_bit()
    #     inputbox.send_keys('Repair the bicycle')
    #     inputbox.send_keys(Keys.ENTER)
    #     sleep_a_bit()
    #     edith_list_url = self.browser.current_url
    #     self.assertRegex(edith_list_url, '/lists/.+')
    #     self.check_for_row_in_list_table('1: Repair the bicycle')

    #     inputbox = self.browser.find_element_by_id('id_new_item')
    #     self.assertEqual(inputbox.get_attribute('placeholder'),
    #                      'Enter a to-do item')
    #     sleep_a_bit()
    #     inputbox.send_keys('Take a bicycle tour')
    #     sleep_a_bit()
    #     inputbox.send_keys(Keys.ENTER)
    #     sleep_a_bit()
    #     for row_text in ('1: Repair the bicycle', '2: Take a bicycle tour'):
    #         self.check_for_row_in_list_table(row_text)

    #     # A new user Francis comes along the site
    #     self.browser.quit()
    #     ## We use a new browser session to make sure there is no
    #     ## trace of Edith's through cokies or etc
    #     self.browser = webdriver.Firefox()

    #     # Francis visits the home page
    #     # There is no sign of Edith's list
    #     self.browser.get(self.live_server_url)
    #     page_text = self.browser.find_element_by_tag_name('body').text
    #     self.assertNotIn('Repair the bicycle', page_text)
    #     self.assertNotIn('bicycle', page_text)

    #     # Francis starts a new list
    #     # There is no sign of Edith's list
    #     inputbox = self.browser.find_element_by_id('id_new_item')
    #     inputbox.send_keys('Buy milk')
    #     inputbox.send_keys(Keys.ENTER)
    #     francis_list_url = self.browser.current_url
    #     self.assertRegex(francis_list_url, '/lists/.+')
    #     sleep_a_bit()
    #     self.assertNotEqual(francis_list_url, edith_list_url)
    #     self.check_for_row_in_list_table('1: Buy milk')

    #     # Again there is no trace of Edith's list
    #     page_text = self.browser.find_element_by_tag_name('body').text
    #     self.assertNotIn('Repair the bicycle', page_text)
    #     self.assertIn('Buy milk', page_text)

    # def check_for_row_in_list_table(self, row_text):
    #     table = self.browser.find_element_by_id('id_list_table')
    #     rows = table.find_elements_by_tag_name('tr')
    #     self.assertIn(row_text, [row.text for row in rows])

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url + "/sources/")
        width, height = 1024, 768
        self.browser.set_window_size(width, height)

        main_div = self.browser.find_element_by_class_name('jumbotron')
        self.assertAlmostEqual(
            main_div.location['x'] + main_div.size['width']/2,
            width/2,
            delta=2
        )

if __name__ == "__main__":
    unittest.main(warnings="ignore")
