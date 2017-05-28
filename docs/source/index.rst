Maya Command Signature Scraper: For people who just really want to check their maya.cmds signatures
###################################################################################################
`Online Documentation (ReadTheDocs) <http://mayasig-cli.readthedocs.io/en/latest/#module-maya_signatures.commands.scrape>`_

.. image:: https://badge.fury.io/py/Maya-Signature-Scraper.svg
    :target: https://badge.fury.io/py/Maya-Signature-Scraper

.. image:: https://travis-ci.org/AndresMWeber/mayasig_cli.svg?branch=master
    :target: https://travis-ci.org/AndresMWeber/mayasig_cli

.. image:: https://coveralls.io/repos/github/AndresMWeber/mayasig_cli/badge.svg?branch=master
    :target: https://coveralls.io/github/AndresMWeber/mayasig_cli?branch=master

.. image:: https://landscape.io/github/AndresMWeber/maya-cmds-help/master/landscape.svg?style=flat
   :target: https://landscape.io/github/AndresMWeber/maya-cmds-help/master
   :alt: Code Health

.. contents::

.. section-numbering::

Synopsis
=============

If you're looking into this tool, you're looking for a programmatic way of getting Maya function signatures.  The current version of the tool has unfiltered prints as status logs...so that might be a deterrent...  I personally built it so that I could compare my maya command calls against kwargs/args Maya expects to reduce errors.

Hope you'll find it useful!  Once you install you will now have a CLI tool called mayasig.

Features
--------
-  Caching
-  Up to date with online help docs
-  Temp file generator
-  JSON file output
-  CLI access
-  Dict output

Installation
============
Windows, etc.
-------------
A universal installation method (that works on Windows, Mac OS X, Linux, …, and always provides the latest version) is to use `pip`:

.. code-block:: bash

    # Make sure we have an up-to-date version of pip and setuptools:
    $ pip install --upgrade pip setuptools
    $ pip install maya-cmds-help


(If ``pip`` installation fails for some reason, you can try
``easy_install maya-cmds-help`` as a fallback.)

Usage
=============

Bash
------------

.. code-block:: bash

    mayasig

    Usage:
      mayasig [-m|--mayaversion VERSION] [-d|--depth DEPTH] (MAYA_CMDS ...)
      mayasig (-h|--help)
      mayasig (--version)

    Options:
      -h --help                         Show this screen.
      --version                         Show version.
      -m VERSION --mayaversion VERSION  If you want to override which Maya docs we query (tested with 2015/2016/2017) [default: 2017]
      -d DEPTH --depth DEPTH            The depth verbosity of the return dictionary [default: 1]
      MAYA_CMDS                         Maya commands to query/scrape from the help and return signatures for

    Examples:
      mayasig group

    Help:
      For help using this tool, please open an issue on the Github repository:
      https://github.com/andresmweber/mayasig-cli

Python Package Usage
---------------------
Feel free to access from the package instead via the two package-level convenience functions:

.. code-block:: python

    maya_signatures.CACHE
    maya_signatures.query

In order to access full functionality from the scraper class you can access a package level instance of maya_signatures.commands.scrape.Scraper using:

.. code-block:: python

    maya_signatures.SCRAPER


.. code-block:: python

    import maya_signatures
    maya_signatures.query('ls')
    # Result:
    #   storing args  ('ls',)  storing kwargs  {}
    #   Successfully loaded json data, loading into cache...
    #   Retrieving cached value for input http://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/CommandsPython/ls.html
    #   wrote out tmp file C:\Users\andre\dev\maya_signature_builder\scrape.json

    maya_signatures.SCRAPER.build_command_stub('ls')
    #  Result: def ls(*args, textures=bool, selection=bool, defaultNodes=bool, templated=bool, visible=bool, references=bool, flatten=bool, nodeTypes=bool, persistentNodes=bool, intermediateObjects=bool, long=bool, leaf=bool, recursive=bool, objectsOnly=bool, lockedNodes=bool, cameras=bool, tail=int, absoluteName=bool, lights=bool, live=bool, renderSetups=bool, containerType=str, preSelectHilite=bool, type=str, containers=bool, shortNames=bool, renderResolutions=bool, head=int, showType=bool, dependencyNodes=bool, orderedSelection=bool, renderQualities=bool, readOnly=bool, referencedNodes=bool, showNamespace=bool, invisible=bool, hilite=bool, untemplated=bool, partitions=bool, ghost=bool, uuid=bool, sets=bool, geometry=bool, assemblies=bool, noIntermediate=bool, modified=bool, allPaths=bool, shapes=bool, materials=bool, excludeType=str, planes=bool, exactType=str, renderGlobals=bool, undeletable=bool, dagObjects=bool, transforms=bool):
    #              pass

.. code-block:: python

    maya_signatures.query('group')
    #  Result: storing args  ('group',)  storing kwargs  {}
    #  Successfully loaded json data, loading into cache...
    #  Could not find key http://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/CommandsPython/group.html in cached values...retrieving...
    #  Trying to find command for web page:
    #          http://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/CommandsPython/group.html
    #  wrote out tmp file C:\Users\andre\dev\maya_signature_builder\scrape.json
    maya_signatures.SCRAPER.get_command_flags('group')
    #  Result: [('name', 'n'), ('parent', 'p'), ('relative', 'r'), ('useAsGroup', 'uag'), ('world', 'w'), ('empty', 'em'), ('absolute', 'a')]

Class Documentation
===================
.. automodule:: maya_signatures.commands.scrape
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

Version Support
===============
This package supports the Maya 2015, 2016 and 2017 help docs so far so please be aware.
I might back port a couple versions of the maya online help, but this is totally dependent on time.


* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
