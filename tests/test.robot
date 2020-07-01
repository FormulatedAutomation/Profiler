*** Settings ***
Library  formulated_automation.profiler.System
Library  formulated_automation.profiler.Debug

Suite Teardown  Teardown

*** Variables ***
${SecretKey}   SuperSecretKey

*** Keywords ***
Teardown
    Write Profile

*** Test Cases ***
Set a breakpoint
    Set Breakpoint
