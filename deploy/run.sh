python ./manage.py migrate

# kill me
# never again
touch celery.log
touch celery_beat.log

celery -A gogetter beat &> celery.log  &
celery -A gogetter worker -l info  &> celery_beat.log  &

python ./manage.py runserver 0.0.0.0:8888

#tail -f /dev/null