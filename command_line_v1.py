from __future__ import print_function
import requests
from requests.auth import HTTPDigestAuth
import urllib


url = 'http://104.40.187.182/rw'
auth = HTTPDigestAuth('Default User', 'robotics')

def moveRobot(arm,action):

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



def main():


    while(1):
        print("\nWhich gesture should YuMi perform?")
        print("[1] - Wave hello")
        print("[2] - Kiss")
        print("[3] - Say no")
        print("[4] - Hand shake")
        print("[5] - I kill you")
        print("[6] - QUIT")
        print("Enter your choice [1-6]: ", end="")

        choice = int(input())
        if choice == 1:
            moveRobot('T_ROB_R','SayHello')
        elif choice == 2:
            moveRobot('T_ROB_R','Kiss')
        elif choice == 3:
            moveRobot('T_ROB_R','SayNo')
        elif choice == 4:
            moveRobot('T_ROB_R','ShakingHands')
        elif choice == 5:
            moveRobot('T_ROB_R','IKillYou')
        elif choice == 6:
            break
        else:
            print("Invalid choice!")



if __name__ == '__main__':
    main()


