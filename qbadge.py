from flask import Flask
from flask import send_file
import requests
from StringIO import StringIO
import os
import re


BADGE_URL = 'https://img.shields.io/badge/{0}-{1}-{2}.svg?style=flat'
STATUS_HOME = '../stati/'
PERCENT_RE = re.compile(r"(\d+)\.?(\d+)?%")


def _decode_percentage(input_string):
    v = -1
    c = 'lightgray'
    m = PERCENT_RE.search(input_string)
    if m:
        v = int(m.group(1))
    if 0 <= v <= 20:
        c = 'red'
    elif 21 <= v <= 40:
        c = 'orange'
    elif 41 <= v <= 60:
        c = 'yellow'
    elif 61 <= v <= 80:
        c = 'yellogreen'
    elif 81 <= v <= 90:
        c = 'green'
    elif 91 <= v:
        c = 'brightgreen'
    if v >= 0:
        status_text = "{0:d}%".format(v)
    else:
        status_text = "unknown"
    return status_text, c


def _decode_passfail(input_string, show_amount=False):
    if input_string.strip() in ["0", ""]:
        return "passing", 'brightgreen'
    else:
        return "failing [{0}]".format(input_string.strip()) if show_amount else "failing", 'red'


def _decode_annotated_passfail(input_string):
    return _decode_passfail(input_string, True)


def _decode_info(input_string):
    return input_string.strip(), "blue"


METRIC_TYPES = {
    'percentage': _decode_percentage,
    'passfail': _decode_passfail,
    'annotated-passfail': _decode_annotated_passfail,
    'info': _decode_info,
}


CONFIGURED_TYPES = {'coverage': 'percentage',
                    'flake8': 'annotated-passfail',
                    'version': 'info'}


app = Flask(__name__)


def _compute_badge(project_name, status_name):
    fname = os.path.join(STATUS_HOME, project_name, status_name)
    status_text = 'unknown'
    status_color = 'lightgray'
    if os.path.exists(fname):
        with file(fname, 'rt') as f:
            lines = f.readlines()
            if len(lines):
                if status_name in CONFIGURED_TYPES.keys():
                    status_text, status_color = METRIC_TYPES[CONFIGURED_TYPES[status_name]](lines[-1])
                else:
                    status_text = lines[-1].strip()
    return BADGE_URL.format(status_name, status_text, status_color)


@app.route('/')
def home_page():
    return 'internal badge maker / forwarder using shield.io'


@app.route('/status/<project>/<status>')
def status_badge(project, status):
    r = requests.get(_compute_badge(project, status))
    image = StringIO(r.content)
    return send_file(image, mimetype=r.headers['Content-Type'])


if __name__ == '__main__':
    app.config.from_object('local_settings')
    app.run(host=app.config.get("HOST", "localhost"),
            port=app.config.get("PORT", "9000")
            )
