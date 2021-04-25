set DATESTAMP=%date:~-4,4%-%date:~-10,2%-%date:~7,2%
set LOGPATH="C:\Users\u004hxc\Documents\Report\%DATESTAMP%"
set WORKSPACE="C:\Users\u004hxc\Documents\CWT Automation - New Trunk\DesktopTest"
set PORTNUMBER=8270
set ENV=local
set VERSION=17.8

chdir /d %WORKSPACE%
REM Non-Citi
call pybot -d %LOGPATH%\galileo\amend -v port:%PORTNUMBER% -v version:%VERSION% -v test_environment:%ENV% -i amendANDgalileoANDapac -e citi -e not_ready -e rail trunk/acceptance_tests/
call pybot -d %LOGPATH%\galileo\air_fare -v port:%PORTNUMBER% -v version:%VERSION% -v test_environment:%ENV% -i air_fareANDgalileoANDapac -e citi  -e not_ready -e rail trunk/acceptance_tests/
call pybot -d %LOGPATH%\galileo\client_info -v port:%PORTNUMBER% -v version:%VERSION% -v test_environment:%ENV% -i client_infoANDgalileoANDapac -e citi  -e not_ready -e rail trunk/acceptance_tests/
call pybot -d %LOGPATH%\galileo\complete -v port:%PORTNUMBER% -v version:%VERSION% -v test_environment:%ENV% -i completeANDgalileoANDapac -e citi  -e not_ready -e rail trunk/acceptance_tests/
call pybot -d %LOGPATH%\galileo\database -v port:%PORTNUMBER% -v version:%VERSION% -v test_environment:%ENV% -i databaseANDgalileoANDapac -e citi  -e not_ready -e rail trunk/acceptance_tests/
call pybot -d %LOGPATH%\galileo\cust_refs -v port:%PORTNUMBER% -v version:%VERSION% -v test_environment:%ENV% -i cust_refsANDgalileoANDapac -e citi  -e not_ready -e rail trunk/acceptance_tests/
call pybot -d %LOGPATH%\galileo\delivery -v port:%PORTNUMBER% -v version:%VERSION% -v test_environment:%ENV% -i deliveryANDgalileoANDapac -e citi  -e not_ready -e rail trunk/acceptance_tests/
call pybot -d %LOGPATH%\galileo\gds -v port:%PORTNUMBER% -v version:%VERSION% -v test_environment:%ENV% -i gdsANDgalileoANDapac -e not_ready -e citi -e rail trunk/acceptance_tests/
call pybot -d %LOGPATH%\galileo\id_traveller -v port:%PORTNUMBER% -v version:%VERSION% -v test_environment:%ENV% -i id_travellerANDgalileoANDapac -e citi -e not_ready -e rail trunk/acceptance_tests/
call pybot -d %LOGPATH%\galileo\recap -v port:%PORTNUMBER% -v version:%VERSION% -v test_environment:%ENV% -i recapANDgalileoANDapac -e not_ready -e citi -e rail trunk/acceptance_tests/
call pybot -d %LOGPATH%\galileo\third_party -v port:%PORTNUMBER% -v version:%VERSION% -v test_environment:%ENV% -i third_partyANDgalileoANDapac -e citi -e not_ready -e rail trunk/acceptance_tests/

REM Citi
call pybot -d %LOGPATH%\galileo\citi_air_fare -v port:%PORTNUMBER% -v version:%VERSION% -v test_environment:%ENV% -i galileoANDapacANDcitiANDair_fare -e not_ready -e rail trunk/citi/acceptance_tests/
call pybot -d %LOGPATH%\galileo\citi_gds -v port:%PORTNUMBER% -v version:%VERSION% -v test_environment:%ENV% -i galileoANDapacANDcitiANDgds -e not_readyANDapac -e rail trunk/citi/acceptance_tests/
call pybot -d %LOGPATH%\galileo\citi_amend -v port:%PORTNUMBER% -v version:%VERSION% -v test_environment:%ENV% -i galileoANDapacANDcitiANDamend -e not_readyANDapac -e rail trunk/citi/acceptance_tests/
call pybot -d %LOGPATH%\galileo\citi_cust_refs -v port:%PORTNUMBER% -v version:%VERSION% -v test_environment:%ENV% -i galileoANDapacANDcitiANDcust_refs -e not_readyANDapac -e rail trunk/citi/acceptance_tests/
call pybot -d %LOGPATH%\galileo\citi_bsp_emd -v port:%PORTNUMBER% -v version:%VERSION% -v test_environment:%ENV% -i galileoANDapacANDcitiANDbsp_emd -e not_readyANDapac -e rail trunk/citi/acceptance_tests/

copy /s /y %WORKSPACE%\result_extractor_excel.py %LOGPATH%\galileo\
chdir /d %LOGPATH%\galileo\
call result_extractor_excel.py

chdir /d %WORKSPACE%
call pybot -d %LOGPATH%\pnr_canceller\galileo -v version:%VERSION% -v test_environment:%ENV% -i pnr_cancellerANDgalileo trunk/pnr_canceller/


pause()