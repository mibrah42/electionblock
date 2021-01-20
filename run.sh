# Simple script for running the necessary components.
~/redis-stable/src/redis-server &
/usr/local/Cellar/rabbitmq/3.8.9_1/sbin/rabbitmq-server &
python3 app.py &
python3 app.py 5001 &
cd client && yarn start &