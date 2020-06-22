from selenium import webdriver
from django.urls import resolve
import unittest
#from cv.views import cv  

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        #self.browser.get('http://127.0.0.1:8000')
    def tearDown(self):
        self.browser.quit()

    def test_cv(self):
        self.browser.get('http://127.0.0.1:8000/cv')

        self.assertIn("CV", self.browser.title)

        # name should be Ivan Tsoninski and it should be in details section with h2
        cv_name = 
            self
            .browser
            .find_element_by_class_name('details')
            .find_elements_by_tag_name('h2')
            .text

        self.assertIn('Ivan Tsoninski', cv_name)

        # details should be seen
        # details must include telephone, emails, github, itch
        details = self.browser.find_element_by_class_name('details')
        self.assertIn('Telephone', details)
        self.assertIn('Email', details)
        self.assertIn('Github', details)
        self.assertIn('Itch', details)

        

        # categories can be seen: Profile, Education, Technical Skills, Experience
        cats = [h.text for h in self.browser.find_elements_by_tag_name('h2')][1:]
        self.assertEquals(cats, ['Profile', 'Education', 'Technical Skills', 'Experience'])

        


if __name__ == "__main__":
    unittest.main(warnings='ignore')