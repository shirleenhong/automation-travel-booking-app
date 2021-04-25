set DATESTAMP=%date:~-4,4%-%date:~-10,2%-%date:~7,2%
set LOGPATH="C:\Users\uexr493\Documents\CWT Projects\4.0 PsyEx\PsyEx TFS Workspace Map\PowerExpress\DesktopTest\Logs\%DATESTAMP%"
set WORKSPACE="C:\Users\uexr493\Documents\CWT Projects\4.0 PsyEx\PsyEx TFS Workspace Map\PowerExpress\DesktopTest"
set ARGS=-v use_mock_env:False -v version:19.2 -v syex_env:Test -v test_environment:local -e not_ready -e obsolete --removekeywords WUKS trunk/tpro/acceptance_tests/

rem HK test scripts
chdir /d %WORKSPACE%

call python sellco_login.py
call pybot -d %LOGPATH%\HK\BSP\other_services -i other_servicesANDhkANDbsp_ticket %ARGS%
call python sellco_login.py
call pybot -d %LOGPATH%\HK\other_services -i other_servicesANDhkANDbusiness_scenarios %ARGS%
call python sellco_login.py
call pybot -d %LOGPATH%\HK\Car Transfer\other_services -i other_servicesANDhkANDcar_transfer %ARGS%
call python sellco_login.py
call pybot -d %LOGPATH%\HK\Consolidator\other_services -i other_servicesANDhkANDconsolidator_ticket_and_lcc %ARGS%
call python sellco_login.py
call pybot -d %LOGPATH%\HK\Insurance\other_services -i other_servicesANDhkANDinsurance %ARGS%
call python sellco_login.py
call pybot -d %LOGPATH%\HK\Multiple EO\other_services -i other_servicesANDhkANDmultiple_exchange_order %ARGS%
call python sellco_login.py
call pybot -d %LOGPATH%\HK\Train\other_services -i other_servicesANDhkANDtrain_and_ferry %ARGS%
call python sellco_login.py
call pybot -d %LOGPATH%\HK\Trasaction\other_services -i other_servicesANDhkANDtransaction_fee %ARGS%
call python sellco_login.py
call pybot -d %LOGPATH%\HK\VisaPro\other_services -i other_servicesANDhkANDvisa_processing %ARGS%
call python sellco_login.py
call pybot -d %LOGPATH%\HK\WithoutGst\other_services -i other_servicesANDhkANDwithout_gst %ARGS%
call python sellco_login.py
call pybot -d %LOGPATH%\HK\HotelInfo\other_services -i other_servicesANDhkANDhotel_info %ARGS%

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