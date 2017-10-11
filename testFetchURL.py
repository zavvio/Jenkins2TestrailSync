import constant
from pprint import pprint
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
plan_id = trf.get_plan_id_by_name('Android - HP Smart [Automated BAT]', projects_id, milestone_id)
# print(plan_id)
plan = client.send_get('get_plan/2586')
pprint(plan)