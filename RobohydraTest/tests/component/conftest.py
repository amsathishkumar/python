'''
Created on Sep 23, 2016

@author: smuniapp
'''
import pytest
import subprocess
import time

def tear_down():
    print "\nTEARDOWN after all tests"

@pytest.fixture(scope="session", autouse=True)
def set_up(request):
    print "\nSETUP before all tests"
    cmd = "node node_modules/robohydra/bin/robohydra.js -I robo/ -n -P sat_mock -p 5600"
    proc=subprocess.Popen(cmd)
    time.sleep(5)
    def fin():
        proc.kill()
    request.addfinalizer(fin)
