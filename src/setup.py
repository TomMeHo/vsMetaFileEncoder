import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name='vsmetaEncoder',
      version='0.1',
      description='A module to encode media information with Synology\'s vsmeta file format.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/TomMeHo/vsMetaFileEncoder',
      author='Thomas Meder',
      author_email='thomas@familie-meder.net',
      license='BSD',
      packages=['vsmetaEncoder'],
      packages=setuptools.find_packages(),
      zip_safe=False,
      install_requires=[
            'datetime >= 4.3'
      ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Logging"
      ],
      python_requires='>=3.6'
)