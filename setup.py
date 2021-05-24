from setuptools import find_packages, setup

with open('.version') as version_file:
    version = version_file.read()

setup(
    name='stock-prediction',
    version=version,
    description='This project is stock prediction service',
    author='Sungoh Kim',
    author_email='sungoh5.kim@g.skku.edu',
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=[
        'Flask==2.0.1',
        'gunicorn==20.1.0',
        'gevent==21.1.2'
        ],
    include_package_data=True
)
