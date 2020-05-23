from selenium import webdriver
from django.urls import resolve
import unittest
from cv.views import cv  

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        #self.browser.get('http://127.0.0.1:8000')
    def tearDown(self):
        self.browser.quit()

    def test_cv(self):
        self.browser.get('http://127.0.0.1:8000/cv')
        #resolve('/cv')
        self.assertIn("CV", self.browser.title)

if __name__ == "__main__":
    unittest.main(warnings='ignore')