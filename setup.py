from distutils.core import setup
setup(
    name = 'antolib',
    packages = ['antolib'],
    install_requires=[
          'paho-mqtt',
    ],
    version = '0.1.1',
    description = 'Python Library for using anto.',
    author = 'AntoIO',
    author_email = 'isaradream@gmail.com',
    keywords = ['anto', 'iot', 'platform', 'mqtt'],
    classifiers = [
      'Topic :: Education',
      'Topic :: Utilities'
      ],
)
