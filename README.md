![Formulated Logo](https://www.formulatedautomation.com/wp-content/uploads/2020/07/Subtract-660x20-1.svg)


**Formulated Autoamation RPA Resources**


-   [/r/OpenSourceRPA](https://reddit.com/r/OpenSourceRPA)
-   [OpenSource RPA LinkedIn
    Group](https://www.linkedin.com/groups/12366622/)
-   [FormulatedAutomation's YouTube
    Screencasts](https://www.youtube.com/channel/UC_IMgIFlNBG94Vm8tNCNeUQ)
-   [Formulated Automation Podcast](https://www.formulatedautomation.com/category/podcast/)


# FormulatedAutomation-Profiler

[![FormulatedAutomation](https://circleci.com/gh/FormulatedAutomation/Profiler.svg?style=shield)](https://app.circleci.com/pipelines/github/FormulatedAutomation/Profiler)

![image](https://user-images.githubusercontent.com/2868/86496363-2473ff00-bd4b-11ea-868a-ee07a2ace9d9.png)

### Introduction

The purpose of this project is to record a snapshot of the runtime
environment for an automation workspace. This includes recording
installed applications and their versions on the machine. This is
especially useful when automations stop working and allows for rapid
debugging of machine prior and current states.

⚠️ This project is currently a work in process and should not be used in
production environments. ⚠️

### Installation

-   Create a virtual environment
-   pip install fa-profiler

### Usage

#### Profiler

``` {.sourceCode .robotframework}
*** Settings ***
Library                 FormulatedAutomation.Profiler
Suite Teardown          Teardown

*** Keywords ***
Teardown
    Write Profile
```

If you look in the 'output' directory (which is the current directory, or
whatever you speficy at runtime), you'll find an fa_report.yml file.
In this file is a profile of the system you ran on, which includes things like

- Python version and installed packages
- Environment variables
- Robot Framework variables (Secrets omitted)
- Installed programs(on Windows)

It's organized in a way that makes 'diffing' it with a previous report trivial
and therefore makes it easy to see what's changed between runs.


[Sample Report from Linux CI](https://35-274999902-gh.circle-artifacts.com/0/output/fa_report.yaml)

##### Omitting secrets from the profile

There's a good chance you're setting a varaible to something you don't want
listed in the logs. In order to prevent secrets from leaking, Profiler will
'redact' any variables with 'secret' in their name. This will later be
configurable.



#### Debugging

The Formulated Automation Profiler also includes some basic debugging tools.

``` {.sourceCode .robotframework}
*** Settings ***
Library                 FormulatedAutomation.Profiler
Suite Teardown          Teardown

*** Keywords ***
Teardown
    Pause On Failure # Launch a Dialog to pause execution whenever a task fails
    Write Profile

*** Keywords ***
Some Task
    Set Breakpoint # Pause execution and drop to Python's 'pdb' debugger
    Do Some Other Task
    Pause for Debug # Pause with a Dialog regardless of failure
```

Pause on Failure and Pause for Debug only occur if the environment variable
'ROBOT_DEBUG' is set to TRUE. This prevents pausing in production if the
keywords are accidentally set.

__Command Line Example:__

Powershell: `$Env:ROBOT_DEBUG = "TRUE"; robot -d output -P src tests `  
Bash: `ROBOT_DEBUG=TRUE && robot -d output -P src tests`


### Testing

This library expects teh ROBOT\_DEBUG environment variable to be set.
You can do this however suits your platform:

Powershell: `$Env:ROBOT_DEBUG = "TRUE"; robot -d output -P src tests `  
Bash: `ROBOT_DEBUG=TRUE && robot -d output -P src tests`

Execute the tests in this project:

``` {.sourceCode .bash}
robot -d output -P src tests
```
