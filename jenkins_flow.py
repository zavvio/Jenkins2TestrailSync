import ast
import urllib.request
from urllib.error import HTTPError

""" Parsing test result from Jenkins (Android>HP Smart>BAT>Latest Results) """
# Fixed address fields
JENKINS_IP_ADDR = 'http://15.98.72.76:8080/job/'
BUILD_ADDR = ''
RESULTS_ADDR = '/testReport'
API_ADDR = '/api/python?pretty=true'
LATEST_BAT_RESULTS = 'lastCompletedBuild'

# Customizable address field
JOB_NAME = 'Android_AIO_Marshmallow_BAT' + '/'
FIXED_BUILD_RESULTS = '632'

# Composed URLs
LATEST_BAT_BUILD = JENKINS_IP_ADDR + JOB_NAME + LATEST_BAT_RESULTS + BUILD_ADDR + API_ADDR
LATEST_BAT_RESULTS = JENKINS_IP_ADDR + JOB_NAME + LATEST_BAT_RESULTS + RESULTS_ADDR + API_ADDR
FIXED_BAT_RESULTS = JENKINS_IP_ADDR + JOB_NAME + FIXED_BUILD_RESULTS + RESULTS_ADDR + API_ADDR

GOOD_STATUS = ("PASSED", "FIXED")

# resp = requests.get(LATEST_BAT_RESULTS).text
try:
    resp = urllib.request.urlopen(LATEST_BAT_RESULTS).read().decode("utf-8")
except HTTPError:
    print("Test build failed, not parsing test results.")
else:
    result = ast.literal_eval(resp)
    # pprint(result)
    print(len(result['suites'][0]['cases']))
    for case in result['suites'][0]['cases']:
        className = case['className'].split('.')
        if case['name'][:4] == "test":
            status_mod = "PASS" if case['status'] in GOOD_STATUS else "FAIL"
            print(str(className[-3:]) + " --- " + case['name'] + ": " +
                  case['status'] + " => " + status_mod)
