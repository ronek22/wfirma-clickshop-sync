# wfirma-clickshop-sync
## About project
Web app made for inventory synchronize between WFirma and Clickshop
After client made some chagnes in WFirma there have to be reflectd in all clickshop shops added to app.
Variants of products can't be updated by Rest API provided by Clickshop, but I created solution to that problem based on selenium.

## Technology Stack
Technology | Role
:-------------------------:|:-------------------------:
Python  |  backend language
Django | backend framework
JINJA | Django template engine
HTML/CSS/JS/Bootstrap | frontend - no framework in use
Nginx | High performance web server
Redis | storing celery tasks
Celery | async solution for django
Postgres | RBDMS
Selenium | update product variants
Docker | containerize app
