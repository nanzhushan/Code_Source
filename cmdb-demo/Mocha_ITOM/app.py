import re

from flask import request, abort

from oms import create_app, IP_WHITE_LIST

app = create_app("production")  # 生产模式


@app.before_request
def ip_process():
    """ip处理"""
    ip = request.remote_addr
    for i, _ip in enumerate(IP_WHITE_LIST):
        if not re.match(_ip, ip):
            if len(IP_WHITE_LIST) - 1 == i:
                abort(403)
                return
        else:
            break


if __name__ == '__main__':
    app.run()
