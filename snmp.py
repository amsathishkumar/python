
import telnetlib
import sys
import time
import re

PORT = '23'
HOST = 'mu-lvsb-isc-aggsw02'
usr = "gimecsystems"
pwd = "dpadliya@007"
#============= Open connection =================
tn = telnetlib.Telnet(HOST, PORT)
DEFAULT_TELNET_EXPECT_TIMEOUT = 2 

#============= Enter Commands =================

#result1 = tn.expect([r"\bUsername\b", "Password:", "#", ">"], DEFAULT_TELNET_EXPECT_TIMEOUT)
#print result1[2]
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
print host_name

