from setuptools import setup

setup(
    name='pysintegrabanco',
    version='0.0.2',
    description='Leitura de arquivos bancarios, francesinhas, .TXT ou .RET',
    url='https://github.com/rfschubert/pys-integrabanco',
    author='Raphael Schubert',
    author_email='rfswdp@gmail.com',
    license='GNU',
    packages=['pysintegrabanco'],
    keywords=['python integra banco', 'python3', 'santander', 'schubert'],
    install_requires=[
        'pendulum'
    ],
    zip_safe=False
)