"""
Renders a Dockerfile template with pip install commands from requirements.txt

ToDo: better --help handling
    http://stackoverflow.com/questions/8236954/specifying-default-filenames-with-argparse-but-not-opening-them-on-help#8239911
"""
import sys
import os

from django.conf import settings
from django.template.loader import render_to_string
from django.template import Context
from pip.download import PipSession
from pip.req.req_file import parse_requirements
import HTMLParser


def djtempl_render(template_absolute_name, template_context):
    """
    Args:
    template_absolute_name: string - the full qualified filename of the file to be rendered by with the django template engine
    template_context: dict - the variables to be rendered into the template

    Returns:
    A string of the rendered template

    """

    try:
        settings.configure()
    except Exception, e:
        pass

    # docs say not to do this but...
    settings.TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.dirname(template_absolute_name)],
        }
    ]
#    django.setup()

    h = HTMLParser.HTMLParser()
    template_name = os.path.basename(template_absolute_name)
    return h.unescape(
        render_to_string(template_name, context=Context(template_context))
    )


def get_requirements(pfile):
    """
    Ask pip to parse it's own requirements file to handle comments, line continuations, nested files etc.

    :param
        pfile: an open file handle
    :return
        a tuple of requirements
    """
    pipSession = PipSession()
    pip_gen = parse_requirements(pfile.name, session=pipSession)
    requirements_tuple = tuple(str(x.req) for x in pip_gen)
    return requirements_tuple


def render_files(pip_file, template_file, docker_file, quiet):

    if not quiet and docker_file.name != '<stdout>':
        if os.path.isfile(docker_file.name):
            print 'File %s already exists' % docker_file.name
            sys.exit(-1)

    requirements_tuple = get_requirements(pip_file)

    template_context = {'pip_requirements': requirements_tuple}

    rendered = djtempl_render(template_file.name, template_context).encode('utf-8','ignore')

    docker_file.write( rendered)
    docker_file.close()
