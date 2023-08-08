from setuptools import setup, find_packages

setup(
    name="tjpw_schedule",
    version='1.0',
    description='',
    author='',
    author_email='',
    url='https://github.com/koboriakira/tjpw_schedule',
    packages=find_packages(),
    entry_points="""
      [console_scripts]
      tjpw_schedule = tjpw_schedule.cli:execute
    """,
    install_requires=open('requirements.txt').read().splitlines(),
    # license='MIT',
)
