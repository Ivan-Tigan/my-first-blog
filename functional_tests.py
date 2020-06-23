from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from django.urls import resolve
import unittest
#from cv.views import cv  
import random
import string
import time 

def random_string():
    return ''.join(random.choice(string.ascii_letters) for i in range(30))

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        #self.browser.get('http://127.0.0.1:8000')
    def tearDown(self):
        self.browser.quit()

    def test_CV_unauthenticated(self):

        self.browser.delete_all_cookies()
        self.browser.get('http://127.0.0.1:8000/cv')

        self.assertIn("CV", self.browser.title)

        # name should be Ivan Tsoninski and it should be in details section with h2
        cv_name = self.browser.find_element_by_class_name('details').find_element_by_tag_name('h2').text

        self.assertIn('Ivan Tsoninski', cv_name)

        # details should be seen
        # details must include telephone, emails, github, itch
        details = self.browser.find_element_by_class_name('details').text
        self.assertIn('Telephone', details)
        self.assertIn('Email', details)
        self.assertIn('Github', details)
        self.assertIn('Itch', details)

        # categories can be seen: Profile, Education, Technical Skills, Experience
        cats = [h.text for h in self.browser.find_elements_by_tag_name('h2')][1:]
        self.assertEquals(cats, ['Profile', 'Education', 'Technical Skills', 'Experience'])

        # there should be no button to edit because you are unauthenticated
        self.assertRaises(NoSuchElementException, lambda: self.browser.find_element_by_class_name('edit_button'))


    def test_CV_edit_unauthenticated(self):

        self.browser.delete_all_cookies()
        self.browser.get('http://127.0.0.1:8000/cv/edit')
        
        # Tab title should be Edit CV.
        self.assertIn("Edit CV", self.browser.title)
        
        # Edit CV should be displayed at the top of the page.
        self.assertIn("Edit CV", self.browser.find_element_by_tag_name('h2').text)

        # If you are not authenticated you should see:
        
        # You are not authenticated so you cannot make and save changes to this CV.
        self.assertIn('You are not authenticated so you cannot make and save changes to this CV.', self.browser.find_element_by_tag_name('body').text)

        # And there should be no save button.
        self.assertEqual(
            [], 
            [ b for b in self.browser.find_elements_by_tag_name('button') if b.text == 'Save']
            )

        # You should still see the CV categories
        cats = [l.text for l in self.browser.find_elements_by_tag_name('label')] 
        for c in cats:
            self.assertIn(c, ['Experience:', 'Education:', 'Technical skills:', 'Details:', 'Profile:'])
        
        # You should be able to edit the text (no saving here)
        text_areas = self.browser.find_elements_by_tag_name('textarea')
        for ta in text_areas:
            text_to_enter = random_string()
            ta.send_keys(text_to_enter)

    
    def test_CV_edit_authenticated(self):

        self.browser.delete_all_cookies()
        self.browser.get('http://127.0.0.1:8000/admin')

        username = "vankata"
        password = "Ivano6ka"
        
        # authenticate  
        field_username = self.browser.find_element_by_xpath('//input[@name="username"]')
        field_username.send_keys(username)
        
        field_password = self.browser.find_element_by_xpath('//input[@name="password"]')
        field_password.send_keys(password)

        self.browser.find_element_by_xpath('//input[@type="submit"]').click()

        # now go to cv page
        self.browser.get('http://127.0.0.1:8000/cv/')

        # there should be a button to edit
        edit_btn = self.browser.find_element_by_class_name('edit_button').find_element_by_tag_name('a')
        self.assertIsNotNone(edit_btn)

        # click to go to edit and wait
        edit_btn.click()
        time.sleep(2)
        # should be in cv edit mode
        self.assertIn('cv/edit', self.browser.current_url)

        # Tab title should be Edit CV.
        self.assertIn("Edit CV", self.browser.title)
        
        # Edit CV should be displayed at the top of the page.
        self.assertIn("Edit CV", self.browser.find_element_by_tag_name('h2').text)

        # You are authenticated so you should not see a message that says otherwise.
        self.assertNotIn('You are not authenticated so you cannot make and save changes to this CV.', self.browser.find_element_by_tag_name('body').text)

        # And there should be a save button.
        save_btn =  [ b for b in self.browser.find_elements_by_tag_name('button') if b.text == 'Save'][0]
        self.assertIsNotNone(save_btn)

        # You should still see the CV categories
        cats = [l.text for l in self.browser.find_elements_by_tag_name('label')] 
        for c in cats:
            self.assertIn(c, ['Experience:', 'Education:', 'Technical skills:', 'Details:', 'Profile:'])
        
        # You should be able to edit the text 
        text_areas = self.browser.find_elements_by_tag_name('textarea')
        text_to_enter = [random_string() for i in range(len(text_areas))]
        for ta, te in zip(text_areas, text_to_enter):
            ta.send_keys(te)

        # you should be able to save your edits and go to the main cv view
        save_btn.click()
        time.sleep(2)
        self.assertNotIn("cv/edit", self.browser.current_url)
        self.assertIn("cv", self.browser.current_url)

        # you should be able to find the texts you entered in the edit page
        for t in text_to_enter:
            self.assertIn(t, self.browser.find_element_by_tag_name('body').text)


if __name__ == "__main__":
    unittest.main(warnings='ignore')