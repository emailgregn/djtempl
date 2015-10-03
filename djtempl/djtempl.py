"""
Renders a Dockerfile template with pip install commands from requirements.txt

ToDo: better --help handling
    http://stackoverflow.com/questions/8236954/specifying-default-filenames-with-argparse-but-not-opening-them-on-help#8239911
"""
import sys
import os
import django
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


def main(argv):
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--template",
                        metavar='file',
                        default='Dockerfile.tmpl',
                        type=argparse.FileType(mode='r'), # 2.7 argparse.FileType() doesn't support encoding=
                        help="The dockerfile template to render")

    parser.add_argument("-p", "--pip",
                        metavar='file',
                        default='requirements.txt',
                        type=argparse.FileType(mode='r'),
                        help="The pip requirements file")

    parser.add_argument("-d", "--dockerfile",
                        metavar='file',
                        default=sys.stdout,
                        type=argparse.FileType(mode='w'),
                        help="The output dockerfile. Default is STDOUT")

    parser.add_argument("-q", "--quiet",
                        action="store_true",
                        help="Silently overwrite if Dockerfile already exists")

    args = parser.parse_args()

    dfile = args.dockerfile
    pfile = args.pip
    tfile = args.template

    if not args.quiet and dfile.name != '<stdout>':
        if os.path.isfile(dfile.name):
            print 'File %s already exists' % dfile.name
            sys.exit(-1)

    requirements_tuple = get_requirements(pfile)

    template_context = {'pip_requirements': requirements_tuple}

    rendered = djtempl_render(tfile.name, template_context).encode('utf-8','ignore')

    dfile.write( rendered)
    dfile.close()

if __name__ == "__main__":
    main(sys.argv[1:])

