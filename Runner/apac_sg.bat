set DATESTAMP=%date:~-4,4%-%date:~-10,2%-%date:~7,2%
set LOGPATH="C:\Users\uexr493\Documents\CWT Projects\4.0 PsyEx\PsyEx TFS Workspace Map\PowerExpress\DesktopTest\Logs\%DATESTAMP%"
set WORKSPACE="C:\Users\uexr493\Documents\CWT Projects\4.0 PsyEx\PsyEx TFS Workspace Map\PowerExpress\DesktopTest"
set ARGS=-v use_mock_env:False -v version:19.4 -v syex_env:Test -v test_environment:local -e other_services -e not_ready -e obsolete --removekeywords WUKS trunk/tpro/acceptance_tests/

rem sg test scripts
chdir /d %WORKSPACE%



call pybot -d %LOGPATH%\sg\air_fare -i air_fareANDsg %ARGS%
call pybot -d %LOGPATH%\sg\client_info -i client_infoANDsg %ARGS%
call pybot -d %LOGPATH%\sg\cust_refs -i cust_refsANDsg %ARGS%
call pybot -d %LOGPATH%\sg\delivery -i deliveryANDsg %ARGS%
call pybot -d %LOGPATH%\sg\id_traveller -i id_travellerANDsg %ARGS%
call pybot -d %LOGPATH%\sg\obt -i obtANDsg %ARGS%
call pybot -d %LOGPATH%\sg\policy_check -i policy_checkANDsg %ARGS%
call pybot -d %LOGPATH%\sg\pspt_and_visa -i pspt_and_visaANDsg %ARGS%
call pybot -d %LOGPATH%\sg\unused_document -i unused_documentANDsg %ARGS%
call pybot -d %LOGPATH%\sg\apis_sfpd -i apis_sfpdANDsg %ARGS%
call pybot -d %LOGPATH%\sg\car -i carANDsg %ARGS%
call pybot -d %LOGPATH%\sg\send_itinerary -i send_itineraryANDsg %ARGS%
call pybot -d %LOGPATH%\sg\workflow -i workflowANDsg %ARGS%

chdir /d %WORKSPACE%\Runner
call python copyfile.py result_extractor_excel.py %LOGPATH%
call python copyfile.py send_email_apac.py %LOGPATH%
call timeout 5
chdir /d %LOGPATH%
call python result_extractor_excel.py
call timeout 2
call python send_email_apac.py

REM REM PNR CANCELLER
REM chdir /d %WORKSPACE%
REM call pybot -d %LOGPATH%\pnr_canceller\amadeus -v version:18.2 -v test_environment:local -i pnr_cancellerANDamadeus trunk/pnr_canceller/
pause