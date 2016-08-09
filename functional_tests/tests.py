from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
import sys
class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url='http://'+arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url=cls.live_server_url
    @classmethod
    def tearDownClass(cls):
        if cls.server_url==cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser=webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self,row_text):
        table=self.browser.find_element_by_id('id_list_table')
        rows=table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in rows])


    def test_can_start_a_list_and_retrive_it_later(self):
        '''
        Edith has heard about a cool new online to-do app.She goes
        to check out its homepage
        '''
        self.browser.get(self.server_url)

        #she notices the page title and header mention to-do lists
        self.assertIn('To-Do',self.browser.title)
        header_text=self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)

        # she is invited to enter a to-do item straight away

        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        #She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures )
        inputbox.send_keys('Buy peacock feathers')

        #When she hits enter, the page updates, and now the page lists
        #"1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        edith_list_url=self.browser.current_url
        self.assertRegex(edith_list_url,'/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        #There is still a text box inviting her to add another item. She
        #enters "Use peacock feathers to make a fly" (Edith is very methodical)
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        #The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        time.sleep(2)
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        #Now a new user, Francis, comes along to the site.

        #We use a new browser session to make sure that no information
        ##of Edith's is coming through from cookies etc
        self.browser.quit()
        time.sleep(2)
        self.browser=webdriver.Firefox()
        self.browser.get(self.server_url)
        #Francis starts a new list by enteriing a new iitem. He
        #is less interesting than Edith..

        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)

        #francis gets his own unique URL
        francis_list_url=self.browser.current_url
        self.assertRegex(francis_list_url,'/lists/.+')
        self.assertNotEqual(francis_list_url,edith_list_url)

        #Again,there is no trace of Ediith's List
        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertIn('Buy milk',page_text)

        #Satisfied, they both go back to sleep


    def test_layout_and_styling(self):
        #Edith goes to the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024,768)

        #She notices the box is nicely centered
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            delta=5
        )
        #she starts a new list and sees the input is nicely
        #centered there too
        inputbox.send_keys('testing\n')
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            delta=5
        )