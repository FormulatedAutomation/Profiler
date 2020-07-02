**Formulated Autoamation RPA Resources**

- `/r/OpenSourceRPA <https://reddit.com/r/OpenSourceRPA>`_
- `OpenSource RPA LinkedIn Group <https://www.linkedin.com/groups/12366622/>`_
- `FormulatedAutomation's YouTube Screencasts <https://www.youtube.com/channel/UC_IMgIFlNBG94Vm8tNCNeUQ>`_

FormulatedAutomation-Profiler
=============================

.. contents::

Introduction
------------

The purpose of this project is to record a snapshot of the runtime environment for an automation workspace.  This
includes recording installed applications and their versions on the machine.  This is especially useful when
automations stop working and allows for rapid debugging of machine prior and current states.

⚠️ This project is currently a work in process and should not be used in production environments. ⚠️

Installation
------------
- Create a virtual environment
- `pip install -e git+https://github.com/FormulatedAutomation/robot-profiler.git#egg=robot-profiler`

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

This library expects teh `ROBOT_DEBUG` environment variable to be set.  You can do this however suits your platform:

Powershell: `$Env:ROBOT_DEBUG="FALSE"`
Windows CMD: `set ROBOT_DEBUG="FALSE"`

Execute the tests in this project:

.. code:: bash

    robot -d output -P src tests
