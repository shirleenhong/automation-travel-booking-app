set DATESTAMP=%date:~-4,4%-%date:~-10,2%-%date:~7,2%
set LOGPATH=C:\Users\U001JCP\TFS\PowerExpressTestAutomation\DesktopTest\Logs\%DATESTAMP%\amadeus
set WORKSPACE=C:\Users\U001JCP\TFS\PowerExpressTestAutomation\DesktopTest
rem for classic
rem set ARGS=-v use_mock_env:False -v version:18.7 -v syex_env:Test -v test_environment:local -e not_ready -e login_dependent -e rail_display -e apac --removekeywords WUKS trunk/acceptance_tests/
rem for sellco
set ARGS=-v use_mock_env:True -v version:18.7 -v syex_env:Test -v test_environment:local -v amadeus_env:sellco -e login_dependent -e rail_display -e apac -e resa_rail -e not_ready -e tqt_needed --removekeywords WUKS trunk/acceptance_tests/

rem fr test scripts
chdir /d %WORKSPACE%
call pybot -d %LOGPATH%\fr\amend -i amendANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\apis_sfpd -i apis_sfpdANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\business_rules -i business_rulesANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\car -i carANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\client_fees -i client_feesANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\client_info -i client_infoANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\cust_refs -i cust_refsANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\database -i databaseANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\delivery -i deliveryANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\id_traveller -i id_travellerANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\policy_check -i policy_checkANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\complete -i completeANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\pspt_and_visa -i pspt_and_visaANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\recap -i recapANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\unused_documents -i unused_documentsANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\third_party -i third_partyANDamadeus %ARGS%
call pybot -d %LOGPATH%\fr\price_tracking -i price_trackingANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\duo_integration -i duo_integrationANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\air_fare -i air_fareANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\gds -i gdsANDamadeusANDfr %ARGS%

chdir /d %WORKSPACE%\Runner
call python copyfile.py %WORKSPACE%\Runner\result_extractor_excel.py %LOGPATH%
call python copyfile.py %WORKSPACE%\Runner\send_email.py %LOGPATH%
call timeout 5

chdir /d %LOGPATH%
call python result_extractor_excel.py
call timeout 2
call python send_email.py

REM REM PNR CANCELLER
chdir /d %WORKSPACE%
call pybot -d %LOGPATH%\pnr_canceller\amadeus -v version:18.2 -v test_environment:local -i pnr_cancellerANDamadeus trunk/pnr_canceller/
pause