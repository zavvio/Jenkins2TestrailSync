import logging
from testrail_3 import *


class TestRailFlow(object):
    """ General flows for TestRail

    """
    def __init__(self, user='', password=''):
        """ Initialize APIClient

        :param user: username, should be your @hp email address
        :param password: API key, generate it via TestRail settings
        """
        logging.basicConfig(level=logging.INFO)
        self.client = APIClient('https://jiracso.testrail.net')
        self.client.user = 'ho-lun-zavvio.mok@hp.com'
        self.client.password = '3HI/BnjdpLGdkHIjdzC2-mnEkT3LbEZQTUPvF.P4x'  # API Key
        if user != '':
            self.client.user = user
        if password != '':
            self.client.password = password

    @staticmethod
    def search_name_in_response(response, name, target):
        for r in response:
            if r['name'] == name:
                logging.info("Found {} [{}]: id={}".format(target, name, r['id']))
                return str(r['id'])
        logging.info("{} [{}] not found.".format(target, name))
        return None

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
        response = self.client.send_get(request)
        return self.search_name_in_response(response, name, target)

    def get_project_id_by_name(self, name='MAQA'):
        """ Find the id of a project based on its name

        :param name: name of the project
        :return: if found, id of the project; else, None
        """
        target = 'Project'
        response = self.client.send_get('get_projects')
        return self.search_name_in_response(response, name, target)

    def get_milestone_id_by_name(self, name='Android - HP Smart v4.6', project_id='20'):
        """ Find the id of a milestone based on its name
        Note: MAQA project id = 20
        :param name: name of the milestone
        :param project_id: project id of which the milestone is in
        :return: if found, id of the milestone; else, None
        """
        target = 'Milestone'
        response = self.client.send_get('get_milestones/{}'.format(project_id))
        return self.search_name_in_response(response, name, target)
