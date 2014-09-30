===============
Release History
===============


.. _whats-new:

Version 6.0.1     2014-09-30
============================

Fixes/Other Changes:
--------------------

   - deleted wrong double line in README.rst
   - some code style adjustments
   - updated tested python version to: 3.4.2rc1
   - Required Software: 

      - setuptools >= 6.0.2
      - PSphinxTheme >= 1.4.0


Version 6.0.0     2014-09-26
============================

Features:
---------

   - implementation of: LCONF_Specification-6.0.rst (raised version to reflect the LCONF_Specification version)

      .. note::

         `LCONF Specification 6.0` is not backwards compatible

            - it allows deep nesting of `Repeated Blocks` and `Key-Value Mappings`

            - it introduces two new identifier for `Key-Value Mappings` and for all `Lists`

               - now all `special LCONF Structures` have identifiers

            - added support for setting empty `Key-Value-Lists`

            - changed `Key :: Value-Lists`: got rid of the square brackets

            - it adds `List-Of-Tuples`: useful for multidimensional lists or tables e.g. csv data

   - added function: `lconf_to_native_type` which transform lconf to a python native type

      - which can be used for example to dump to yaml


   - **Speed Improvements:**

   .. rst-class:: fullwidth

   .. table:: Speed Improvements: new python library version is much faster than the previous implementation

      ======================== =========================================== =================================================
      lconf library action     PY version speed improvement                final speed improvement (cython)
      ======================== =========================================== =================================================
      lconf validation: FASTER **old** version: is still about 10% faster  final **new** version: takes only 60% of previous
      lconf emit: FASTER       **new** version: is about 30% faster        final **new** version: takes only 50% of previous
      lconf parse: FASTER      **new** version: is about 15% faster        final **new** version: takes only 55% of previous
      ======================== =========================================== =================================================

   .. rst-class:: fullwidth

   .. table:: Speed Comparison: PY: lconf vs. json (using OrderedDict) vs. PyYAML (3.11)

      =========== ================= =============================== ================================
      action      PY PyYAML         PY json (using OrderedDict)     PY lconf
      =========== ================= =============================== ================================
      emit/dump:  **slowest** 100%  **middle** 6% of PyYaml's time  **fastest** 1% of PyYaml's time
      parse/load: **slowest** 100%  **middle** 6% of PyYaml's time  **fastest** 3% of PyYaml's time
      =========== ================= =============================== ================================


   .. rst-class:: fullwidth

   .. table:: Speed Comparison: C: lconf vs. json (using OrderedDict) vs. PyYAML (3.11)

      =========== =========================== ====================================== ========================================
      action      C  json (using OrderedDict) C  json                                C lconf
      =========== =========================== ====================================== ========================================
      emit/dump:  **slowest** 100%            **middle** 70% of Ordered Json's time  **fastest** 26% of Ordered Json's time
      parse/load: **slowest** 100%            **fastest** 10% of Ordered Json's time **middle** 90% of Ordered Json's time
      =========== =========================== ====================================== ========================================


   .. todo::

      At the moment the `LCONF` cython extensions `.pyx` is just a simple copy of the `.py` file.
      This could be improved in the future.


Fixes/Other Changes:
--------------------

   - improved: setup.py, MANIFEST.in, Makefile
   - changed: transform.py `lconf_to_datetime` format from: `YYYY-MM-DD-hh:mm` to `YYYY-MM-DD hh:mm`

      - plus additional support for: lconf_to_datetime `YYYY-MM-DD hh:mm:ss`

   - update required package versions


Version 2.6.0     2014-07-02
============================

Features:
---------

   - implementation of: LCONF_Specification-5.0.rst


Project start 2014-04-21
========================

   - project start
