#!/usr/bin/env python
import sys, subprocess
from os.path import join, dirname
from os import getcwd

virtualenv = join('.', dirname(sys.argv[0]),
                  '..', 'virtualenv', 'virtualenv.py')
    

def bootstrap(path, distribute=True):
    if distribute:
        return subprocess.call([virtualenv, '--distribute', path])
    else:
        return subprocess.call([virtualenv, '--setuptools', path])

def make_relocatable(path):
    return subprocess.call([virtualenv, '--relocatable', path])


def build_from_requirements(path, pypi_server=None,
                            mirrors=True, requirements=None):
    pip = join(path, 'bin', 'pip')
    if not requirements:
        requirements = join(getcwd(), "requirements.txt")
    if pypi_server and not mirrors:
        return subprocess.call([pip, 'install', '-i %s' % pypi_server,
                                '-r', '%s' % requirements])
    elif not pypi_server and mirrors:
        return subprocess.call([pip, 'install', '--use-mirrors',
                                '-r', '%s' % requirements])
    elif not pypi_server and not mirrors:
        return subprocess.call([pip, 'install', '-r', '%s' % requirements])
    else:
        print "pypi_server and mirrors options can't both be enabled"

def main(path):
    if bootstrap(path) == 0:
        build_from_requirements(path)
        make_relocatable(path)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print "python build.py install_path"
