import os
import json
import unittest
import sys
sys.path.append('../')
from app import create_app
from manage import destroy_tables, create_tables
from unittest import TestCase
from .helper_data import *
from .helper_methods import *

class BaseTestCase(TestCase):
        """ Base Tests """
        def setUp(self):
                self.app = create_app(config_name='testing')
                # self.app_context = self.app.app_context()
                # self.app_context.push()
                self.client = self.app.test_client(use_cookies=True)
                with self.app.app_context():
                        create_tables()
        
    
        def teardown(self):
                with self.app.app_context():
                        destroy_tables()


# Make the tests conveniently executable
if __name__ == "__main__":
        unittest.main()