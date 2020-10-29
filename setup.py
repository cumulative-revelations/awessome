from setuptools import setup, find_packages

PACKAGE_NAME = "awessome"
#version_meta = runpy.run_path("./version.py")
#VERSION = version_meta["__version__"]

classifiers = ['Development Status :: 4 - Beta', 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: MIT License', 'Natural Language :: English',
                 'Programming Language :: Python :: 3.5', 'Topic :: Scientific/Engineering :: Artificial Intelligence',
                 'Topic :: Scientific/Engineering :: Information Analysis', 'Topic :: Text Processing :: Linguistic',
                 'Topic :: Text Processing :: General']

def parse_requirements(filename):
        """Load requirements from a pip requirements file."""
        lineiter = (line.strip() for line in open(filename))
        return [line for line in lineiter if line and not line.startswith("#")]


setup(
  name=PACKAGE_NAME,
  version='0.0.1',
  description='awessome',
  include_package_data=True,
  install_requires=parse_requirements("requirements.txt"),
  long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/cumulative-revelations/awessome',  
  author='Amal Htait and Leif Azzopardi',
  author_email='amal.htait@strath.ac.uk, leif.azzopardi@strath.ac.uk',
  license='MIT', 
  classifiers=classifiers,
  keywords=['awessome', 'sentiment', 'analysis', 'opinion', 'mining', 'nlp', 'text', 'data',
            'text analysis', 'opinion analysis', 'sentiment analysis', 'text mining', 'twitter sentiment',
            'opinion mining', 'social media', 'twitter', 'social', 'media'], 
  packages=find_packages()
)
