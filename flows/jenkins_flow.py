import ast
import logging
import pprint
import urllib.request
from resource import constant
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
    CONSOLE_OUTPUT_ADDR = '/consoleText'

    # Customizable address field
    FIXED_BUILD = '632'

    def __init__(self, job_name, jenkins_ip_addr=None, fixed_build=None):
        """ Initialize APIClient

        :param jenkins_ip_addr: e.g. "http://15.98.72.76:8080"
        :param job_name: name of a Jenkins job, e.g. "Android_AIO_Marshmallow_BAT"
        """
        logging.basicConfig(level=logging.INFO)
        if jenkins_ip_addr is not None:
            self.JENKINS_IP_ADDR = jenkins_ip_addr + '/job/'
        self.JOB_NAME = job_name + '/'

        # Composed URLs
        if fixed_build is not None:
            self.FIXED_BUILD = fixed_build
            self.RESULTS_LINK = self.JENKINS_IP_ADDR + self.JOB_NAME + self.FIXED_BUILD + self.RESULTS_ADDR + self.API_ADDR
            self.CONSOLE_LINK = self.JENKINS_IP_ADDR + self.JOB_NAME + self.FIXED_BUILD + self.CONSOLE_OUTPUT_ADDR
        else:
            self.RESULTS_LINK = self.JENKINS_IP_ADDR + self.JOB_NAME + self.LATEST_BUILD + self.RESULTS_ADDR + self.API_ADDR
            self.CONSOLE_LINK = self.JENKINS_IP_ADDR + self.JOB_NAME + self.LATEST_BUILD + self.CONSOLE_OUTPUT_ADDR

        # self.LATEST_BAT_BUILD = JENKINS_IP_ADDR + JOB_NAME + LATEST_BAT_RESULTS + BUILD_ADDR + API_ADDR

        self.result = None
        self.get_result()

    def get_result(self):
        """ Retrieve the latest test result from the Jenkins job

        :return: python dict for the test result
        """
        try:
            resp = urllib.request.urlopen(self.RESULTS_LINK).read().decode("utf-8")
        except HTTPError:
            logging.warning(" Test build failed, not parsing test results.")
        else:
            self.result = ast.literal_eval(resp)
            # pprint(result)
            return self.result

    def get_apk_name(self):
        """ Retrieve name of the app apk under test, which contains the version number
        e.g. PrinterControl-googlestore-debug-develop_daily_2017-10-12_08-56-09_4.6.40.apk
        :return: Name of the target app apk
        """
        try:
            resp = urllib.request.urlopen(self.CONSOLE_LINK).read().decode("utf-8")
        except HTTPError:
            logging.warning(" Test build failed, not parsing test results.")
        else:
            for substring in resp.split('\n'):
                if '.apk' in substring and 'http' in substring:
                    app_version = substring.strip().split('/')[-1]
                    logging.info('>> App Version: {}'.format(app_version))
                    return app_version

    def get_device_info(self):
        """ Parse console log to retrieve info of the device under test
        device = DEVICE-device-name
        platform = DEVICE-platform-name
        version = DEVICE-platform-version
        :return: tuple (device, platform, version)
        """
        try:
            resp = urllib.request.urlopen(self.CONSOLE_LINK).read().decode("utf-8")
        except HTTPError:
            logging.warning(" Test build failed, not parsing for device info.")
        else:
            device, platform, version = None, None, None
            strings = resp.split('\n')
            for substring in strings:
                if 'DEVICE-device-name' in substring:
                    device = substring.strip().split('=')[-1]
                    logging.info('>> Device: {}'.format(device))
                    break
                    # return device_name
            for substring in strings:
                if 'DEVICE-platform-name' in substring:
                    platform = substring.strip().split('=')[-1]
                    logging.info('>> Platform: {}'.format(platform))
                    break
                    # return platform
            for substring in strings:
                if 'DEVICE-platform-version' in substring:
                    version = substring.strip().split('=')[-1]
                    logging.info('>> Platform version: {}'.format(version))
                    break
                    # return version
            return device, platform, version

    def generate_post_data(self, test_case_id):
        """ Generate the data packet ready to be POST to TestRail
        Data packet is in the following format:
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
        :param test_case_id: a data structure storing the Test Case IDs
        :return: A POST-format of the parsed Jenkins result if it's available.
        """
        if self.result is None:
            logging.warning(" Self.result is empty meaning test result wasn't parsed right from Jenkins.")
            return None
        apk_version = self.get_apk_name()
        device, platform, version = self.get_device_info()
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
                    suite = test_case_id[case['className']]
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

                # Parsing apk name or build version, e.g. v4.6.99999
                data['version'] = apk_version
                data['comment'] = "Device={}\nPlatform={}\nPlatform version={}".format(device, platform, version)

                if type(data['case_id']) is str:
                    packet['results'].append(data)
                elif type(data['case_id']) is list:
                    temp_list = data['case_id']
                    for item in temp_list:
                        dd = data.copy()
                        dd['case_id'] = item
                        packet['results'].append(dd)

                # print(str(class_name[-3:]) + " --- " + case['name'] + ": " + case['status'] + " => " + data['status_id'])
        logging.info(' POST-ready data >>\n' + pprint.pformat(packet))
        return packet


# # Sample test_case_id
# sample_test_case_id = {
#     'MobileApps.tests.android.aio.bat.test_suite_01_android_aio_bat_scan_tile.Test_Suite_01_Android_AiO_BAT_Scan_Tile': {
#         'test_01_scan_multiple_pages': '214866',
#         'test_02_scan_pdf_share_gmail': '214867',
#         'test_03_scan_pdf_print_trapdoor_ui': '214868',
#         'test_05_scan_pdf_save': '214869',
#         'test_06_scan_jpg_save': '214870',
#         'test_07_verify_existed_saved_files': '214871'
#     }
# }
# JOB_NAME = 'Android_AIO_Marshmallow_BAT/'
# JF = JenkinsFlow(job_name=JOB_NAME)
# JF.generate_post_data(sample_test_case_id)
# JF.get_apk_name()
# d, p, v = JF.get_device_info()
