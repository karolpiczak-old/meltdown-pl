from selenium import selenium
import unittest, time, re

class faq_page(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_faq_page(self):
        sel = self.selenium
        sel.open("/faq/")
        try: self.failUnless(sel.is_text_present("FAQ"))
        except AssertionError, e: self.verificationErrors.append(str(e))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
