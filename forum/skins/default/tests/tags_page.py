from selenium import selenium
import unittest, time, re

class tags_page(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_tags_page(self):
        sel = self.selenium
        sel.open("/")
        sel.click("nav_tags")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("Tag list"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("by name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("by popularity"))
        except AssertionError, e: self.verificationErrors.append(str(e))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
