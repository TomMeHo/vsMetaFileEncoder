import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
      name='vsmetaCodec',
      version='1.1.1',
      description='A module to encode and decode media information with Synology\'s vsmeta file format.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/berfre/vsMetaFileCodec',
      author='Thomas Meder',
      author_email='tom@tommho.net',
      license='BSD',
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
      python_requires='>=3.8'
)
