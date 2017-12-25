from setuptools import setup

setup(name='transithelper',
      version='0.1',
      description='Shared lib for transit devices',
      author='Yan Zhan',
      packages=['transithelper'],
      zip_safe=False,
      install_requires=[
            'flask', 'requests'
      ])
