call locust -f ..\tests\remarks_services.py --csv=..\results\remarks_services --no-web --loglevel=DEBUG --logfile=..\results\remarks_services.log -c 1000 -r 1 -t 360m
pause