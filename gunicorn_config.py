# Source: https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py

import os
import threading
import sys
import traceback

port_number = 5000
bind = "0.0.0.0:{}".format(port_number)
backlog = 2048
workers = int(os.environ.get('GUNICORN_NUMBER_WORKERS', 3))
worker_class = 'sync'
worker_connections = 1000
timeout = 600
keepalive = 2
spew = False
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

errorlog = '-'
loglevel = 'info'
accesslog = '-'
access_log_format = '%({X-Real-IP}i)s - - - %(t)s "%(r)s" "%(f)s" "%(a)s" %({X-Request-Id}i)s %(L)s %(b)s %(s)s'
proc_name = 'api'


def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def pre_fork(server, worker):
    pass


def pre_exec(server):
    server.log.info("Forked child, re-executing.")


def when_ready(server):
    server.log.info("Server is ready. Spawning workers")


def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

    # get traceback info
    id2name = {th.ident: th.name for th in threading.enumerate()}
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId, ""),
                                            threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                                                        lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))


def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")