from setuptools import setup

setup(
    name = 'zk',
    version = '0.1',
    py_modules = ['zk'],
    install_requires = [
        'click',
    ],
    entry_points = '''
        [console_scripts]
        zk=zk:cli
    '''
)
