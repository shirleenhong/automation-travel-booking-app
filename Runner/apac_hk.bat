set DATESTAMP=%date:~-4,4%-%date:~-10,2%-%date:~7,2%
set LOGPATH="C:\Users\uexr493\Documents\CWT Projects\4.0 PsyEx\PsyEx TFS Workspace Map\PowerExpress\DesktopTest\Logs\%DATESTAMP%"
set WORKSPACE="C:\Users\uexr493\Documents\CWT Projects\4.0 PsyEx\PsyEx TFS Workspace Map\PowerExpress\DesktopTest"
set ARGS=-v use_mock_env:False -v version:19.4 -v syex_env:Test -v test_environment:local -e other_services -e not_ready -e obsolete --removekeywords WUKS trunk/tpro/acceptance_tests/

rem HK test scripts
chdir /d %WORKSPACE%
REM call pybot -d %LOGPATH%\HK\air_fare -i air_fareANDhk %ARGS%
call pybot -d %LOGPATH%\HK\client_info -i client_infoANDhk %ARGS%
call pybot -d %LOGPATH%\HK\cust_refs -i cust_refsANDhk %ARGS%
call pybot -d %LOGPATH%\HK\delivery -i deliveryANDhk %ARGS%
call pybot -d %LOGPATH%\HK\id_traveller -i id_travellerANDhk %ARGS%
call pybot -d %LOGPATH%\HK\obt -i obtANDhk %ARGS%
REM call pybot -d %LOGPATH%\HK\other_services -i other_servicesANDhk %ARGS%
call pybot -d %LOGPATH%\HK\policy_check -i policy_checkANDhk %ARGS%
call pybot -d %LOGPATH%\HK\pspt_and_visa -i pspt_and_visaANDhk %ARGS%
call pybot -d %LOGPATH%\HK\unused_document -i unused_documentANDhk %ARGS%

call pybot -d %LOGPATH%\HK\apis_sfpd -i apis_sfpdANDhk %ARGS%
call pybot -d %LOGPATH%\HK\car -i carANDhk %ARGS%
call pybot -d %LOGPATH%\HK\send_itinerary -i send_itineraryANDhk %ARGS%
call pybot -d %LOGPATH%\HK\workflow -i workflowANDhk %ARGS%

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