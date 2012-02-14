#!/usr/bin/env python
import sys, os, subprocess

def bootstrap(path, distribute=True):
    virtualenv = os.path.dirname(sys.argv[0])
    if distribute:
        return subprocess.call([os.path.join(virtualenv, '..',
                                             'virtualenv', 'virtualenv.py'),
                                '--distribute',
                                path])
    else:
        return subprocess.call([os.path.join(virtualenv, '..',
                                             'virtualenv', 'virtualenv.py'),
                                '--setuptools',
                                path])

def build_from_requirements(path, pypi_server=None,
                            mirrors=True, requirements=None):
    pip = os.path.join(path, 'bin', 'pip')
    if not requirements:
        requirements = os.path.join(os.getcwd(), "requirements.txt")
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
        return build_from_requirements(path)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print "python build.py install_path"
