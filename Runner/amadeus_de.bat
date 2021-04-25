set DATESTAMP=%date:~-4,4%-%date:~-10,2%-%date:~7,2%
set LOGPATH=C:\Users\U001JCP\TFS\PowerExpressTestAutomation\DesktopTest\Logs\%DATESTAMP%\amadeus
set WORKSPACE=C:\Users\U001JCP\TFS\PowerExpressTestAutomation\DesktopTest
rem for classic
set ARGS=-v use_mock_env:False -v version:18.7 -v syex_env:Test -v test_environment:local -e not_ready -e login_dependent -e rail_display -e apac --removekeywords WUKS trunk/acceptance_tests/
rem for sellco
rem set ARGS=-v use_mock_env:False -v version:18.4 -v syex_env:Test -v test_environment:local -v amadeus_env:sellco -e login_dependent -e rail_display -e apac -e resa_rail -e not_ready -e tqt_needed --removekeywords WUKS trunk/acceptance_tests/

chdir /d %WORKSPACE%

rem de test scripts
call pybot -d %LOGPATH%\de\air_fare -i air_fareANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\amend -i amendANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\apis_sfpd -i apis_sfpdANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\business_rules -i business_rulesANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\car -i carANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\client_fees -i client_feesANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\client_info -i client_infoANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\complete -i completeANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\cust_refs -i cust_refsANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\database -i databaseANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\delivery -i deliveryANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\id_traveller -i id_travellerANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\policy_check -i policy_checkANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\pspt_and_visa -i pspt_and_visaANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\recap -i recapANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\unused_documents -i unused_documentsANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\third_party -i third_partyANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\gds -i gdsANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\price_tracking -i price_trackingANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\duo_integration -i duo_integrationANDamadeusANDde %ARGS%

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