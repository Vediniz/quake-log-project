*** Settings ***
Library    Collections
Library    OperatingSystem
Library    String
Library    ../resources/QuakeLog.py  

*** Variables ***
${TEST_LOG_FILE}                ../data/qltest.log
${expected_report_game_path}    ../data/qlresult_game_report.txt
${expected_report_kbm_path}     ../data/qlresult_kbm_report.txt
*** Test Cases ***
Test Case: Generate Game Report
    [Documentation]    Test case to verify generation of the game report.
    ${games}        QuakeLog.Read File    ${TEST_LOG_FILE}
    ${game_info}    QuakeLog.Extract Informations    ${games}
    ${report}       QuakeLog.Generate Game Report
    ${expected_game_report}    Get File    ${expected_report_game_path}
    ${expected_game_report}    Convert To String    ${expected_game_report}
    Should Be Equal As Strings    ${report}    ${expected_game_report}

Test Case: Generate Kill by Means Report
    [Documentation]    Test case to verify generation of the kill by means report.
    ${games}        QuakeLog.Read File    ${TEST_LOG_FILE}
    ${game_info}    QuakeLog.Extract Informations    ${games}
    ${report}        QuakeLog.Generate Kill By Means Report
    ${expected_kbm_report}    Get File    ${expected_report_kbm_path}
    ${expected_kbm_report}    Convert To String    ${expected_kbm_report}
    Should Be Equal As Strings    ${report}    ${expected_kbm_report}
