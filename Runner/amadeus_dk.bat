set DATESTAMP=%date:~-4,4%-%date:~-10,2%-%date:~7,2%
set LOGPATH=C:\Users\U001JCP\TFS\PowerExpressTestAutomation\DesktopTest\Logs\%DATESTAMP%\amadeus
set WORKSPACE=C:\Users\U001JCP\TFS\PowerExpressTestAutomation\DesktopTest
rem for classic
set ARGS=-v use_mock_env:False -v version:18.7 -v syex_env:Test -v test_environment:local -e not_ready -e login_dependent -e rail_display -e apac --removekeywords WUKS trunk/acceptance_tests/
rem for sellco
rem set ARGS=-v use_mock_env:False -v version:18.4 -v syex_env:Test -v test_environment:local -v amadeus_env:sellco -e login_dependent -e rail_display -e apac -e resa_rail -e not_ready -e tqt_needed --removekeywords WUKS trunk/acceptance_tests/

rem dk test scripts
chdir /d %WORKSPACE%
call pybot -d %LOGPATH%\dk\air_fare -i air_fareANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\amend -i amendANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\apis_sfpd -i apis_sfpdANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\business_rules -i business_rulesANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\car -i carANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\client_fees -i client_feesANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\client_info -i client_infoANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\complete -i completeANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\cust_refs -i cust_refsANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\database -i databaseANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\delivery -i deliveryANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\id_traveller -i id_travellerANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\policy_check -i policy_checkANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\pspt_and_visa -i pspt_and_visaANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\recap -i recapANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\unused_documents -i unused_documentsANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\third_party -i third_partyANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\gds -i gdsANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\price_tracking -i price_trackingANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\duo_integration -i duo_integrationANDamadeusANDdk %ARGS%

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