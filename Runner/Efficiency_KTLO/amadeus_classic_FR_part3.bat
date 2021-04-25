set DATESTAMP=%date:~-4,4%-%date:~-10,2%-%date:~7,2%
set LOGPATH=C:\Users\u001ncb\Documents\Report\%DATESTAMP%\amadeus
set WORKSPACE=C:\Users\u001ncb\DesktopTest
rem for classic
set ARGS=-v use_mock_env:False -v version:19.4 -v syex_env:Test -v test_environment:local -e not_ready -e login_dependent -e rail_display -e apac --removekeywords WUKS Efficiency_18.10/acceptance_tests/
rem for sellco
rem set ARGS=-v use_mock_env:False -v version:19.4 -v syex_env:Test -v test_environment:local -v amadeus_env:sellco -e login_dependent -e rail_display -e apac -e resa_rail -e not_ready -e tqt_needed --removekeywords WUKS Efficiency_18.10/acceptance_tests/

chdir /d %WORKSPACE%
REM FR test scripts
call pybot -d %LOGPATH%\fr\pspt_and_visa -i pspt_and_visaANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\recap -i recapANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\unused_documents -i unused_documentsANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\price_tracking -i price_trackingANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\duo_integration -i duo_integrationANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\fr\logs -i logsANDamadeusANDfr %ARGS%
call pybot -d %LOGPATH%\ca\air_fare -i air_fareANDamadeusANDca %ARGS%


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