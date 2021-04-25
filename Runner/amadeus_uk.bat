set DATESTAMP=%date:~-4,4%-%date:~-10,2%-%date:~7,2%
set LOGPATH=C:\Users\U001JCP\TFS\PowerExpressTestAutomation\DesktopTest\Logs\%DATESTAMP%\amadeus
set WORKSPACE=C:\Users\U001JCP\TFS\PowerExpressTestAutomation\DesktopTest
rem for classic
rem set ARGS=-v use_mock_env:False -v version:18.7 -v syex_env:Test -v test_environment:local -e not_ready -e login_dependent -e rail_display -e apac --removekeywords WUKS trunk/acceptance_tests/
rem for sellco
set ARGS=-v use_mock_env:False -v version:18.7 -v syex_env:Test -v test_environment:local -v amadeus_env:sellco -e login_dependent -e rail_display -e apac -e resa_rail -e not_ready -e tqt_needed --removekeywords WUKS trunk/acceptance_tests/

rem uk test scripts
chdir /d %WORKSPACE%
call pybot -d %LOGPATH%\uk\third_party -i third_partyANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\gds -i gdsANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\air_fare -i air_fareANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\amend -i amendANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\apis_sfpd -i apis_sfpdANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\business_rules -i business_rulesANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\car -i carANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\client_fees -i client_feesANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\client_info -i client_infoANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\complete -i completeANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\cust_refs -i cust_refsANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\database -i databaseANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\delivery -i deliveryANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\id_traveller -i id_travellerANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\policy_check -i policy_checkANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\pspt_and_visa -i pspt_and_visaANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\recap -i recapANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\unused_documents -i unused_documentsANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\price_tracking -i price_trackingANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\duo_integration -i duo_integrationANDamadeusANDuk %ARGS%

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