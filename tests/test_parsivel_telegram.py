"""
This module contains tests for the ParsivelTelegram class methods.

Functions:
- test_capture_prefixes_and_data_parsivel: Tests the correctness of capturing telegram data.
- test_capture_prefixes_and_data_empty_parsivel: Tests the correctness of capturing telegram when telegram is empty.
- test_capture_prefixes_and_data_partial_telegram_parsivel: Tests the correctness of capturing telegram data when
  only a partial Parsivel telegram is given.
- test_capture_prefixes_and_data_one_missing_value_parsivel: Tests the correctness of capturing telegram data when
  a Parsivel telegram with a missing value is given.
- test_parse_telegram_row_parsivel: Tests the correctness of creating a ParsivelTelegram object with contents.
- test_parse_empty_telegram_row_parsivel: Tests the correctness of creating a ParsivelTelegram object without contents.
- test_parse_telegram_row_missing_value_thies: Tests the correctness of creating a ParsivelTelegram object with one value
  missing.
- test_parse_telegram_row_edge_cases_parsivel: Tests 2 edge cases. Parsing a telegram row with a key that has assigned
  multiple values (key:val;val;) and parsing a telegram with a key that is not in the configuration
  dictionary of the sensor.
- test_str2list_parsivel: Tests str2list method for ParsivelTelegram class.
"""

import logging
from logging import StreamHandler
from datetime import datetime, timezone
from pathlib import Path
from pydantic.v1.utils import deep_update

from conftest import now
from modules.telegram import ParsivelTelegram
from modules.util_functions import yaml2dict


log_handler = StreamHandler()
logger = logging.getLogger('testlog')
logger.addHandler(log_handler)
wd = Path(__file__).parent.parent
test_data_dir = wd / 'test_data'
config_dict = yaml2dict(path=wd / 'configs_netcdf' / 'config_general_parsivel.yml')
config_dict_site = yaml2dict(path=wd / 'configs_netcdf' / 'config_008_GV.yml')
config_dict = deep_update(config_dict, config_dict_site)

parsivel_lines = [b'TYP OP4A\r\n', b'01:0000.000\r\n', b'02:0000.00\r\n', b'03:00\r\n', b'04:00\r\n', b'05:   NP\r\n', b'06:   C\r\n', b'07:-9.999\r\n', b'08:20000\r\n', b'09:00043\r\n', b'10:13894\r\n', b'11:00000\r\n', b'12:021\r\n', b'13:450994\r\n', b'14:2.11.6\r\n', b'15:2.11.1\r\n', b'16:0.50\r\n', b'17:24.3\r\n', b'18:0\r\n', b'19: \r\n', b'20:10:13:21\r\n', b'21:25.05.2023\r\n', b'22:\r\n', b'23:\r\n', b'24:0000.00\r\n', b'25:000\r\n', b'26:032\r\n', b'27:022\r\n', b'28:022\r\n', b'29:000.041\r\n', b'30:00.000\r\n', b'31:0000.0\r\n', b'32:0000.00\r\n', b'34:0000.00\r\n', b'35:0000.00\r\n', b'40:20000\r\n', b'41:20000\r\n', b'50:00000000\r\n', b'51:000140\r\n', b'90:-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;\r\n', b'91:00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;\r\n', b'93:000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;\r\n', b'94:0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;\r\n', b'95:0.00;0.00;0.00;0.00;0.00;0.00;0.00;\r\n', b'96:0000000;0000000;0000000;0000000;0000000;0000000;0000000;\r\n', b'97:;\r\n', b'98:;\r\n', b'99:;\r\n', b'\x03'] # pylint: disable=line-too-long
parsivel_db_line_edge_case = '01:0000.000; 02:0000.00; 03:1;2; 90:0,0; 91:0,0; 93:0,0; 800:1; '
keys = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '34', '35', '40', '41', '50', '51', '90', '91', '93', '94', '95', '96']
key_90_values = ['-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999', '-9.999']
key_91_values = ['00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000', '00.000']
parsivel_lines_partial = [b'TYP OP4A\r\n', b'01:0000.000\r\n', b'02:0000.00\r\n', b'03:00\r\n']
parsivel_lines_missing_value = [b'TYP OP4A\r\n', b'01:0000.000\r\n', b'02:0000.00\r\n', b'03:00\r\n',b'04:00\r\n', b'05:   NP\r\n', b'06:   C\r\n', b'07:-9.999\r\n', b'08:20000\r\n', b'09:00043\r\n', b'10:13894\r\n', b'11:00000\r\n', b'12:021\r\n', b'13:450994\r\n', b'14:2.11.6\r\n', b'15:2.11.1\r\n', b'16:0.50\r\n', b'17:24.3\r\n', b'18:0\r\n', b'19: \r\n', b'20:10:13:21\r\n', b'21:25.05.2023\r\n', b'22:\r\n', b'23:\r\n', b'24:0000.00\r\n', b'25:000\r\n', b'26:032\r\n', b'27:022\r\n', b'28:022\r\n', b'29:000.041\r\n', b'30:00.000\r\n', b'31:0000.0\r\n', b'32:0000.00\r\n', b'34:0000.00\r\n', b'35:0000.00\r\n', b'40:20000\r\n', b'41:20000\r\n', b'50:00000000\r\n', b'51:000140\r\n', b'90:-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;\r\n', b'91:00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;\r\n', b'93:000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;\r\n', b'94:0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;\r\n', b'95:0.00;0.00;0.00;0.00;0.00;0.00;0.00;\r\n', b'96:0000000;0000000;0000000;0000000;0000000;0000000;0000000;\r\n', b'97:;\r\n', b'98:;\r\n', b'99:;\r\n', b'\x03'] # pylint: disable=line-too-long



