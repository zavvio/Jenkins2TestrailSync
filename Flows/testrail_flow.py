import logging
from TestRailAPI.testrail_3 import *


class TestRailFlow(object):
    """ General flows for TestRail

    """
    def __init__(self, user, password):
        """ Initialize APIClient

        :param user: username, should be your @hp email address
        :param password: API key, generate it via TestRail settings
        """
        logging.basicConfig(level=logging.INFO)
        self.client = APIClient('https://jiracso.testrail.net')
        self.client.user = user
        self.client.password = password

    @staticmethod
    def search_name_in_response(response, name, target):
        for r in response:
            if r['name'] == name:
                logging.info(" Found {} [{}]: id={}".format(target.lower(), name, r['id']))
                return str(r['id'])
        logging.warning(" {} [{}] not found.".format(target, name))
        return None

    def get_project_id_by_name(self, name='MAQA'):
        """ Find the id of a project based on its name

        :param name: name of the project
        :return: if found, id of the project; else, None
        """
        target = 'Project'
        resp = self.client.send_get('get_projects')
        return self.search_name_in_response(resp, name, target)

    def get_milestone_id_by_name(self, name='Android - HP Smart v4.6',
                                 project_id='20'):
        """ Find the id of a milestone based on its name
        Note: MAQA project id = 20
        :param name: name of the milestone
        :param project_id: project id of which the milestone is in
        :return: if found, id of the milestone; else, None
        """
        target = 'Milestone'
        resp = self.client.send_get('get_milestones/{}'.format(project_id))
        return self.search_name_in_response(resp, name, target)

    def get_plan_id_by_name(self, name, project_id, milestone_id=''):
        """ Find the id of a test plan based on its name

        :param name: name of the test plan
        :param project_id: id of the project which contains the test plan
        :param milestone_id: id of the milestone which contains the test plan
        :return: if found, id of the test plan; else, None
        """
        target = 'Test plan'
        request = 'get_plans/{}&is_completed=0'.format(project_id)
        if milestone_id != '':
            request += '&milestone_id={}'.format(milestone_id)
        resp = self.client.send_get(request)
        return self.search_name_in_response(resp, name, target)

    def get_configs_from_project(self, project_id):
        """ Get all the Configurations of a Project

        :param project_id: id of a Project
        :return: raw response of the Configs from TestRail API
        """
        return self.client.send_get('get_configs/{}'.format(project_id))

    @staticmethod
    def get_config_id_by_name(configs_resp, config_name, group_name=''):
        """ Find the ID of a Configuration based on its name[, and group name]

        :param configs_resp: the raw response data structure from TestRail API for
                        Configs, use method "get_configs_from_project"
        :param config_name: name of the target Configuration, e.g. Palermo
        :param group_name: name of the target Configuration's group e.g. Printer
        :return: if found, ID of the target Configuration
        """
        if group_name == '':
            for group in configs_resp:
                g_configs = group['configs']
                for g_config in g_configs:
                    # print(g_config['name'])
                    if config_name == g_config['name']:
                        logging.info(">> Found config '{}', ID = {}".format(g_config['name'], g_config['id']))
                        return g_config['id']
        else:
            for group in configs_resp:
                if group_name == group['name']:
                    g_configs = group['configs']
                    for g_config in g_configs:
                        # print(g_config['name'])
                        if config_name == g_config['name']:
                            logging.info(">> Found config '{}', ID = {}".format(g_config['name'], g_config['id']))
                            return g_config['id']
        if group_name != '':
            logging.warning(">> Unable to find config {} > {}".format(group_name, config_name))
        else:
            logging.warning(">> Unable to find config {}".format(config_name))
        return None

    def generate_config_ids_list_by_name(self, configs_resp, configs):
        """ Construct a list of Config IDs from the Configs' name

        :param configs_resp: response from "get_configs_from_project"
        :param configs: list of Configuration names; e.g. ['Nexus 5', 'Naples']
        :return: a sorted list of Config IDs
        """
        config_ids = []
        for conf in configs:
            conf_id = self.get_config_id_by_name(configs_resp, conf)
            if conf_id is not None:
                config_ids.append(conf_id)
        return sorted(config_ids)

    def get_run_id_in_plan_by_name(self, name, plan_id, configs=None):
        """ Find the id of a specific Test Run in a Test Plan based on its name

        :param name: name of the test run
        :param plan_id: id of the Test Plan in which the Test Run resides
        :param configs: list of Configuration for the Test Run;
                        e.g. response from "generate_config_ids_list_by_name"
        :return: if found, id of the test run; else, None
        """
        if configs is None:
            configs = []
        target = 'Test run'
        resp = self.client.send_get('get_plan/{}'.format(plan_id))
        # return self.search_name_in_response(resp['entries'], name, target)

        for r in resp['entries']:
            if r['name'] == name:  # Found a matching entry, now find matching Config
                logging.info(" Found entry '{}', now find Run with matching Config...".format(name))
                runs = r['runs']
                for run in runs:
                    if run['config_ids'] == configs:
                        logging.info(" Found {} '{}': id={}".format(target.lower(), name, run['id']))
                        return str(run['id'])
        logging.warning(" {} '{}' with Config {} not found.".format(target, name, configs))
        return None

    def post_results_to_test_run(self, run_id, test_result):
        """ Send the POST HTTP request to TestRail

        :param run_id: ID of the Test Run for the result
        :param test_result: a data structure in the following format;
                            use "jenkins_flow.generate_post_data"
            # sample_packet = {
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
        :return: HTTP response from TestRail
        """
        return self.client.send_post('add_results_for_cases/' + run_id, test_result)
