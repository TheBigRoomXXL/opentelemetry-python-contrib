OpenTelemetry Requests Instrumentation
======================================

|pypi|

.. |pypi| image:: https://badge.fury.io/py/opentelemetry-instrumentation-requests.svg
   :target: https://pypi.org/project/opentelemetry-instrumentation-requests/

This library allows tracing deserialization, validation and seralization made by the
`marshmallow <https://marshmallow.readthedocs.io/en/stable/>`_ library.

Installation
------------

::

     pip install opentelemetry-instrumentation-marshmallow

Configuration
-------------

Exclude lists (TODO)
*************
To exclude certain URLs from being tracked, set the environment variable ``OTEL_PYTHON_MARSHMALLOW_EXCLUDED_SCHEMA``
with comma delimited regexes representing which schema to exclude.

For example,

::

    export OTEL_PYTHON_MARSHMALLOW_EXCLUDED_SCHEMA="client/.*/info,healthcheck"

will exclude requests such as ``https://site/client/123/info`` and ``https://site/xyz/healthcheck``.

References
----------

* `OpenTelemetry requests Instrumentation <https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/requests/requests.html>`_
* `OpenTelemetry Project <https://opentelemetry.io/>`_
* `OpenTelemetry Python Examples <https://github.com/open-telemetry/opentelemetry-python/tree/main/docs/examples>`_
