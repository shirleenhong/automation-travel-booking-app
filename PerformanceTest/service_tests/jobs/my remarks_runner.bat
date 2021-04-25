call locust -f ..\tests\remarks_services.py --csv=..\results\remarks_services --no-web --loglevel=DEBUG --logfile=..\results\remarks_services.log -c 840 -r 1 -t 1m
pause