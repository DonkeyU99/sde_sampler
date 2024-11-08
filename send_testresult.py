import requests
import os
import json
import xml.etree.ElementTree as ET

#TEST2

CHATID = ''  # chat id of OOD in Latent Space
JENKINS = ''
JOBNAME = 'run-test-sde-sampler'

def send_to_telegram(msg):
    """send message to telegram channel"""
    global CHATID
    BOTTOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    print(BOTTOKEN)
    url = f'https://api.telegram.org/bot{BOTTOKEN}/sendMessage'
    payload = {'chat_id': CHATID, 'text': f'{msg}'}
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r)


def parse_test_result(file_testresult):
    tree = ET.parse(file_testresult)
    testsuite = tree.find('testsuite')
    n_error = int(testsuite.get('errors'))
    n_failure = int(testsuite.get('failures'))
    n_skipped = int(testsuite.get('skipped'))
    n_test = int(testsuite.get('tests'))
    time = float(testsuite.get('time'))
    if n_error == 0 and n_failure == 0:
        txt_allpass = ' - ALL TEST PASSED'
    else:
        txt_allpass = ' - SOMETHING WRONG'
    txt_result = f'{n_error} Errors, {n_failure} Failures, {n_skipped} Skips {txt_allpass}\n' +\
                 f'{n_test} Tests run for {time:.1f} sec\n' +\
                 f'Visit: {JENKINS}/{JOBNAME}/'
    return txt_result


def send_test_result():
    txt_result = "TEST"#parse_test_result('testresult.xml')
    send_to_telegram(txt_result)

if __name__ == '__main__':
    send_test_result()