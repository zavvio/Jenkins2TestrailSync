import urllib
import ast

from testrailAPI.backup.testrail import *


client = APIClient('https://jiracso.testrail.net')
client.user = 'ho-lun-zavvio.mok@hp.com'
client.password = '3HI/BnjdpLGdkHIjdzC2-mnEkT3LbEZQTUPvF.P4x'  # API Key

# case = client.send_get('get_projects')
# case = client.send_get('get_suites/20')  # project_id of MAQA = 20
# case = client.send_get('get_cases/20&suite_id=159&section_id=10608')  # suite_id of 'Android - HP Smart' = 159
# pprint(case)


########## Parsing test result from Jenkins (Android - HP Smart - BAT - Latest Results) ##########

JENKINS_IP_ADDR = 'http://15.98.72.76:8080/job/'
JOB_NAME = 'Android_AIO_Marshmallow_BAT/'
RESULTS_ADDR = '/testReport/api/python?pretty=true'

LATEST_BAT_RESULTS = 'lastCompletedBuild'
FIXED_BUILD_RESULTS = '632'

FULL_URL = JENKINS_IP_ADDR + JOB_NAME + LATEST_BAT_RESULTS + RESULTS_ADDR
FIXED_URL = JENKINS_IP_ADDR + JOB_NAME + FIXED_BUILD_RESULTS + RESULTS_ADDR

print("Fetching results: {}".format(FULL_URL))

result = ast.literal_eval(urllib.urlopen(FULL_URL).read())
print urllib.urlopen(FULL_URL).read()
# pprint(result)
print len(result['suites'][0]['cases'])
for case in result['suites'][0]['cases']:
    className = case['className'].split('.')
    if case['name'][:4] == 'test':
        print str(className[-3:]) + ' --- ' + case['name'] + ': ' + ('PASS' if case['status'] == 'PASSED' else 'FAIL')