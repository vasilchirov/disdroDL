"""
Module with all test fixtures.
"""

import os
import logging
from pathlib import Path
from logging import StreamHandler
from datetime import datetime, timedelta, timezone
import unittest
from pydantic.v1.utils import deep_update
import pytest

from modules.sqldb import create_db, connect_db
from modules.util_functions import yaml2dict
from modules.now_time import NowTime
from modules.telegram import ParsivelTelegram, ThiesTelegram
from modules.netCDF import NetCDF

# General

now = NowTime()
wd = Path().resolve()
data_dir = wd / 'sample_data'

log_handler = StreamHandler()
logger = logging.getLogger('test-log')
logger.addHandler(log_handler)

start_dt = datetime(year=2024, month=1, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc)
data_points_24h = 1440  # (60min * 24h)

# Parsivel

db_file = 'test_parsivel.db'
db_path_parsivel = data_dir / db_file

config_dict = yaml2dict(path=wd / 'configs_netcdf' / 'config_general_parsivel.yml')
config_dict_site = yaml2dict(path=wd / 'configs_netcdf' / 'config_008_GV.yml')
config_dict_parsivel = deep_update(config_dict, config_dict_site)

parsivel_lines = [b'TYP OP4A\r\n', b'01:0000.000\r\n', b'02:0000.00\r\n', b'03:00\r\n', b'04:00\r\n', b'05:   NP\r\n', b'06:   C\r\n', b'07:-9.999\r\n', b'08:20000\r\n', b'09:00043\r\n', b'10:13894\r\n', b'11:00000\r\n', b'12:021\r\n', b'13:450994\r\n', b'14:2.11.6\r\n', b'15:2.11.1\r\n', b'16:0.50\r\n', b'17:24.3\r\n', b'18:0\r\n', b'19: \r\n', b'20:10:13:21\r\n', b'21:25.05.2023\r\n', b'22:\r\n', b'23:\r\n', b'24:0000.00\r\n', b'25:000\r\n', b'26:032\r\n', b'27:022\r\n', b'28:022\r\n', b'29:000.041\r\n', b'30:00.000\r\n', b'31:0000.0\r\n', b'32:0000.00\r\n', b'34:0000.00\r\n', b'35:0000.00\r\n', b'40:20000\r\n', b'41:20000\r\n', b'50:00000000\r\n', b'51:000140\r\n', b'90:-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;\r\n', b'91:00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;\r\n', b'93:000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;\r\n', b'94:0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;0000;\r\n', b'95:0.00;0.00;0.00;0.00;0.00;0.00;0.00;\r\n', b'96:0000000;0000000;0000000;0000000;0000000;0000000;0000000;\r\n', b'97:;\r\n', b'98:;\r\n', b'99:;\r\n', b'\x03'] # pylint: disable=line-too-long

# Thies

db_file = 'test_thies.db'
db_path_thies = data_dir / db_file

config_dict = yaml2dict(path=wd / 'configs_netcdf' / 'config_general_thies.yml')
config_dict_site = yaml2dict(path=wd / 'configs_netcdf' / 'config_008_GV_THIES.yml')
config_dict_thies = deep_update(config_dict, config_dict_site)

thies_lines = '06;0854;2.11;01.01.14;18:59:00;00;00;NP   ;000.000;00;00;NP   ;000.000;000.000;000.000;0000.00;99999;-9.9;100;0.0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;+23;26;1662;4011;2886;258;062;063;+20.3;999;9999;9999;9999;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;99999;99999;9999;999;E9;'

#TODO: remove redundancy when thies works

@pytest.fixture()
def create_db_():
    """
    This function creates test.db in sample_data if it does not exist yet.
    """
    if os.path.isfile(db_path_parsivel):
        os.remove(db_path_parsivel)
    create_db(dbpath=db_path_parsivel)

@pytest.fixture()
def create_db_thies_():
    """
    This function creates test.db in sample_data if it does not exist yet.
    """
    if os.path.isfile(db_path_thies):
        os.remove(db_path_thies)
    create_db(dbpath=db_path_thies)

@pytest.fixture()
def db_insert_24h(create_db_): # pylint: disable=unused-argument,redefined-outer-name
    """
    This function inserts 24 hours worth of data into the test database.
    :param create_db_: the function to create the test database
    """
    # inserts 1440 rows to db
    con, cur = connect_db(dbpath=str(db_path_parsivel))
    for i in range(data_points_24h):
        new_time = start_dt + timedelta(minutes=i)  # time offset: by 1 minute
        telegram = ParsivelTelegram(config_dict=config_dict_parsivel,
                                    telegram_lines=parsivel_lines,
                                    timestamp=new_time,
                                    db_cursor=cur,
                                    telegram_data={},
                                    logger=logger)
        telegram.capture_prefixes_and_data()
        telegram.prep_telegram_data4db()
        telegram.insert2db()
    con.commit()
    cur.close()
    con.close()

@pytest.fixture()
def db_insert_24h_thies(create_db_thies_): # pylint: disable=unused-argument,redefined-outer-name
    """
    This function inserts 24 hours worth of data into the test database.
    :param create_db_: the function to create the test database
    """
    # inserts 1440 rows to db
    con, cur = connect_db(dbpath=str(db_path_thies))
    for i in range(data_points_24h):
        new_time = start_dt + timedelta(minutes=i)  # time offset: by 1 minute
        telegram = ThiesTelegram(config_dict=config_dict_thies,
                                    telegram_lines=thies_lines,
                                    timestamp=new_time,
                                    db_cursor=cur,
                                    telegram_data={},
                                    logger=logger)
        telegram.insert2db()
    con.commit()
    cur.close()
    con.close()

@pytest.fixture()
def db_insert_24h_w_gaps(create_db_): # pylint: disable=unused-argument,redefined-outer-name
    """
    This function inserts 24 hours worth of data into the test database, but with some missing rows.
    :param create_db_: the function to create the test database
    """
    # inserts 1440 rows to db, but in half of entries, telegram is empty
    con, cur = connect_db(dbpath=str(db_path_parsivel))
    for i in range(data_points_24h):
        new_time = start_dt + timedelta(minutes=i)  # time offset: by 1 minute
        if i % 2 == 0:
            data_lines = parsivel_lines
        else:
            data_lines = []  # odd index: empty list, instead of parsivel_lines
        telegram = ParsivelTelegram(config_dict=config_dict_parsivel,
                                    telegram_lines=data_lines,
                                    timestamp=new_time,
                                    db_cursor=cur,
                                    telegram_data={},
                                    logger=logger)
        telegram.capture_prefixes_and_data()
        telegram.prep_telegram_data4db()
        telegram.insert2db()
    con.commit()
    cur.close()
    con.close()

@pytest.fixture()
def db_insert_24h_empty(create_db_): # pylint: disable=unused-argument,redefined-outer-name
    """
    This function inserts 24 hours worth of data into the test database, but with some missing rows.
    :param create_db_: the function to create the test database
    """
    # inserts 1440 rows to db, but in half of entries, telegram is empty
    con, cur = connect_db(dbpath=str(db_path_parsivel))
    for i in range(data_points_24h):
        new_time = start_dt + timedelta(minutes=i)  # time offset: by 1 minute
        data_lines = []  # everything empty
        telegram = ParsivelTelegram(config_dict=config_dict_parsivel,
                                    telegram_lines=data_lines,
                                    timestamp=new_time,
                                    db_cursor=cur,
                                    telegram_data={},
                                    logger=logger)
        telegram.capture_prefixes_and_data()
        telegram.prep_telegram_data4db()
        telegram.insert2db()
    con.commit()
    cur.close()
    con.close()
