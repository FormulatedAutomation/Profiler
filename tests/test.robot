*** Settings ***
Library  FormulatedAutomation.Profiler.System
Library  FormulatedAutomation.Profiler.Debug

Suite Teardown  Teardown

*** Keywords ***
Teardown
    Write Profile To Output

*** Test Cases ***
Get a system profile
    Set Breakpoint
    Write profile to output
