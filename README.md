#  Slovakia

Question 1: Script Python

Code script getweather.py:
#!/usr/bin/env python
'''
@author: Sandro Melo

'''
import os
try:
    import pyowm
except:
    print('Big problem -> Not found modulo pyowm!',sys.exc_info()[0])
    print('This script was write to Python 3')
    sys.exit(0)

#mykey="a97e4c2f53f23fbb1ca98c3ac20288ca"
#city="dublin"

mykey=os.environ['OPENWEATHER_API_KEY']
city=os.environ['CITY_NAME']

def func_weather():
    owm = pyowm.OWM(mykey) 
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    wind = str(w.get_wind())                  
    desc = str(w.get_status())                  
    temperatura = w.get_temperature(unit='celsius') 
    temp2 = str(temperatura.get('temp','0'))
    humi = str(w.get_humidity())
    print('source=openweathrmap, ' + 'city=' + '\"' + city + '\", ' 'description=' + desc + ' temp=' + temp2 + ', ' + ' humidity=' + humi)
func_weather() 


Script test
# ./getweather.py 
source=openweathrmap, city="honolulu", decription=Rain temp=23.6,  humidity=90




Dockerfile content:
FROM sgoblin/python3.5
MAINTAINER Sandro Melo
LABEL vendor=weather:dev \
      com.example.is-beta= \
      com.example.is-production="" \
      com.example.version="0.0.1-beta" \
      com.example.release-date="2018-10-30"
WORKDIR /bin
COPY getweather.py /bin
RUN chmod +x /bin/getweather.py
RUN pip3 install --upgrade pip 
RUN pip3 install pyowm 



Create de docker
# docker build -t getweather:0.1 .
Sending build context to Docker daemon  4.711MB
Step 1/8 : FROM sgoblin/python3.5
 ---> 4c988d11a493
Step 2/8 : MAINTAINER Sandro Melo
 ---> Using cache
 ---> e9683f63c087
Step 3/8 : LABEL vendor weather:dev com.example.is-beta  com.example.is-production "" com.example.version "0.0.1-beta" com.example.release-date "2018-10-30"
 ---> Running in 209d1e5367bc


Docker created evidences :
# docker images
REPOSITORY     TAG         IMAGE ID            CREATED             SIZE
getweather     0.1         84360aaf6d84        9 seconds ago       543MB
<none>          <none>     f93c2e39d589        8 hours ago         523MB
sgoblin/python3.5   latest 4c988d11a493        6 months ago     523MB






Ansible | Syslog - Playbook created:
# cat docker_syslog.yml 

---
- name: Enable Syslog feature
  hosts: docker

  tasks:
          - name: Identify if there is the daemon.json file
            command: test -f /etc/docker/daemon.json
            register: result
            ignore_errors: yes

          - name: STOP Docker Deamon
            service:
                    name: docker
                    state: stopped

          - name: COPY daemon.json TEMPLATE
            copy:  src=/opt/ansible/files/daemon.json  dest=/etc/docker/daemon.json
            when: result.rc == 1
         
          - name: START Docker Deamon
            service:
                    name: docker
                    state: started





Evidence:

# ansible-playbook  docker_syslog.yml 

PLAY [Enable Syslog feature] ***************************************************

TASK [setup] *******************************************************************
ok: [127.0.0.1]

TASK [Identify if there is the daemon.json file] *******************************
fatal: [127.0.0.1]: FAILED! => {"changed": true, "cmd": ["test", "-f", "/etc/docker/daemon.json"], "delta": "0:00:00.002785", "end": "2018-10-30 20:33:27.405482", "failed": true, "rc": 1, "start": "2018-10-30 20:33:27.402697", "stderr": "", "stdout": "", "stdout_lines": [], "warnings": []}
...ignoring

TASK [STOP Docker Deamon] ******************************************************
changed: [127.0.0.1]

TASK [COPY daemon.json TEMPLATE] ***********************************************
changed: [127.0.0.1]

TASK [START Docker Deamon] *****************************************************
changed: [127.0.0.1]

PLAY RECAP *********************************************************************
127.0.0.1                  : ok=5    changed=4    unreachable=0    failed=0 

Validation:
# docker info | grep -i syslog
Logging Driver: syslog
WARNING: No swap limit support



