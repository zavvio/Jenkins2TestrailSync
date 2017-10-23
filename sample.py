import logging
from pprint import pprint

from flows.jenkins_flow import JenkinsFlow
from flows.testrail_flow import TestRailFlow
from testrailAPI.testrail_3 import *

user = ''  # username = @hp.com email address
password = ''  # API Key - generate this via TestRail settings

# ########## Initiate TestRail API object ##########

testrail_url = 'https://testrail.tools.cso-hp.com'
client = APIClient(testrail_url)
client.user = user
client.password = password

trf = TestRailFlow(testrail_url, user, password)

# ########## Usage sample of some TestRailFlow easy methods ##########

# find a Project's ID
project_id = trf.get_project_id_by_name('MAQA')
# print(project_id)

# find the ID of a Milestone in a Project
milestone_id = trf.get_milestone_id_by_name('Android - HP Smart v4.6')
# print(milestone_id)

# find the ID of a Test Plan in a Project, and optionally in a Milestone
plan_id = trf.get_plan_id_by_name('Android - HP Smart (Automated BAT)', project_id, milestone_id)
# print(plan_id)

# retrieve all the available Configurations of a Project
configs = trf.get_configs_from_project(project_id=project_id)
# pprint(configs)

# find the ID of a Configuration by its name and optionally its group name
# config_id = trf.get_config_id_by_name(configs, 'Naples', 'Printer')
# print(config_id)

# create a list of Configuration IDs based on a list of Config names
config_ids = trf.generate_config_ids_list_by_name(configs, ['Palermo', 'Samsung Galaxy S7'])
# config_ids = trf.generate_config_ids_list_by_name(configs, ['Nexus 6P', 'Naples Super'])
# print(config_ids)

# retrieve a Test Plan based on its name
plan = client.send_get('get_plan/{}'.format(plan_id))
# pprint(plan)

# find the ID of a Test Run within a Test Plan, and optionally, for specific Configs
# run_id = trf.get_run_id_in_plan_by_name('Android - HP Smart (Automated BAT) [EN]', plan_id, config_ids)
# print(run_id)
run_id = trf.get_run_id_in_plan_by_name('Android - HP Smart (Automated BAT) [FR]', plan_id)
# print(run_id)

# Happy-path example of pulling latest BAT result from Jenkins to post it on TestRail
JOB_NAME = 'Android_AIO_Marshmallow_BAT/'  # job name on Jenkins
JF = JenkinsFlow(job_name=JOB_NAME, fixed_build='679')  # fixed_build is optional
# Sample test_case_id
sample_test_case_id = {
    'MobileApps.tests.android.aio.bat.test_suite_01_android_aio_bat_scan_tile.Test_Suite_01_Android_AiO_BAT_Scan_Tile': {
        'test_01_scan_multiple_pages': '214866',
        'test_02_scan_pdf_share_gmail': '214867',
        'test_03_scan_pdf_print_trapdoor_ui': '214868',
        'test_05_scan_pdf_save': '214869',
        'test_06_scan_jpg_save': '214870',
        'test_07_verify_existed_saved_files': '214871'
    }
}
try:
    run_id = '9999999999999'  # get this from "get_run_id_in_plan_by_name"
    test_result = JF.generate_post_data(sample_test_case_id)
    response = trf.post_results_to_test_run(run_id, test_result)
except APIError as e:
    logging.warning(' Error code - {}'.format(e.code))
    logging.warning(e)
else:
    logging.info(' Result successfully posted.')
    pprint(response)

# ########## Raw TestRail API usage sample ##########

# # find Test Suites under a specific Project
# suites = client.send_get('get_suites/{}'.format(project_id))
# pprint(suites)
#
# # find Test Cases under a specific Project>TestSuite>Section
# #       project_id of 'MAQA' = 20
# #       suite_id of 'Android - HP Smart' = 159
# case = client.send_get('get_cases/20&suite_id=159&section_id=10608')
# pprint(case)
#
# # find Test Runs of a specific Project
# runs = client.send_get('get_runs/{}'.format(project_id))
# pprint(runs)
#
# # find Test Plans of a specific Project
# plans = client.send_get('get_plans/{}'.format(project_id))
# print(len(plans))
#
# # retrieve a specific Test Plan
# #       plan_id of 'Android - HP Smart (Automated BAT)' = 2586
# plan = client.send_get('get_plan/2586')
# pprint(plan)
#
# # retrieve ALL results for all Tests under a Test Run
# #       plan_run_id of 'Android - HP Smart (Automated BAT) [FR]' = 2615
# run_results = client.send_get('get_results_for_run/2615')
# pprint(run_results)
#
# # find Tests (instance of Test Cases) under a Test Run
# tests = client.send_get('get_tests/2615')
# pprint(tests)
#
# # find all results for a Test
# #       test_case_id of 'test_01_basic_function_action_bar_option' = 86205
# test_results = client.send_get('get_results/372316')
# pprint(test_results)
#
# # retrieve a specific Test (instance of Test Case)
# #       test_id of 'test_01_basic_function_action_bar_option' = 1369099
# test = client.send_get('get_test/1369099')
# pprint(test)
