import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../djtempl'))
import djtempl

class PipRequirementsTests(unittest.TestCase):

    def test_pip_requirements_01(self):

        # expected is ../data/requirements.txt without the comments and stuff
        expected = ("Django>=1.8.3",
                    "django-bootstrap3==6.1.0",
                    "django-lazysignup==1.0.1",
                    "django-registration-redux==1.2",
                    "Djangorestframework==3.2.3",
                    "django-redis-sessions==0.5.0",
                    "huey==0.4.9"
                    )
        rfilename = os.path.join(os.path.dirname(__file__), '../data/requirements.txt')
        with open(rfilename, 'r') as pfile:
            actual = djtempl.get_requirements(pfile)

        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
