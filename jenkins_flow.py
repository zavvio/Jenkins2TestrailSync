import ast
import constant
import logging
import urllib.request
from urllib.error import HTTPError


class JenkinsFlow(object):
    """ General flows for Jenkins

    """
    GOOD_STATUS = ("PASSED", "FIXED")

    # Fixed address fields
    JENKINS_IP_ADDR = 'http://15.98.72.76:8080/job/'
    # BUILD_ADDR = ''
    LATEST_BUILD = 'lastCompletedBuild'
    RESULTS_ADDR = '/testReport'
    API_ADDR = '/api/python?pretty=true'

    # Customizable address field
    JOB_NAME = 'Android_AIO_Marshmallow_BAT' + '/'
    FIXED_BUILD = '632'

    def __init__(self, jenkins_ip_addr=None, job_name=None, fixed_build=None):
        """ Initialize APIClient

        :param jenkins_ip_addr: e.g. "http://15.98.72.76:8080"
        :param job_name: name of a Jenkins job, e.g. "Android_AIO_Marshmallow_BAT"
        """
        if jenkins_ip_addr is not None:
            self.JENKINS_IP_ADDR = jenkins_ip_addr + '/job/'
        if job_name is not None:
            self.JOB_NAME = job_name + '/'

        # Composed URLs
        if fixed_build is not None:
            self.FIXED_BUILD = fixed_build
            self.LATEST_RESULTS_LINK = self.JENKINS_IP_ADDR + self.JOB_NAME + self.FIXED_BUILD + self.RESULTS_ADDR + self.API_ADDR
        else:
            self.LATEST_RESULTS_LINK = self.JENKINS_IP_ADDR + self.JOB_NAME + self.LATEST_BUILD + self.RESULTS_ADDR + self.API_ADDR

        # self.LATEST_BAT_BUILD = JENKINS_IP_ADDR + JOB_NAME + LATEST_BAT_RESULTS + BUILD_ADDR + API_ADDR

        self.result = None
        self.get_result()

    def get_result(self):
        """ Retrieve the latest test result from the Jenkins job

        :return: python dict for the test result
        """
        try:
            resp = urllib.request.urlopen(self.LATEST_RESULTS_LINK).read().decode("utf-8")
        except HTTPError:
            logging.warning("Test build failed, not parsing test results.")
        else:
            self.result = ast.literal_eval(resp)
            # pprint(result)
            return self.result

    def get_apk_version_number(self):
        """ Retrieve version number of the app under test

        :return: Version number of the target app
        """
        # TODO: Parsing build version, e.g. v4.6.99999
        pass

    def generate_post_data(self):
        """ Generate the data packet ready to be POST to TestRail

        :return:
        """
        packet = {
            'results': []
        }
        # print(len(result['suites'][0]['cases']))
        for case in self.result['suites'][0]['cases']:
            data = {}
            # data['className'] = case['className']
            # class_name = case['className'].split('.')
            if case['name'][:4] == "test":
                # Fetching the corresponding test case id on TestRail
                try:
                    suite = constant.test_case_id[case['className']]
                    try:
                        case_id = suite[case['name']]
                        data['case_id'] = case_id
                    except KeyError:
                        logging.warning('Test case not exist in the map: {} - {}'.format(case['name'], case['className']))
                        continue
                except KeyError:
                    logging.warning('Test suite not exist in the map: {}'.format(case['className']))
                    continue

                # Parsing test status, e.g. Pass/Fail
                # data['status_id'] = "PASS" if case['status'] in self.GOOD_STATUS else "FAIL"
                if case['status'] in self.GOOD_STATUS:
                    data['status_id'] = constant.test_status_by_name['Passed']
                else:
                    data['status_id'] = constant.test_status_by_name['Failed']

                packet['results'].append(data)

                # TODO: Parsing build version, e.g. v4.6.99999

                # print(str(class_name[-3:]) + " --- " + case['name'] + ": " + case['status'] + " => " + data['status_id'])
        print(packet)
        return packet


# JF = JenkinsFlow()
# JF.generate_post_data()
