import constant
import logging
from pprint import pprint
from jenkins_flow import JenkinsFlow
from testrail_3 import *
from testrail_flow import TestRailFlow

user = 'ho-lun-zavvio.mok@hp.com'
password = '3HI/BnjdpLGdkHIjdzC2-mnEkT3LbEZQTUPvF.P4x'  # API Key
trf = TestRailFlow(user=user, password=password)

client = APIClient('https://jiracso.testrail.net')
client.user = 'ho-lun-zavvio.mok@hp.com'
client.password = '3HI/BnjdpLGdkHIjdzC2-mnEkT3LbEZQTUPvF.P4x'  # API Key

projects_id = trf.get_project_id_by_name('MAQA')
milestone_id = trf.get_milestone_id_by_name('Android - HP Smart v4.6')

# case = client.send_get('get_suites/{}'.format(projects_id))
# suite_id of 'Android - HP Smart' = 159
# case = client.send_get('get_cases/20&suite_id=159&section_id=10608')
# pprint(case)
# print(constant.test_status)
# runs = client.send_get('get_runs/{}'.format(projects_id))
# pprint(runs)
# plans = client.send_get('get_plans/{}'.format(projects_id))
# print(len(plans))
plan_id = trf.get_plan_id_by_name('Android - HP Smart (Automated BAT)', projects_id, milestone_id)
# print(plan_id)
plan = client.send_get('get_plan/2586')
# pprint(plan)
# run = client.send_get('get_results_for_run/2615')
tests = client.send_get('get_tests/2615')
# pprint(tests)
# client.send_get('get_results/52101')
# test = client.send_get('get_test/1369099')
# pprint(test)
# result = client.send_get('get_results/372316')
# pprint(result)

run_id = str(2615)
case_id = 86205
# test_result = {
#         "results": [
#             {
#                 "case_id": 86205,
#                 "status_id": 5,
#                 "comment": "This test failed"
#             },
#             {
#                 "case_id": 9999999999999,
#                 "status_id": 4,
#                 "comment": "This test needs retest",
#                 "elapsed": "1s",
#                 "version": "4.6.001"
#             }
#         ]
#     }
JF = JenkinsFlow(fixed_build='679')
test_result = JF.generate_post_data()

try:
    response = client.send_post('add_results_for_cases/'+run_id, test_result)
except APIError as e:
    logging.warning('Error - {}'.format(e.code))
    logging.warning(e)
else:
    logging.info('Result successfully posted.')
    pprint(response)
logging.info('DONE.')
