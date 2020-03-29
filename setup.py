from setuptools import setup, find_packages




with open('requirements.txt') as f:
    DEPENDENCIES = f.read().splitlines()


setup(name='graphaite',
      version='0.0.3',
      description="vizAI",
      license='',
      packages=find_packages(),
      zip_safe=False,
      install_requires=DEPENDENCIES
      )