def test_capture_prefixes_and_data_parsivel():
    """
    This function tests that the capture_prefixes_and_data method correctly fills
    the telegram data dictionary.
    """
    telegram = ParsivelTelegram(config_dict=None,
                             telegram_lines=parsivel_lines,
                             timestamp=None,
                             db_cursor=None,
                             telegram_data={},
                             logger=None)
    telegram.capture_prefixes_and_data()

    data_dictionary = telegram.telegram_data
    #check that all the keys are in the dictionary
    assert list(data_dictionary.keys()) == keys
    #check that values from telegram are populated to dictionary
    assert data_dictionary['08'] == '20000'
    assert data_dictionary['14'] == '2.11.6'
    #check that keys with data arrays/matrices work
    assert data_dictionary['90'] == key_90_values
    assert data_dictionary['91'] == key_91_values
    assert data_dictionary['93'] == ['000' for _ in range(1024)]

def test_capture_prefixes_and_data_empty_parsivel():
    """
    This function tests that the capture_prefixes_and_data method correctly fills
    the telegram data dictionary when an empty telegram is given.
    """
    telegram = ParsivelTelegram(config_dict=None,
                                telegram_lines='',
                                timestamp=None,
                                db_cursor=None,
                                telegram_data={},
                                logger=None)
    telegram.capture_prefixes_and_data()

    data_dictionary = telegram.telegram_data
    #check that telegram data is empty
    assert len(data_dictionary.keys()) == 0

def test_capture_prefixes_and_data_partial_telegram_parsivel():
    """
    This function tests that the capture_prefixes_and_data method correctly fills
    the telegram data dictionary when a partial telegram is given.
    """
    telegram = ParsivelTelegram(config_dict=None,
                                telegram_lines=parsivel_lines_partial,
                                timestamp=None,
                                db_cursor=None,
                                telegram_data={},
                                logger=None)
    telegram.capture_prefixes_and_data()

    data_dictionary = telegram.telegram_data
    #check that telegram data is filled
    assert list(data_dictionary.keys()) == ['01', '02', '03']
    assert list(data_dictionary.values()) == ['0000.000', '0000.00', '00']

def test_capture_prefixes_and_data_one_missing_value_parsivel():
    """
    This function tests that the capture_prefixes_and_data method correctly fills
    the telegram data dictionary when a telegram with one missing value (val;;val;) is given.
    """
    telegram = ParsivelTelegram(
        config_dict=config_dict,
        telegram_lines=parsivel_lines,
        timestamp=now.utc,
        db_cursor=None,
        telegram_data={},
        logger=None)
    telegram.capture_prefixes_and_data()
    assert telegram.telegram_data['03'] == '00'
    telegram.telegram_data['03'] = ''
    telegram.prep_telegram_data4db()
    telegram_str_list = telegram.telegram_data_str.split('; ')
    assert telegram_str_list[2] == '03:None'

# Python docs: fromtimestamp(timestamp, tz=None)¶ on timezones
# Return local date and time corresponding to POSIX timestamp, such as is returned by time.time().
# If optional argument tz is None or not specified then
# the timestamp is converted to the platform’s local date and time,
# and the returned datetime object is naive.

