set DATESTAMP=%date:~-4,4%-%date:~-10,2%-%date:~7,2%
set LOGPATH=C:\Users\U027VXP\DesktopTest\Logs\%DATESTAMP%\sabre
set WORKSPACE=C:\Users\U027VXP\DesktopTest
set ARGS=-v use_mock_env:False -v version:19.1 -v syex_env:Test -v test_environment:local -e not_ready -e login_dependent -e rail_display -e apac --removekeywords WUKS Efficiency_18.10/acceptance_tests/

chdir /d %WORKSPACE%
rem call pybot -d %LOGPATH%\air_fare -i air_fareANDsabre %ARGS%
rem call pybot -d %LOGPATH%\amend -i amendANDsabre %ARGS%
rem call pybot -d %LOGPATH%\apis_sfpd -i apis_sfpdANDsabre %ARGS%
rem call pybot -d %LOGPATH%\business_rules -i business_rulesANDsabre %ARGS%
rem call pybot -d %LOGPATH%\car -i carANDsabre %ARGS%
rem call pybot -d %LOGPATH%\client_fees -i client_feesANDsabre %ARGS%
rem call pybot -d %LOGPATH%\client_info -i client_infoANDsabre %ARGS%
call pybot -d %LOGPATH%\complete -i completeANDsabre %ARGS%
call pybot -d %LOGPATH%\cust_refs -i cust_refsANDsabre %ARGS%
rem call pybot -d %LOGPATH%\database -i databaseANDsabre %ARGS%
rem call pybot -d %LOGPATH%\delivery -i deliveryANDsabre %ARGS%
call pybot -d %LOGPATH%\gds -i gdsANDsabre %ARGS%
call pybot -d %LOGPATH%\id_traveller -i id_travellerANDsabre %ARGS%
call pybot -d %LOGPATH%\policy_check -i policy_checkANDsabre %ARGS%
call pybot -d %LOGPATH%\pspt_and_visa -i pspt_and_visaANDsabre %ARGS%
call pybot -d %LOGPATH%\recap -i recapANDsabre %ARGS%
call pybot -d %LOGPATH%\third_party -i third_partyANDsabre %ARGS%
call pybot -d %LOGPATH%\price_tracking -i price_trackingANDsabre %ARGS%
rem call pybot -d %LOGPATH%\unused_documents -i unused_documentsANDsabre %ARGS%

chdir /d %WORKSPACE%\Runner
call python copyfile.py %WORKSPACE%\Runner\result_extractor_excel.py %LOGPATH%
call python copyfile.py %WORKSPACE%\Runner\send_email.py %LOGPATH%
call timeout 5

chdir /d %LOGPATH%
call python result_extractor_excel.py
call timeout 2
call python send_email.py

REM PNR CANCELLER
chdir /d %WORKSPACE%
call pybot -d %LOGPATH%\pnr_canceller\sabre -v version:18.6 -v syex_env:Test -v test_environment:local -i pnr_cancellerANDsabre trunk/pnr_canceller/
pause