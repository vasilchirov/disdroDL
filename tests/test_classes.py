"""
This module contains tests for the NowTime and Telegram classes.

Functions:
- test_NowTime: Tests that the NowTime class functions in general, and returns the correct time.
- test_timestamp: Tests the correctness of the iso format strings from the NowTime class.
- test_Telegram_row: Tests the correctness of creating a ParsivelTelegram object with contents.
- test_Telegram_empty_row: Tests the correctness of creating a ParsivelTelegram object without contents.
- create_test_data_dir: Creates a directory at the given path if it doesn't exist yet.
- test_telegram_row_thies: Tests the correctness of creating a ThiesTelegram object with contents.
- test_telegram_empty_row_thies: Tests the correctness of creating a ThiesTelegram object without contents.
- test_parse_telegram_row_edge_cases: Tests that a telegram row with key:val,val,...; for some pair can be parsed.
- test_create_telegram_not_recognized: Tests parsing a non recognized sensor type.
"""

import os
import logging
from logging import StreamHandler
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock
from pydantic.v1.utils import deep_update

from modules.now_time import NowTime
from modules.telegram import ParsivelTelegram, ThiesTelegram
from modules.util_functions import yaml2dict
import modules.telegram as telegram


log_handler = StreamHandler()
logger = logging.getLogger('testlog')
logger.addHandler(log_handler)
wd = Path(__file__).parent.parent
test_data_dir = wd / 'test_data'
config_dict = yaml2dict(path=wd / 'configs_netcdf' / 'config_general_parsivel.yml')
config_dict_site = yaml2dict(path=wd / 'configs_netcdf' / 'config_008_GV.yml')
config_dict = deep_update(config_dict, config_dict_site)

config_dict_thies = yaml2dict(path=wd / 'configs_netcdf' / 'config_general_thies.yml')
config_dict_site_thies = yaml2dict(path=wd / 'configs_netcdf' / 'config_008_GV_THIES.yml')
config_dict_thies = deep_update(config_dict_thies, config_dict_site_thies)

parsivel_lines = [b'TYP OP4A\r\n', b'01:0000.000\r\n', b'02:0000.00\r\n', b'03:00\r\n', b'04:00\r\n', b'05:   NP\r\n', b'06:   C\r\n', b'07:-9.999\r\n', b'08:20000\r\n', b'09:00043\r\n', b'10:13894\r\n', b'11:00000\r\n', b'12:021\r\n', b'13:450994\r\n', b'14:2.11.6\r\n', b'15:2.11.1\r\n', b'16:0.50\r\n', b'17:24.3\r\n', b'18:0\r\n', b'19: \r\n', b'20:10:13:21\r\n', b'21:25.05.2023\r\n', b'22:\r\n', b'23:\r\n', b'24:0000.00\r\n', b'25:000\r\n', b'26:032\r\n', b'27:022\r\n', b'28:022\r\n', b'29:000.041\r\n', b'30:00.000\r\n', b'31:0000.0\r\n', b'32:0000.00\r\n', b'34:0000.00\r\n', b'35:0000.00\r\n', b'40:20000\r\n', b'41:20000\r\n', b'50:00000000\r\n', b'51:000140\r\n', b'90:-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;\r\n', b'91:00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;\r\n', b'93:000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;\r\n', b'94:0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;\r\n', b'95:0.00;0.00;0.00;0.00;0.00;0.00;0.00;\r\n', b'96:0000000;0000000;0000000;0000000;0000000;0000000;0000000;\r\n', b'97:;\r\n', b'98:;\r\n', b'99:;\r\n', b'\x03'] # pylint: disable=line-too-long
parsivel_db_line_edge_case = '01:0000.000; 02:0000.00; 03:1;2; 90:0,0; 91:0,0; 93:0,0'

def test_NowTime():
    """
    This function tests that the NowTime class functions in general, and returns the correct time.
    """
    now = NowTime()
    test_time_list = datetime.utcnow().strftime("%H:%M:%S").split(":")
    assert isinstance(now.time_list, list) is True
    assert now.time_list[0] == test_time_list[0]
    assert now.time_list[1] == test_time_list[1]
    assert now.time_list[2] == test_time_list[2]
    # assert: the following attributes are only created after method: __date_strings()
    assert isinstance(now.iso, str) is True
    assert isinstance(now.ym, str) is True
    assert isinstance(now.ymd, str) is True


def test_timestamp():
    """
    This functions tests the correctness of the iso format strings from the NowTime class.
    """
    now = NowTime()
    print('now.utc', now.utc)
    print('now.utc (iso)', now.utc.isoformat())
    ts = now.utc.timestamp()
    ts_no_tz = datetime.fromtimestamp(ts)
    ts_tz = datetime.fromtimestamp(ts, tz=timezone.utc)
    assert ts_tz.isoformat() == now.utc.isoformat()
    assert ts_no_tz.isoformat() != now.utc.isoformat()  # no tz aware date will differ from tzaware
    # print('now.utc.timestamp', ts)
    # print('ts_no_tz', ts_no_tz)
    # print('utcfromtimestamp', datetime.utcfromtimestamp(ts))
    # print('ts_tz', ts_tz)

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

def create_test_data_dir(directory):
    """
    This functions creates a directory at the given path if it doesn't exist yet.
    """
    if not os.path.exists(path=directory):
        os.mkdir(path=directory)

def test_parse_telegram_row_edge_cases():
    """
    Tests that a telegram row with key:val,val,... for some pair can be passed
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


def test_create_telegram_not_recognized(caplog):
    """
    Tests that if a configuration dictionary for a not recognized disdrometer sensor is
    parsed the logger sends a message and the function returns None.
    """
    config_dict = MagicMock()
    values = { 'global_attrs': {'sensor_type':'wrong_telegram'} }
    config_dict.__getitem__.side_effect = values.__getitem__
    assert config_dict['global_attrs']['sensor_type'] == 'wrong_telegram'
    created_telegram = telegram.create_telegram(config_dict=config_dict,
                                                telegram_lines=None,
                                                db_row_id=None,
                                                timestamp=None,
                                                db_cursor=None,
                                                telegram_data={},
                                                logger=logger)
    assert [r.msg for r in caplog.records][0] == 'Sensor type wrong_telegram not recognized'
    assert created_telegram == None