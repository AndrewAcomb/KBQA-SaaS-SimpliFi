from setuptools import setup, find_packages

requires = [
'flask',
'flask-cors',
'FlaskPusher'
]

setup(
    name='kbqa-saas-flask',
    version='0.0',
    description='Comp finder website using api',
    author='<Your actual name here>',
    author_email='<Your actual e-mail address here>',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)