test_status_by_id = {
    '1': 'Passed',
    '2': 'Blocked',
    '3': 'Untested',
    '4': 'Retest',
    '5': 'Failed',
    '6': 'N/A',
}

test_status_by_name = {
    'Passed': '1',
    'Blocked': '2',
    'Untested': '3',
    'Retest': '4',
    'Failed': '5',
    'N/A': '6',
}

# status = client.send_get('get_statuses')
"""  # begin of statuses
[{'color_bright': 12709313,
  'color_dark': 6667107,
  'color_medium': 9820525,
  'id': 1,
  'is_final': True,
  'is_system': True,
  'is_untested': False,
  'label': 'Passed',
  'name': 'passed'},
 {'color_bright': 16578570,
  'color_dark': 12565506,
  'color_medium': 14933760,
  'id': 2,
  'is_final': True,
  'is_system': True,
  'is_untested': False,
  'label': 'Blocked',
  'name': 'blocked'},
 {'color_bright': 15790320,
  'color_dark': 11579568,
  'color_medium': 15395562,
  'id': 3,
  'is_final': False,
  'is_system': True,
  'is_untested': True,
  'label': 'Untested',
  'name': 'untested'},
 {'color_bright': 11845370,
  'color_dark': 2047228,
  'color_medium': 5335031,
  'id': 4,
  'is_final': False,
  'is_system': True,
  'is_untested': False,
  'label': 'Retest',
  'name': 'retest'},
 {'color_bright': 16552594,
  'color_dark': 16386570,
  'color_medium': 16533845,
  'id': 5,
  'is_final': True,
  'is_system': True,
  'is_untested': False,
  'label': 'Failed',
  'name': 'failed'},
 {'color_bright': 13684944,
  'color_dark': 0,
  'color_medium': 10526880,
  'id': 6,
  'is_final': True,
  'is_system': False,
  'is_untested': False,
  'label': 'N/A',
  'name': 'custom_status1'}]
"""  # end of statuses

test_case_id = {
    'MobileApps.tests.android.aio.bat.test_suite_01_android_aio_bat_scan_tile.Test_Suite_01_Android_AiO_BAT_Scan_Tile': {
        # 'test_01_scan_multiple_pages': '86174',
        # 'test_02_scan_pdf_share_gmail': '86175',
        # 'test_03_scan_pdf_print_trapdoor_ui': '86176'
    },
    'MobileApps.tests.android.aio.bat.test_suite_02_android_aio_bat_scan_to_email_tile.Test_Suite_02_Android_AiO_BAT_Scan_To_Email_Tile': {

    },
    'MobileApps.tests.android.aio.bat.test_suite_03_android_aio_bat_scan_to_cloud_tile.Test_Suite_03_Android_AiO_BAT_Scan_To_Cloud_Tile': {

    },
    'MobileApps.tests.android.aio.bat.test_suite_04_android_aio_bat_print_photos_tile.Test_Suite_04_Android_AIO_BAT_Print_Photos_Tile': {

    },
    'MobileApps.tests.android.aio.bat.test_suite_05_android_aio_bat_print_documents_tile.Test_Suite_05_Android_AIO_BAT_Print_Documents_Tile': {
        'test_01_print_documents_pdf_share_gmail': ['86205', '86206', '86207'],
        'test_02_print_documents_jpg_share_gmail': '86208',
        'test_03_print_documents_jpg_print_trapdoor_ui': '86209'
    },
    'MobileApps.tests.android.aio.bat.test_suite_06_android_aio_bat_camera_scan.Test_Suite_06_Android_Bat_Camera_Scan': {

    },
    'MobileApps.tests.android.aio.bat.test_suite_08_android_aio_bat_printer_info.Test_Suite_08_Android_AiO_Bat_Printer_Info': {

    },
    'MobileApps.tests.android.aio.bat.test_suite_09_android_aio_bat_moobe.Test_Suite_09_Android_AiO_MOOBE': {

    },
    'link': 'https://jiracso.testrail.net/index.php?/cases/view/<test case id>'
}
