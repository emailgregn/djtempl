from djtempl import render_files
import argparse
import sys

def main():
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
    quiet = args.quiet

    render_files(pfile, tfile, dfile, quiet)
