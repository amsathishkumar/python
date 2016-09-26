'''
Created on Sep 23, 2016

@author: smuniapp
'''
import requests

class TestClassA:
    def test_1(self):        
        print "test A1 called"
        r = requests.get("http://localhost:5600/requestlist")
        print r.status_code
        print r.json()
        
    def test_2(self):
        print "test A2 called"
        r = requests.post("http://localhost:5600/sat")
        print r.status_code
        print r.json()
        

class TestClassB:
    def test_1(self):
        print "test B1 called"