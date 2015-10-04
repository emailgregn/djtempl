import unittest
import os
import tempfile
import subprocess

class CommandLineTests(unittest.TestCase):

    def test_commandline_allargs(self):
        expected = """
FROM python:2.7-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /src
WORKDIR /src
RUN pip install --upgrade pip

# Start Template generated

RUN pip install --upgrade Django>=1.8.3
RUN pip install --upgrade django-bootstrap3==6.1.0
RUN pip install --upgrade django-lazysignup==1.0.1
RUN pip install --upgrade django-registration-redux==1.2
RUN pip install --upgrade Djangorestframework==3.2.3
RUN pip install --upgrade django-redis-sessions==0.5.0
RUN pip install --upgrade huey==0.4.9
# End Template generated
""".splitlines()
        with tempfile.NamedTemporaryFile(mode='rw') as tmpFile:
            args = [
                'djtempl',
                '-t',   '../tests/data/Dockerfile.tmpl',
                '-p',   '../tests/data/requirements.txt',
                '-d',   tmpFile.name,
                '-q'
            ]

            cwd = os.path.join(os.path.dirname(__file__), '../../djtempl')
            subprocess.call(args=args, cwd=cwd)

            tmpFile.seek(0)

            actual = tmpFile.read().splitlines()

        self.maxDiff = None
        self.assertEqual(actual, expected)




if __name__ == '__main__':
    unittest.main()