def test_telegram_row_parsivel():
    """
    This function tests the correctness of creating a ParsivelTelegram object with contents.
    """
    row = {'id': 65, 'timestamp': 1702893300.577833, 'datetime': '2023-12-18T09:55:00.577833', 'parsivel_id': 'PAR008', 'telegram': 'VERSION:2.11.6; BUILD:2112151; 01:0000.000; 02:0000.00; 03:00; 04:00; 05:NP; 06:C; 07:-9.999; 08:20000; 09:00060; 10:11424; 11:00000; 12:008; 13:450994; 14:2.11.6; 15:2.11.1; 16:2.00; 17:24.2; 18:0; 19:None; 20:09; 21:18.12.2023; 22:GV; 23:None; 24:0000.00; 25:000; 26:021; 27:010; 28:010; 29:000.013; 30:00.000; 31:0000.0; 32:0000.00; 34:0000.00; 35:0000.00; 40:20000; 41:20000; 50:00000000; 51:000139; 90:-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999; 91:00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000; 93:000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000; 94:0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000; 95:0.00,0.00,0.00,0.00,0.00,0.00,0.00; 96:0000000,0000000,0000000,0000000,0000000,0000000,0000000'} # pylint: disable=line-too-long
    row_ts_dt = datetime.fromtimestamp(row.get('timestamp'), tz=timezone.utc)
    row_telegram = ParsivelTelegram(
        config_dict=config_dict,
        telegram_lines=row.get('telegram'),
        timestamp=row_ts_dt,
        db_cursor=None,
        telegram_data={},
        logger=logger)
    row_telegram.parse_telegram_row()
    # time
    assert row_ts_dt == row_telegram.timestamp
    assert row.get('timestamp') == row_telegram.timestamp.timestamp()
    # matrix fields (2D, 3D)
    assert len(row_telegram.telegram_data['90']) == 32
    for i in row_telegram.telegram_data['90']:
        assert len(i) >= 4 and len(i) < 7 and ',' not in i
    assert len(row_telegram.telegram_data['91']) == 32
    for i in row_telegram.telegram_data['91']:
        # print('f91:', i)
        assert len(i) == 6 and ',' not in i
    assert len(row_telegram.telegram_data['93']) == 1024
    for i in row_telegram.telegram_data['93']:
        # print('f93:', i)
        assert len(i) == 3
        for letter in i:
            assert int(letter) in list(range(10))
    for key in row_telegram.telegram_data.keys():
        assert key in config_dict['telegram_fields']


def test_telegram_empty_row_parsivel():
    """
    This function tests the correctness of creating a ParsivelTelegram object without contents.
    """
    row = {'id': 65, 'timestamp': 1702893300.577833, 'datetime': '2023-12-18T09:55:00.577833',
           'parsivel_id': 'PAR008','telegram': ''}
    row_ts_dt = datetime.fromtimestamp(row.get('timestamp'), tz=timezone.utc)
    row_telegram = ParsivelTelegram(
        config_dict=config_dict,
        telegram_lines=row.get('telegram'),
        timestamp=row_ts_dt,
        db_cursor=None,
        telegram_data={},
        logger=logger)
    row_telegram.parse_telegram_row()
    assert row_telegram.telegram_data == {}

def test_parse_telegram_row_missing_value_parsivel():
    """
    This function tests the correctness of creating a ThiesTelegram object with contents, but
    with one value missing.
    """
    row = {'id': 65, 'timestamp': 1702893300.577833, 'datetime': '2023-12-18T09:55:00.577833', 'parsivel_id': 'PAR008',
           'telegram': 'VERSION:2.11.6; BUILD:2112151; 01:0000.000; 02:0000.00;; 04:00; 05:NP; 06:C; 07:-9.999; 08:20000; 09:00060; 10:11424; 11:00000; 12:008; 13:450994; 14:2.11.6; 15:2.11.1; 16:2.00; 17:24.2; 18:0; 19:None; 20:09; 21:18.12.2023; 22:GV; 23:None; 24:0000.00; 25:000; 26:021; 27:010; 28:010; 29:000.013; 30:00.000; 31:0000.0; 32:0000.00; 34:0000.00; 35:0000.00; 40:20000; 41:20000; 50:00000000; 51:000139; 90:-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999,-9.999; 91:00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000,00.000; 93:000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000; 94:0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000; 95:0.00,0.00,0.00,0.00,0.00,0.00,0.00; 96:0000000,0000000,0000000,0000000,0000000,0000000,0000000'}  # pylint: disable=line-too-long
    row_ts_dt = datetime.fromtimestamp(row.get('timestamp'), tz=timezone.utc)
    telegram = ParsivelTelegram(
        config_dict=config_dict,
        telegram_lines=row.get('telegram'),
        timestamp=row_ts_dt,
        db_cursor=None,
        telegram_data={},
        logger=logger)
    telegram.parse_telegram_row()
    assert len(telegram.telegram_data) == 35
    assert '03' not in telegram.telegram_data.keys()

def test_parse_telegram_row_edge_cases_parsivel():
    """
    This function tests 2 edge cases. Parsing a telegram row with a key that has assigned
    multiple values (key:val;val;) and parsing a telegram with a key that is not in the configuration
    dictionary of the sensor.
    """
    telegram = ParsivelTelegram(
        config_dict=config_dict,
        telegram_lines=parsivel_db_line_edge_case,
        timestamp=None,
        db_cursor=None,
        telegram_data={},
        logger=None)
    telegram.parse_telegram_row()
    assert telegram.telegram_data['03'] == ['1','2']
    assert '800' not in telegram.telegram_data.keys()

def test_str2list_parsivel():
    """
    Tests that str2list method works with Parsivel telegrams
    """
    telegram_data =  {'1': '1,2,3,4,5'}
    telegram = ParsivelTelegram(
        config_dict=None,
        telegram_lines=None,
        timestamp=None,
        db_cursor=None,
        telegram_data=telegram_data,
        logger=None)
    telegram.str2list('1',',')
    assert telegram_data['1'] == ['1','2','3','4','5']