set DATESTAMP=%date:~-4,4%-%date:~-10,2%-%date:~7,2%
set LOGPATH=C:\Users\U001JCP\TFS\PowerExpressTestAutomation\DesktopTest\Logs\%DATESTAMP%\amadeus
set WORKSPACE=C:\Users\U001JCP\TFS\PowerExpressTestAutomation\DesktopTest
rem for classic
set ARGS=-v use_mock_env:False -v version:18.4 -v syex_env:Test -v test_environment:local -e not_ready -e login_dependent -e rail_display -e apac --removekeywords WUKS trunk/acceptance_tests/
rem for sellco
rem set ARGS=-v version:18.4 -v syex_env:Test -v test_environment:local -v amadeus_env:sellco -e not_ready -e login_dependent -e rail_display -e apac -e resa_rail -e not_ready -e tqt_needed --removekeywords WUKS trunk/acceptance_tests/

chdir /d %WORKSPACE%
rem fr test scripts
call pybot -d %LOGPATH%\fr\air_fare -i air_fareANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\gds -i gdsANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\amend -i amendANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\apis_sfpd -i apis_sfpdANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\business_rules -i business_rulesANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\car -i carANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\client_fees -i client_feesANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\client_info -i client_infoANDamadeusANDfr %ARGS%
rem call pybot -d %LOGPATH%\fr\cust_refs -i cust_refsANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\database -i databaseANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\delivery -i deliveryANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\id_traveller -i id_travellerANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\policy_check -i policy_checkANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\complete -i completeANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\pspt_and_visa -i pspt_and_visaANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\recap -i recapANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\unused_documents -i unused_documentsANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\third_party -i third_partyANDamadeus %ARGS%

rem uk test scripts
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
rem call pybot -d %LOGPATH%\uk\cust_refs -i cust_refsANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\database -i databaseANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\delivery -i deliveryANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\id_traveller -i id_travellerANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\policy_check -i policy_checkANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\pspt_and_visa -i pspt_and_visaANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\recap -i recapANDamadeusANDuk %ARGS%
call pybot -d %LOGPATH%\uk\unused_documents -i unused_documentsANDamadeusANDuk %ARGS%

rem de test scripts
call pybot -d %LOGPATH%\de\air_fare -i air_fareANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\amend -i amendANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\apis_sfpd -i apis_sfpdANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\business_rules -i business_rulesANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\car -i carANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\client_fees -i client_feesANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\client_info -i client_infoANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\complete -i completeANDamadeusANDde %ARGS%
rem call pybot -d %LOGPATH%\de\cust_refs -i cust_refsANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\database -i databaseANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\delivery -i deliveryANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\id_traveller -i id_travellerANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\policy_check -i policy_checkANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\pspt_and_visa -i pspt_and_visaANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\recap -i recapANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\unused_documents -i unused_documentsANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\third_party -i third_partyANDamadeusANDde %ARGS%
call pybot -d %LOGPATH%\de\gds -i gdsANDamadeusANDde %ARGS%

rem dk test scripts
call pybot -d %LOGPATH%\dk\air_fare -i air_fareANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\amend -i amendANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\apis_sfpd -i apis_sfpdANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\business_rules -i business_rulesANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\car -i carANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\client_fees -i client_feesANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\client_info -i client_infoANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\complete -i completeANDamadeusANDdk %ARGS%
rem call pybot -d %LOGPATH%\dk\cust_refs -i cust_refsANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\database -i databaseANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\delivery -i deliveryANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\id_traveller -i id_travellerANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\policy_check -i policy_checkANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\pspt_and_visa -i pspt_and_visaANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\recap -i recapANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\unused_documents -i unused_documentsANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\third_party -i third_partyANDamadeusANDdk %ARGS%
call pybot -d %LOGPATH%\dk\gds -i gdsANDamadeusANDdk %ARGS%

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

