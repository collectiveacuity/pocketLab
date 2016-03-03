=======
labMgmt
=======
*A Collection of Methods for Managing Laboratory Projects*

:Source: https://bitbucket.org/collectiveacuity/labsmgmt.git

High-Level Classes
------------------
- **labScraper**: A class to manage various different scraping techniques

Low-Level Classes
-----------------
- **seleniumMod**: A class to scrape data from websites based upon selenium
- **splinterMod**: A class to scrape data from websites based upon splinter
- **morphAPI**: A class to manage requests to Morph.io to scrape data from websites

Features
--------
-

System Requirements
-------------------
- **pycrypto**: https://pypi.python.org/pypi/pycrypto
- - Windows requires Microsoft Visual Studio packages
- - Linux requires C compiler (often in dev distro)
- **phantomjs**: http://phantomjs.org/

Installation
============
From BitBucket::

    $ git clone https://bitbucket.org/collectiveacuity/labscrape.git
    $ python setup.py sdist --format=gztar
    $ python setup.py develop  # for local on-the-fly file updates

Getting Started
^^^^^^^^^^^^^^^
This module is designed to manage...

Run a string validation tool::
.. code-block:: python

    from labScrape.webscrapers import labScraper

    scraper = labScraper()

For more details about how to use labScrape, refer to the
`Reference Documentation on BitBucket
<https://bitbucket.org/collectiveacuity/labScrape/REFERENCE.rst>`_