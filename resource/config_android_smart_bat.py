TESTRAIL_LINK = 'https://jiracso.testrail.net'
USERNAME = ''  # username = @hp.com email address
PASSWORD = ''  # API Key - generate this via TestRail settings
PROJECT = 'MAQA'
MILESTONE = 'Android - HP Smart v4.6'
TEST_PLAN = 'Android - HP Smart (Automated BAT)'
TEST_RUN = 'Android - HP Smart (Automated BAT) [EN]'
CONFIGS = ['Nexus 6P', 'Naples']

JENKINS_JOB = 'Android_AIO_Marshmallow_BAT'

test_case_id = {
    'MobileApps.tests.android.aio.bat.test_suite_01_android_aio_bat_scan_tile.Test_Suite_01_Android_AiO_BAT_Scan_Tile': {
        'test_01_scan_multiple_pages': '214866',
        'test_02_scan_pdf_share_gmail': '214867',
        'test_03_scan_pdf_print_trapdoor_ui': '214868',
        'test_05_scan_pdf_save': '214869',
        'test_06_scan_jpg_save': '214870',
        'test_07_verify_existed_saved_files': '214871'
    },
    'MobileApps.tests.android.aio.bat.test_suite_02_android_aio_bat_scan_to_email_tile.Test_Suite_02_Android_AiO_BAT_Scan_To_Email_Tile': {

    },
    'MobileApps.tests.android.aio.bat.test_suite_03_android_aio_bat_scan_to_cloud_tile.Test_Suite_03_Android_AiO_BAT_Scan_To_Cloud_Tile': {

    },
    'MobileApps.tests.android.aio.bat.test_suite_04_android_aio_bat_print_photos_tile.Test_Suite_04_Android_AIO_BAT_Print_Photos_Tile': {

    },
    'MobileApps.tests.android.aio.bat.test_suite_05_android_aio_bat_print_documents_tile.Test_Suite_05_Android_AIO_BAT_Print_Documents_Tile': {

    },
    'MobileApps.tests.android.aio.bat.test_suite_06_android_aio_bat_camera_scan.Test_Suite_06_Android_Bat_Camera_Scan': {

    },
    'MobileApps.tests.android.aio.bat.test_suite_08_android_aio_bat_printer_info.Test_Suite_08_Android_AiO_Bat_Printer_Info': {

    },
    'MobileApps.tests.android.aio.bat.test_suite_09_android_aio_bat_moobe.Test_Suite_09_Android_AiO_MOOBE': {

    },
    'link': 'https://jiracso.testrail.net/index.php?/cases/view/<test case id>'
}
