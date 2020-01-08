import setuptools


with open('README.md', 'r') as source:
    long_description = source.read()

setuptools.setup(
    name='python-smsprosto',
    version='0.0.1',
    author="Adam Lavrik",
    author_email="lavrik.adam@gmail.com",
    description="A simple Python 2 and 3 client for Russian SMS API service \"Prosto SMS\" (https://sms-prosto.ru)",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/adam-lavrik/python-smsprosto',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache 2.0 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
    install_requires=['requests>=2.0']
)
