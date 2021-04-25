call locust -f ..\tests\apac_services.py --csv=..\results\apac_services --no-web --loglevel=DEBUG --logfile=..\results\apac_services.log -c 1000 -r 1 -t 360m
pause