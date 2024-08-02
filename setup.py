from setuptools import setup, find_packages

setup(
    name='pystickyn',
    version='0.2.0',
    author='Samuel Alexander Rodriguez',
    author_email='samlexrod@outlook.com',
    description='A package to organize your thoughts in sticky notes in a Jupyter Notebook.',
    long_description='''Your Package Name is a Python package that provides a convenient way to organize your thoughts using sticky notes within a Jupyter Notebook. It offers various types of sticky notes, such as completed, working, todo, failed, validating, and warning notes, each with customizable options and the ability to include code snippets.
    For detailed documentation and usage examples, please visit the project repository on GitHub: https://github.com/samlexrod/pystickyn''',
    url='https://github.com/samlexrod/pystickyn',
    packages=find_packages(),
    install_requires=[
        'pygments>=2.18.0',
        'ipython>=8.26.0',
        'ipywidgets>=8.1.3',
        'markdown2>=2.4.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
