from setuptools import setup

setup(
    name='reggie-dsl',
    version='0.1a5',
    packages=['reggie', 'examples'],
    url='https://github.com/romilly/reggie',
    license='MIT',
    author='romilly',
    author_email='romilly.cocking@gmail.com',
    description='Python DSL for Regular Expressions',
    long_description='reggie-dsl lets Python developers create regular expressions that are readable and easy to use.',
    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6', ],
)
