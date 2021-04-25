set DATESTAMP=%date:~-4,4%-%date:~-10,2%-%date:~7,2%
set LOGPATH=C:\Users\U001JCP\TFS\PowerExpressTestAutomation\DesktopTest\Logs\%DATESTAMP%\galileo
set WORKSPACE=C:\Users\U001JCP\TFS\PowerExpressTestAutomation\DesktopTest
set ARGS=-v use_mock_env:False -v version:17.11 -v syex_env:Test -v test_environment:local -e not_ready -e login_dependent -e rail_display -e apac --removekeywords WUKS trunk/acceptance_tests/

chdir /d %WORKSPACE%
call pybot -d %LOGPATH%\air_fare -i air_fareANDgalileo %ARGS%
call pybot -d %LOGPATH%\amend -i amendANDgalileo %ARGS%
call pybot -d %LOGPATH%\apis_sfpd -i apis_sfpdANDgalileo %ARGS%
call pybot -d %LOGPATH%\business_rules -i business_rulesANDgalileo %ARGS%
call pybot -d %LOGPATH%\car -i carANDgalileo %ARGS%
call pybot -d %LOGPATH%\client_fees -i client_feesANDgalileo %ARGS%
call pybot -d %LOGPATH%\client_info -i client_infoANDgalileo %ARGS%
call pybot -d %LOGPATH%\complete -i completeANDgalileo %ARGS%
call pybot -d %LOGPATH%\cust_refs -i cust_refsANDgalileo %ARGS%
call pybot -d %LOGPATH%\database -i databaseANDgalileo %ARGS%
call pybot -d %LOGPATH%\delivery -i deliveryANDgalileo %ARGS%
call pybot -d %LOGPATH%\gds -i gdsANDgalileo %ARGS%
call pybot -d %LOGPATH%\id_traveller -i id_travellerANDgalileo %ARGS%
call pybot -d %LOGPATH%\policy_check -i policy_checkANDgalileo %ARGS%
call pybot -d %LOGPATH%\pspt_and_visa -i pspt_and_visaANDgalileo %ARGS%
call pybot -d %LOGPATH%\recap -i recapANDgalileo %ARGS%
call pybot -d %LOGPATH%\third_party -i third_partyANDgalileo %ARGS%
call pybot -d %LOGPATH%\unused_documents -i unused_documentsANDgalileo %ARGS%

chdir /d %WORKSPACE%\Runner
call python copyfile.py %WORKSPACE%\Runner\result_extractor_excel.py %LOGPATH%
call python copyfile.py %WORKSPACE%\Runner\send_email.py %LOGPATH%
call timeout 5

chdir /d %LOGPATH%
call python result_extractor_excel.py
call timeout 2
call python send_email.py

rem PNR CANCELLER
chdir /d %WORKSPACE%
call pybot -d %LOGPATH%\pnr_canceller\galileo -v version:18.4 -v syex_env:Test -v test_environment:local -i pnr_cancellerANDgalileo trunk/pnr_canceller/
pause