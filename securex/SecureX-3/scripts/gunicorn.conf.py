# import multiprocessing

pidfile = 'flask_app.pid'
workers = 2
# workers = multiprocessing.cpu_count() * 2 + 1
bind = '0.0.0.0:80'
accesslog = './logs/access.log'
errorlog = './logs/error.log'
#certfile = './certs/local.cer'
#keyfile = './certs/local.key'
# user = 'ubuntu'
# group = 'ubuntu'