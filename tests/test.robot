*** Settings ***
Library  FormulatedAutomation.Profiler.System
Library  FormulatedAutomation.Profiler.Debug

Suite Teardown  Teardown

*** Variables ***
${SecretKey}   SuperSecretKey

*** Keywords ***
Teardown
    Write Profile

*** Test Cases ***
Get a system profile
    Set Breakpoint
