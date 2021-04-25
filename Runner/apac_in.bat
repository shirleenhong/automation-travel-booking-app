set DATESTAMP=%date:~-4,4%-%date:~-10,2%-%date:~7,2%
set LOGPATH="C:\Users\U001JCP\TFS\PowerExpressTestAutomation\DesktopTest\Logs\%DATESTAMP%"
set WORKSPACE="C:\Users\U001JCP\TFS\PowerExpressTestAutomation\DesktopTest"
set ARGS=-v use_mock_env:False -v version:18.10 -v syex_env:Test -v test_environment:local -e not_ready -e obsolete --removekeywords WUKS trunk/tpro/acceptance_tests/

rem IN test scripts
chdir /d %WORKSPACE%
call pybot -d %LOGPATH%\in\air_fare -i air_fareANDin %ARGS%
call pybot -d %LOGPATH%\in\client_info -i client_infoANDin %ARGS%
call pybot -d %LOGPATH%\in\cust_refs -i cust_refsANDin %ARGS%
call pybot -d %LOGPATH%\in\delivery -i deliveryANDin %ARGS%
call pybot -d %LOGPATH%\in\id_traveller -i id_travellerANDin %ARGS%
call pybot -d %LOGPATH%\in\obt -i obtANDin %ARGS%
call pybot -d %LOGPATH%\in\other_services -i other_servicesANDin %ARGS%
call pybot -d %LOGPATH%\in\policy_check -i policy_checkANDin %ARGS%
call pybot -d %LOGPATH%\in\pspt_and_visa -i pspt_and_visaANDin %ARGS%

call pybot -d %LOGPATH%\in\apis_sfpd -i apis_sfpdANDin %ARGS%
call pybot -d %LOGPATH%\in\car -i carANDin %ARGS%
call pybot -d %LOGPATH%\in\send_itinerary -i send_itineraryANDin %ARGS%
call pybot -d %LOGPATH%\in\workflow -i workflowANDin %ARGS%

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
REM call pybot -d %LOGPATH%\pnr_canceller\amadeus -v version:18.2 -v test_environment:local -i pnr_cancellerANDamadeus trunk/pnr_canceller/
pause