import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../djtempl'))
import djtempl

class DjtemplRenderTests(unittest.TestCase):

    def test_djtempl_render_01(self):
        tfilename = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)),
            '../data/simplest.tmpl')

        expected = requirements_tuple = (
            "Django==1.8.3",
            "django-bootstrap3==6.1.0",
            "django-lazysignup==1.0.1",
            "django-registration-redux==1.2",
            "Djangorestframework==3.2.3",
            "django-redis-sessions==0.5.0",
            "huey==0.4.9"
        )

        template_context = {'pip_requirements': requirements_tuple}
        rendered = djtempl.djtempl_render(tfilename, template_context).encode('utf-8','ignore')

        actual = tuple(rendered.splitlines())
        self.assertEqual(actual, expected)


    def test_django_render_unescaping(self):
        """
        The django template renderer html escapes things like <= and >=
        Make sure that they are coming out of the rendering unescaped.
        """
        tfilename = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)),
            '../data/simplest.tmpl')

        expected = requirements_tuple = (
            "Django>=1.8.3",
            "django-bootstrap3>=6.1.0",
            "django-lazysignup<=1.0.1",
            "django-registration-redux<=1.2",
            "Djangorestframework=>3.2.3",
            "django-redis-sessions<=0.5.0",
            "huey==0.4.9"
        )

        template_context = {'pip_requirements': requirements_tuple}
        rendered = djtempl.djtempl_render(tfilename, template_context).encode('utf-8','ignore')

        actual = tuple(rendered.splitlines())
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
