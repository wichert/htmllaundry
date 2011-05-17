from setuptools import setup, find_packages

version = "1.10"

setup(name="htmllaundry",
      version=version,
      description="Simple HTML cleanup utilities",
      long_description=open("README.rst").read()+"\n\n"+
                       open("CHANGES.rst").read(),
      classifiers=[
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.4",
          "Programming Language :: Python :: 2.5",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Text Processing :: Markup :: HTML",
          ],
      keywords="html clean",
      author="Wichert Akkerman",
      author_email="wichert@wiggy.net",
      url="",
      license="BSD",
      packages=find_packages(exclude=["tests"]),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "lxml",
      ],
      extras_require={
          "z3cform": [ "z3c.form",
                       "zope.interface",
                       "zope.component",
                       "zope.schema",
                     ],
      },
      tests_require="nose>=0.10.0b1",
      test_suite="nose.collector",
      )
