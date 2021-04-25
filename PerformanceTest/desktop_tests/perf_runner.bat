rem set DATESTAMP=%date:~-4,4%-%date:~-10,2%-%date:~7,2%
rem set LOGPATH="C:\Users\U001JCP\TFS\PowerExpressTestAutomation\DesktopTest\PerformanceTest\Logs\%DATESTAMP%"
rem set WORKSPACE="C:\Users\U001JCP\TFS\PowerExpressTestAutomation\DesktopTest\PerformanceTest\"
rem set ARGS= -v version:18.10 -v syex_env:Test -v test_environment:local --removekeywords WUKS desktop_tests

rem HK test scripts
rem chdir /d %WORKSPACE%
call pybot --test Perf -v version:18.10 -v surname:BEAR -v firstname:HKOTHERS apac.txt
pause