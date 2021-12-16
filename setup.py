import pathlib
import setuptools

here = pathlib.Path(__file__).parent.resolve()

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='jwtserver',
    version='0.0.3',
    author='Darkdeal',
    author_email='real@darkedal.net',
    description='jwt authorization server',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache2',
    url='https://github.com/darkdealnet/jwtserver',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: Apache Software License',
    ],
    packages=setuptools.find_packages(
        where='src',
        include=['jwtserver', 'jwtserver.*'],
        exclude=['jwtserver.tests']
    ),
    package_dir={'': 'src'},
    python_requires=">=3.10",
    install_requires=[
        'uvicorn==0.16.0',
        'loguru==0.5.3',
        'aioredis==2.0.0',
        'fastapi==0.70.1',
        'sqlalchemy==1.4.28',
        'sqlalchemy_utils==0.37.9',
        'asyncpg==0.25.0',
        'psycopg2-binary==2.9.2',
        'httpx==0.21.1',
        'phonenumbers==8.12.39',
        'python-jose==3.3.0',
        'passlib==1.7.4',
        'starlette~=0.16.0',
        'pydantic~=1.8.2',
    ],
    package_data={
        'jwtserver': ['default.ini'],
    },
)
