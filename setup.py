from setuptools import setup

setup(
    name='app',
    version='0.1',  # Across config.py, app.py, ../setup.py
    description='simple-flask-api-with-sqlalchemy',
    author='Eric Dalrymmple',
    author_email='eric_dalrymple@apple.com',
    packages=['app'],
    include_package_data=True,  # needed for copying static files
    install_requires=open('requirements.txt').read().split(),
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
    ],
    license='MIT',
    python_requires='>=3.7',
    test_suite="tests.test_suite"
)
