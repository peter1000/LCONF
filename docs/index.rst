.. image:: _static/LCONFMain350_220.png
   :align: center

=============
Documentation
=============

This is release |release| of a Python package named :mod:`!LCONF`.

:Author: peter1000
:Github: https://github.com/peter1000


Welcome
=======
`LCONF` stands for L(ight) CONF(iguration) a light - human-friendly, simple readable data serialization format for dynamic
configuration.

- in many situations `LCONF` is a suitable replacement for `YAML <http://www.yaml.org/>`_
- `LCONF` can be used to replace `JSON <http://json.org/>`_ in many cases

.. note::

   - LCONF python library is much faster than PyYAML 3.11
   - LCONF python library emits much faster than the python included json (c extension) defaults
   - LCONF python library parses a little bit faster than the python included json (c extension) using an OrderedDict
   - LCONF python library parses still much slower than the python included json (c extension) defaults

|

- This package contains also the original `python3/cython LCONF implementation`

- There exists a simple `pygments lexer` for LCONF: to highlight code
   `LconfPygmentsLexer <https://github.com/peter1000/LconfPygmentsLexer>`_

- There is also a `sphinx theme` which has an admonition for LCONF Example code.
   `PSphinxTheme <https://github.com/peter1000/PSphinxTheme>`_


Below is an example using the `PSphinxTheme` lconf-example admonition which uses `LconfPygmentsLexer` to highlight code.


.. lconf-example:: This is a `LCONF` example using the `PSphinxTheme` lconf-admonition to highlight code

   .. code-block:: lconf

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


Content Summary
===============

.. rst-class:: floater

.. seealso:: :ref:`What's new in LCONF <whats-new>`


Introductory Materials
----------------------

:doc:`install`
   requirements and installations instructions


**LCONF-Specification docs:**

- :doc:`LCONF_Specification_Abstract`
- :doc:`LCONF_Specification`
- :doc:`LCONF_Specification_Examples`


:doc:`history`
   history of current and past releases


.. _code-usage-examples:

Code & Usage Examples
=====================

:ref:`LCONF-Default-Template-Structure Usage Example <lconf-default-template-structure-usage-example>`


For more *examples* see any files in the `LCONF source` (not all projects might have all of these folders).

- :samp:`{SOURCE}/Examples`

- :samp:`{SOURCE}/Tests`

- :samp:`{SOURCE}/SpeedIT`


Online Resources
================

.. rst-class:: html-plain-table

   ================ ====================================================
   Homepage:        `<https://github.com/peter1000/LCONF>`_
   Online Docs:     `<http://packages.python.org/LCONF>`_
   Download & PyPI: `<http://pypi.python.org/pypi/LCONF>`_
   Source:          `<https://github.com/peter1000/LCONF>`_
   ================ ====================================================


Related Resources
-----------------

.. rst-class:: html-plain-table

   =================== ==================================================== ================================================
   LconfPygmentsLexer: `<https://github.com/peter1000/LconfPygmentsLexer>`_ a simple pygments lexer for LCONF
   PSphinxTheme:       `<https://github.com/peter1000/PSphinxTheme>`_       a sphinx theme which has an admonition for LCONF
   =================== ==================================================== ================================================


Projects using LCONF
====================

Known `projects` which make use of: **LCONF**

- `PyNHEP <https://github.com/peter1000/PyNHEP>`_
   PyNHEP: The N(utrition) and H(ealthy) E(ating) P(lanner).
