import logging
import pprint
from flows.jenkins_flow import JenkinsFlow
from flows.testrail_flow import TestRailFlow
from resource import config_android_smart_bat as CFG
from testrailAPI.testrail_3 import *

# ########## Initiate TestRail API object ##########

client = APIClient(CFG.TESTRAIL_LINK)
client.user = CFG.USERNAME
client.password = CFG.PASSWORD

trf = TestRailFlow(CFG.TESTRAIL_LINK, client.user, client.password)

# ########## Usage sample of some TestRailFlow easy methods ##########

# find a Project's ID
project_id = trf.get_project_id_by_name(CFG.PROJECT)
# find the ID of a Milestone in a Project; this field is OPTIONAL
milestone_id = trf.get_milestone_id_by_name(CFG.MILESTONE)

# retrieve all the available Configurations of a Project
configs = trf.get_configs_from_project(project_id=project_id)
# create a list of Configuration IDs based on a list of Config names
config_ids = trf.generate_config_ids_list_by_name(configs, CFG.CONFIGS)

# find the ID of a Test Plan in a Project, and optionally in a Milestone
plan_id = trf.get_plan_id_by_name(CFG.TEST_PLAN, project_id, milestone_id)
# find the ID of a Test Run within a Test Plan, and optionally, for specific Configs
run_id = trf.get_run_id_in_plan_by_name(CFG.TEST_RUN, plan_id, config_ids)

# Happy-path example of pulling latest BAT result from Jenkins to post it on TestRail
JF = JenkinsFlow(job_name=CFG.JENKINS_JOB)
try:
    test_result = JF.generate_post_data(CFG.test_case_id)
    response = trf.post_results_to_test_run(run_id, test_result)
except APIError as e:
    logging.warning(' Error code - {}'.format(e.code))
    logging.warning(e)
else:
    logging.info(' Result successfully POSTed.')
    logging.info(' POST Response >>\n' + pprint.pformat(response))
