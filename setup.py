from setuptools import setup, find_packages

version = "1.2"

setup(name="htmllaundry",
      version=version,
      description="Simple HTML cleanup utilities",
      long_description=open("README.txt").read()+"\n\n"+
                       open("CHANGES.txt").read(),
      classifiers=[
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
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
