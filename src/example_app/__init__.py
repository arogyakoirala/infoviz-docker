from flask import Flask, request
import os

app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>CALCentral Task API</h1>'


@app.route('/status', methods=['GET'])
def status(): 
    args = request.args

    UID = args.get('UID')
    CLCODE = args.get('CLCODE')
    CLITEM = args.get('CLITEM')
    # STCODE = args.get('STCODE')
    status = os.popen(f'python getter.py -s {UID} -c {CLCODE} -i {CLITEM}').read()
    os.system(f'python chupdummy.py {UID} {CLCODE} {CLITEM} {status}')
    return status

@app.route('/chup', methods=['GET'])
def chup():
    args = request.args

    UID = args.get('UID')
    CLCODE = args.get('CLCODE')
    CLITEM = args.get('CLITEM')
    STCODE = args.get('STCODE')

    os.system(f'python chupdummy.py {UID} {CLCODE} {CLITEM} {STCODE}')
    result = os.popen(f'python chup.py -s {UID} -c {CLCODE} -i {CLITEM} -x {STCODE}').read()
    return result