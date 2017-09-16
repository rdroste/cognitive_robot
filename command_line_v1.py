from __future__ import print_function
import requests
from requests.auth import HTTPDigestAuth
import urllib


url = 'http://212.243.230.221/rw'
auth = HTTPDigestAuth('Default User', 'robotics')

def moveSingleRobot(arm,action):

    session = requests.session()

    r0 = session.get(url + '/rapid/symbol/data/RAPID/'+arm+'/Remote/bStart?json=1',
                       auth=auth)
    print(r0)
    print(r0.text)

    r02 = session.get(url + '/rapid/symbol/data/RAPID/'+arm+'/Remote/bRunning?json=1',
                       )
    print(r02)
    print(r02.text)


    payload={'value':'"'+action+'"'}
    headers = {u'content-type': u'application/x-www-form-urlencoded'}
    r1 = session.post(url + '/rapid/symbol/data/RAPID/'+arm+'/Remote/stName?action=set',
                       data=payload,
                       headers=headers)
    print(r1)
    print(r1.text)

    r2 = session.post(url + '/rapid/symbol/data/RAPID/'+arm+'/Remote/bStart?action=set',
                       data={'value':'true'},
                       )
    print(r2)

    return;

def moveDoubleRobot(arm,action,arm2,action2):

    session = requests.session()

    r0 = session.get(url + '/rapid/symbol/data/RAPID/'+arm+'/Remote/bStart?json=1',
                       auth=auth)
    print(r0)
    print(r0.text)

    r1 = session.get(url + '/rapid/symbol/data/RAPID/'+arm2+'/Remote/bStart?json=1',
                       auth=auth)
    print(r1)
    print(r1.text)

    r02 = session.get(url + '/rapid/symbol/data/RAPID/'+arm+'/Remote/bRunning?json=1',
                       )
    print(r02)
    print(r02.text)

    r03 = session.get(url + '/rapid/symbol/data/RAPID/'+arm2+'/Remote/bRunning?json=1',
                       )
    print(r03)
    print(r03.text)


    payload={'value':'"'+action+'"'}
    headers = {u'content-type': u'application/x-www-form-urlencoded'}
    r1 = session.post(url + '/rapid/symbol/data/RAPID/'+arm+'/Remote/stName?action=set',
                       data=payload,
                       headers=headers)
    print(r1)
    print(r1.text)

    payload={'value':'"'+action2+'"'}
    headers = {u'content-type': u'application/x-www-form-urlencoded'}
    r2 = session.post(url + '/rapid/symbol/data/RAPID/'+arm2+'/Remote/stName?action=set',
                       data=payload,
                       headers=headers)
    print(r2)
    print(r2.text)

    r2 = session.post(url + '/rapid/symbol/data/RAPID/'+arm+'/Remote/bStart?action=set',
                       data={'value':'true'},
                       )
    print(r2)

    r3 = session.post(url + '/rapid/symbol/data/RAPID/'+arm2+'/Remote/bStart?action=set',
                       data={'value':'true'},
                       )
    print(r3)

    return; 


