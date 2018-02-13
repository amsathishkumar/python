from multiprocessing import Process
import datetime
from multiprocessing import Pool
import paramiko
import subprocess
import os
from pysnmp.entity.rfc3413.oneliner import cmdgen
import mail
import telnetlib
import re

#rootdir = "D:\\NetworkAudit\\Rancid\\router.db"
rootdir = "/home/tools/sathish/router.db"

def allConfig(vender):
    hostsdic = {}
    f = open(rootdir)
    for line in iter(f):
        line = line.lower()
        if ((vender in line) and (len(line.strip().split(":")[0])> 0)):
           hostsdic[line.strip().split(":")[0]]={"ping":"0","snmp":"0","ssh":"0"}
    return hostsdic

def count(allhosts):
    ctdic = { "ping":0, "snmp":0, "ssh":0, "fping":0, "fsnmp":0, "fssh":0}
    for hostname, hostoprs in allhosts.items():
        for hostopr, value in hostoprs.items():
            if (hostopr == "ping" and value == 1):
                ctdic["ping"] = ctdic["ping"] + 1
            if hostopr == "snmp" and value == 1:
                ctdic["snmp"] = ctdic["snmp"] + 1
            if hostopr == "ssh" and value == 1:
                ctdic["ssh"] = ctdic["ssh"]+ 1
            if (hostopr == "ping" and value == 0):
                ctdic["fping"] = ctdic["fping"] + 1
            if hostopr == "snmp" and value == 0:
                ctdic["fsnmp"] = ctdic["fsnmp"] + 1
            if hostopr == "ssh" and value == 0:
                ctdic["fssh"] = ctdic["fssh"]+ 1

    return ctdic

def pinghost(hostname):
    #print('The name of host is : ', hostname)
    res = subprocess.call(['ping', '-c', '2', '-W', '1', hostname],stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
    if res == 0:
        #print("ping to", hostname, "OK")
        res1 = 1
    elif res == 2:
        #print("no response from", hostname)
        res1 = 0
    else:
        #print("ping to", hostname, "failed!")
        res1 = 0
    return res1

def sshhost(hostname):
    usr = "gimecsystems"
    pwd = "dpadliya@007"
    try:
        paramiko.util.log_to_file ('paramiko.log')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=usr, password=pwd,look_for_keys=False,timeout=6)
        #print("ssh to "+hostname + "OK")
        return 1
    except:
        if telnethost(hostname) == 1:
           return 1
        else:
           #print("ssh to "+hostname+"failed!")
           return 0

def snmphost(hostname):
    #[tools@gimec-mum-s1 cpuscripts]$/usr/bin/snmpwalk -v 2c -c t7t7m1tr01 192.168.228.7 1.3.6.1.4.1.9.2.1.57
    #SNMPv2-SMI::enterprises.9.2.1.57.0 = INTEGER: 19
    try:
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData('t7t7m1tr01'),
        cmdgen.UdpTransportTarget((hostname, 161)),'1.3.6.1.4.1.9.2.1.57.0')
    except:
        #print("snmp to "+hostname+"failed!")
        return 0
    if errorIndication:
       #print("snmp to "+hostname+"failed!")
       #print(errorIndication)
       return 0
    else:
       if errorStatus:
          #print("snmp to "+hostname+"failed!")
          #print('%s at %s' % (
          #errorStatus.prettyPrint(),
          #errorIndex and varBinds[int(errorIndex)-1] or '?'
          #)
          #)
          return 0
       else:
           #print("snmp to "+hostname + "OK")
           #for name, val in varBinds:
           #    print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
           return 1

def telnethost(host):
    PORT = '23'
    usr = "gimecsystems"
    pwd = "dpadliya@007"
    try:
       #============= Open connection =================
       tn = telnetlib.Telnet(host, PORT)
       DEFAULT_TELNET_EXPECT_TIMEOUT = 2
       #============= Enter Commands =================
       tn.expect(["username:"], DEFAULT_TELNET_EXPECT_TIMEOUT)
       tn.write("{0}".format(usr))
       tn.write("\n")
       tn.expect(["Password:"], DEFAULT_TELNET_EXPECT_TIMEOUT)
       tn.write("{0}".format(pwd))
       tn.write("\n")
       tn.write("\n")
       tn.expect(["#"], DEFAULT_TELNET_EXPECT_TIMEOUT)
       tn.write("\n")
       host_name = tn.read_until("#")
       host_name = re.sub('[!#@$?]', '', host_name)
       #print host_name
       if host == host_name:
          return 1
       else:
          return 0
    except:
          return 0

if __name__ == "__main__":
    now = datetime.datetime.now()
    print (str(now))
    venderlist = ["cisco","alcatellucent","juniper","huawei"]
    hbody = "<h2> Count Detals </h2>"
    for vender in venderlist:
        print("vender Start: "+ vender)
        vcount = 0
        hbody = hbody + "<h3>Vender:" + vender + "</h3>"
        allhosts = allConfig(vender)
        for hostname, hostoprs in allhosts.items():
            vcount = vcount + 1
            for hostopr, value in hostoprs.items():
                if hostopr == "ping":
                   hostoprs[hostopr] = pinghost(hostname)
                if hostopr == "snmp":
                   hostoprs[hostopr] = snmphost(hostname)
                if hostopr == "ssh":
                   hostoprs[hostopr] = sshhost(hostname)

        print(allhosts)
        countdic=count(allhosts)
        hbody = hbody + "<table border=1 cellpadding = '5' cellspacing = '5'><tr><td>Total host</td><td>"+str(len(allhosts))+"</td></tr> <tr><td>Total ping host</td><td>"+ str(countdic["ping"])+"</td><td>"+ str(countdic["fping"])+"</td></tr> <tr> <td>Total snmp host:</td><td>"+ str(countdic["snmp"])+"</td><td>"+str(countdic["fsnmp"])+"</td></tr><tr><td>Total ssh host</td><td>"+ str(countdic["ssh"])+"</td><td>"+ str(countdic["fssh"])+"</td></tr></table>" 
        #print("Total host:"+ str(len(allhosts)))
        #print("Total ping host:" + str(countdic["ping"]))
        #print("Total snmp host:" + str(countdic["snmp"]))
        #print("Total ssh host:" + str(countdic["ssh"]))
    print(hbody)
    now = datetime.datetime.now()
    print (str(now))

