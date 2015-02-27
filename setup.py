from distutils.core import setup
from distutils.sysconfig import *
from distutils.util import *

from phylorelief import __version__
        
try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

# setup arguments
packages=['phylorelief']
scripts = ["scripts/phylorelief"]

data_files = []
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent'
    ]
                 
setup(name = 'phylorelief',
      version=__version__,
      description='phylogenetic-based relief',
      long_description=open('README.rst').read(),
      author='Davide Albanese',
      author_email='davide.albanese@fmach.it',
      maintainer='Davide Albanese',
      maintainer_email='davide.albanese@fmach.it',
      url='',
      download_url='',
      license='GPLv3',
      packages=packages,
      scripts=scripts,
      data_files=data_files,
      classifiers=classifiers
    )
