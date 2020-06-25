*** Settings ***
Library  FormulatedAutomation.Profiler.System
Library  FormulatedAutomation.Profiler.Debug

Suite Teardown  Teardown

*** Keywords ***
Teardown
    Write Profile

*** Test Cases ***
Get a system profile
    Set Breakpoint
