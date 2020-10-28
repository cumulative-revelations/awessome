from setuptools import setup, find_packages
 
classifiers = ['Development Status :: 4 - Beta', 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: MIT License', 'Natural Language :: English',
                 'Programming Language :: Python :: 3.5', 'Topic :: Scientific/Engineering :: Artificial Intelligence',
                 'Topic :: Scientific/Engineering :: Information Analysis', 'Topic :: Text Processing :: Linguistic',
                 'Topic :: Text Processing :: General']
 
setup(
  name='awessome',
  version='0.0.1',
  description='awessome',
  include_package_data=True,
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Amal Htait and Leif Azzopardi',
  author_email='amal.htait@strath.ac.uk, leif.azzopardi@strath.ac.uk',
  license='MIT', 
  classifiers=classifiers,
  keywords=['awessome', 'sentiment', 'analysis', 'opinion', 'mining', 'nlp', 'text', 'data',
            'text analysis', 'opinion analysis', 'sentiment analysis', 'text mining', 'twitter sentiment',
            'opinion mining', 'social media', 'twitter', 'social', 'media'], 
  packages=find_packages(),
  install_requires=[''] 
)