FormulatedAutomation-Profiler
==================

.. contents::

**In Alpha, rapidly changing**

Introduction
------------

Installation
------------

Usage
-----

.. code:: robotframework

    *** Settings ***
    Library                 FormulatedAutomation.Profiler
    Suite Teardown          Teardown

    *** Keywords ***
    Teardown
        Write Profile



Testing
-------

`$Env:ROBOT_DEBUG = "FALSE"; robot -d output -P src tests`