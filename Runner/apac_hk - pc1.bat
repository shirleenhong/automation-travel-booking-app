set DATESTAMP=%date:~-4,4%-%date:~-10,2%-%date:~7,2%
set LOGPATH="C:\Users\UEXR493\Documents\QA\Test Results\APACREGRESSION\%DATESTAMP%"
set WORKSPACE="C:\Users\uexr493\Documents\CWT Projects\4.0 PsyEx\PsyEx TFS Workspace Map\PowerExpress\DesktopTest"
set ARGS=-v use_mock_env:False -v version:18.10 -v syex_env:Test -v test_environment:local -e not_ready -e obsolete --removekeywords WUKS trunk/tpro/acceptance_tests/

rem HK test scripts
chdir /d %WORKSPACE%


REM 

call pybot -d %LOGPATH%\HK\other_services -i other_servicesANDhk %ARGS%




chdir /d %WORKSPACE%\Runner
call python copyfile.py %WORKSPACE%\Runner\result_extractor_excel.py %LOGPATH%
call python copyfile.py %WORKSPACE%\Runner\send_email_apac.py %LOGPATH%
call timeout 5

chdir /d %LOGPATH%
call python result_extractor_excel.py
call timeout 2
call python send_email_apac.py

REM REM PNR CANCELLER
REM chdir /d %WORKSPACE%
REM call pybot -d %LOGPATH%\pnr_canceller\amadeus -v version:18.10 -v test_environment:local -i pnr_cancellerANDamadeus trunk/pnr_canceller/
pause