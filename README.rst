=====
LCONF
=====

About
=====
`LCONF` stands for L(ight) CONF(iguration) a light - human-friendly, simple readable data serialization format for dynamic
configuration.

.. important:: REPLACEMENT

   - in many situations `LCONF` is a suitable replacement for `YAML <http://www.yaml.org/>`_
   - `LCONF` can be used to replace `JSON <http://json.org/>`_ in many cases

.. note::

   - LCONF python library is much faster than PyYAML 3.11
   - LCONF python library emits much faster than the python included json (c extension) defaults
   - LCONF python library parses a little bit faster than the python included json (c extension) using an OrderedDict
   - LCONF python library parses still much slower than the python included json (c extension) defaults


|

The latest documentation can be found online at `<http://packages.python.org/LCONF>`_.

|

.. code-block:: text

   ___SECTION :: A short example with a number of features

   # Comment-Line: `List-Of-Tuples`
   - people_list |name|height_cm|weight_kg|
      Tim,  178,  86
      John, 166,  67

   # Comment-Line: `Repeated-Block-Identifier`
   * Persons_BLK
      person1
         first :: Tim
         last :: Doe
         age :: 39
         registered :: true
         salary :: 70000
         sex :: M
         # Comment-Line: `Key :: Value-List`
         - interests :: Reading,Mountain Biking,Hacking
         # Comment-Line: `Key-Value-List`
         - sports
            tennis
            football
            soccer
         # Comment-Line: `Key-Value-Mapping`
         . favorites
            food :: Spaghetti
            sport :: Soccer
            color :: Blue
      person2
         first :: John
         last :: Doe
         age :: 29
         registered :: true
         salary :: 45000
         sex :: M
         # Comment-Line: empty `Key :: Value-List`
         - interests ::
         # Comment-Line: empty `Key-Value-List`
         - sports
         # Comment-Line: `Key-Value-Mapping`
         . favorites
            food :: Pizza
            sport :: None
            color :: Orange
   ___END


Requirements
============
See: RequiredSoftware in documentation or::

   {SOURCE}/docs/RequiredSoftware.rst


Installation
============
#. To install from pypi using ``pip/pip3``::

   $ pip3 install LCONF

#. To install from the source::

   $ python3 setup.py install


Building the Documentation
--------------------------
If you wish to generate your own copy of the documentation, you will need to:

#. Get the `LCONF` source.
#. If not already installed - install `PSphinxTheme <https://github.com/peter1000/PSphinxTheme>`_ ::

   $ pip3 install PSphinxTheme

#. From the `LCONF` source directory, run ``python3 setup.py build_sphinx -E``.
#. Once Sphinx is finished, point a web browser to the file::

   {SOURCE}/build/sphinx/html/index.html


Online Resources
================
- Docs:       http://packages.python.org/LCONF
- PyPI:       http://pypi.python.org/pypi/LCONF
- Source:     https://github.com/peter1000/LCONF


Projects using LCONF
====================

`projects` which make use of: **LCONF**

- `PyNHEP <https://github.com/peter1000/PyNHEP>`_
   PyNHEP: The N(utrition) and H(ealthy) E(ating) P(lanner).


|
|

`LCONF` is distributed under the terms of the BSD 3-clause license.
Consult `LICENSE` or `BSD-3-Clause <http://opensource.org/licenses/BSD-3-Clause>`_.

(c) 2014, `peter1000` https://github.com/peter1000
All rights reserved.

|
|
