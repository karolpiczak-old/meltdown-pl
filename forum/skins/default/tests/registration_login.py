from selenium import selenium
import unittest, time, re
import random

class registration_login(unittest.TestCase):
    def setUp(self):
        rand_number = random.randrange(1, 10000)
        self.verificationErrors = []
        self.account_name = 'TestAccount%d' % rand_number
        self.account_email = 'test_account_%d@example.com' % rand_number
        self.selenium = selenium("localhost", 4444, "*chrome", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_registration_login(self):
        sel = self.selenium
        sel.open("/account/signin/")
        sel.click("link=Create account")
        sel.wait_for_page_to_load("30000")
        sel.type("id_username", "%s" % self.account_name)
        sel.type("id_email", "%s" % self.account_email)
        sel.type("id_password1", "test")
        sel.type("id_password2", "test")
        sel.click("bnewaccount")
        sel.wait_for_page_to_load("30000")
        sel.click("link=logout")
        sel.wait_for_page_to_load("30000")
        sel.click("btLogout")
        sel.wait_for_page_to_load("30000")
        sel.click("link=login")
        sel.wait_for_page_to_load("30000")
        sel.type("id_username", "%s" % self.account_name)
        sel.type("id_password", "test")
        sel.click("blogin")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_element_present("link=%s" % self.account_name))
        except AssertionError, e: self.verificationErrors.append(str(e))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