Question 2 - Script to scanner host: 

Nmap module

# pip3 install python-nmap
Collecting python-nmap
  Downloading https://files.pythonhosted.org/packages/dc/f2/9e1a2953d4d824e183ac033e3d223055e40e695fa6db2cb3e94a864eaa84/python-nmap-0.6.1.tar.gz (41kB)
    100% |████████████████████████████████| 51kB 561kB/s 
Building wheels for collected packages: python-nmap
  Running setup.py bdist_wheel for python-nmap ... done
  Stored in directory: /root/.cache/pip/wheels/bb/a6/48/4d9e2285291b458c3f17064b1dac2f2fb0045736cb88562854
Successfully built python-nmap
Installing collected packages: python-nmap
Successfully installed python-nmap-0.6.1



Lib test:
python3.5
Python 3.5.3 (default, Sep 27 2018, 17:25:39) 
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import nmap
>>> ninja = nmap.PortScanner()


The code of scanner made with Python:
#!/usr/bin/env python
'''
@author: Sandro Melo
basenado em  http://xael.org/norman/python/python-nmap
NMAP integration classes and modules
'''

import sys
import os
try:
    import nmap
except:
    print('Big problem -> Not found modulo nmap:',sys.exc_info()[0])
    print('This script was write to Python 3')
    sys.exit(0)

try:
    ninja = nmap.PortScanner()
except nmap.PortScannerError:
    print('Modulo Nmap not found:', sys.exc_info()[0])
    sys.exit(0)
except:
    print('Big problem -> Unexpect Error:',sys.exc_info()[0])
    sys.exit(0)

msg_erro1="  -> Type the target address"
msg_erro2="  -> Example :  192.168.0.1 "

if len(sys.argv) != 2:
    print("#"*80)
    print(" ")
    print("Sintaxe:  python  " + (str(sys.argv[0])) + msg_erro1)
    print(" Network address Example: ")
    print(" # python  " + (str(sys.argv[0])) + msg_erro2)
    print(" ")
    print("#"*80)
    print(" ")
    sys.exit(1) 

host = sys.argv[1] 
ninja.scan(host, '1-1000')

def scantcp():
    for port in ninja[host]['tcp']:
        thisDict = ninja[host]['tcp'][port]
        print('Host: ' + host +  '    Ports: ' + str(port) + '/open/tcp////')

####
scantcp()

Evidence of test:
# scanner 10.0.2.9
Host: 10.0.2.9    Ports: 80/open/tcp////
Host: 10.0.2.9    Ports: 443/open/tcp////
Host: 10.0.2.9    Ports: 21/open/tcp////
Host: 10.0.2.9    Ports: 22/open/tcp////

Question 3 - Ansible | Rsyslogd: 

Playbook that call the role for rsyslgd:

---
# Server logs remote
- name: Config log remote server by Ansible roles
  hosts: localhost

  roles:
          - rsyslogd




Evidence playbook works:

# ansible-playbook remote_rsyslog.yml 

PLAY [Config log remote server by Ansible roles] *******************************

TASK [setup] *******************************************************************
ok: [127.0.0.1]

TASK [rsyslogd : Identify if there is the /etc/ryslog.d directory] *************
changed: [127.0.0.1]

TASK [rsyslogd : STOP Rsyslogd Deamon] *****************************************
changed: [127.0.0.1]

TASK [rsyslogd : Config the remote Server Log] *********************************
changed: [127.0.0.1]

TASK [rsyslogd : START Rsyslogd Deamon] ****************************************
ok: [127.0.0.1]

PLAY RECAP *********************************************************************
127.0.0.1                  : ok=5    changed=3    unreachable=0    failed=0   


Role Rsyslogd file:

---
# roles file for rsyslogd
- name: Identify if there is the /etc/ryslog.d directory
  command: test -d /etc/rsyslog.d
  register: result
  ignore_errors: yes

- name: STOP Rsyslogd Deamon
  service:
        name: rsyslog
        state: stopped

- name: Config the remote Server Log
  shell: echo "*.*          @10.0.0.1:514" >> /etc/rsyslog.d/logserver.log
  when: result.rc == 0
         
- name: START Rsyslogd Deamon
  service:
        name: rsyslog
        state: started


