from distutils.core import setup
setup(
  name = 'btrdbutil',
  packages = ['btrdbutil'],
  version = '0.1',
  install_requires = ['btrdb'],
  description = 'Python bindings for multi-resolution retrieval from BTrDB',
  author = 'Omid Ardakanian',
  author_email = 'ardakanian@berkeley.edu',
  url = 'https://github.com/SoftwareDefinedBuildings/uPMU-tools',
  keywords = ['BTrDB', 'timeseries', 'search'],
  classifiers = [],
)
