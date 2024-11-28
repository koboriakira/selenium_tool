from setuptools import setup, find_packages

setup(
    name="selenium_tool",
    version='1.0',
    description='',
    author='',
    author_email='',
    url='https://github.com/koboriakira/selenium_tool',
    packages=find_packages(),
    entry_points="""
      [console_scripts]
      selenium_tool = selenium_tool.cli:execute
    """,
    install_requires=open('requirements.txt').read().splitlines(),
    # license='MIT',
)
