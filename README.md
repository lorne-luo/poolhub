Getting started
===============

1. Clone project `git clone git@git.butterfly.com.au:django/example.git`
2. `cd example`
3. Setup virtualenv `/bin/bash ./shell.sh setupenv`
4. Run server `/bin/bash ./shell.sh runserver`
5. That's it. Your server URL will be at YOUR-DEV-DOMAIN.butterfly.com.au:8000
6. Some settings value can be change by creating .env file in your project root. Example. You may want to change BASE_URL and DATABASE_URL when settings up your local.
7. run `python manage.py init` will create a superuser with `butterflynet@butterfly.com.au / But3as2flying` if no superuser exist

Environment Variables
===============
- DATABASE_URL
- BASE_URL
- DEBUG: default is False
- ADMINS: admin's email, separate by comma
- SECRET_KEY: longrandom string
- AWS_STORAGE_BUCKET_NAME
- AWS_S3_REGION_NAME: default is ap-southeast-2
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY

See docs/ for more 
