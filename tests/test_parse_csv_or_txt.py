import datetime
import unittest
from pathlib import Path
from netCDF4 import Dataset
from cftime import num2date
from pydantic.v1.utils import deep_update
from modules.telegram import ParsivelTelegram
from modules.netCDF import NetCDF
import tempfile
import os
import shutil
from unittest.mock import patch, Mock, mock_open
from modules.util_functions import yaml2dict, create_logger
from datetime import datetime, timezone
from parse_disdro_csv_or_txt import parsival_telegram_to_dict, thies_telegram_to_dict, \
    choose_sensor, process_row, process_txt_file, main, csv_loop, txt_loop # pylint: disable=import-error

output_file_dir = Path('sample_data/')


def side_effect_parsival(*args, **kwargs):
    '''
    Side effect for the parsivel telegram object, called in the testing txt_loop
    '''
    telegram_objs = []
    for _ in range(2):
        kwargs['telegram_data'] = {'01: 0000.246', '02: 0100.87', '03: 61', '04: 61', '05:   -RA', '06:   R-', '07: 16.854'}
        parsivel_telegram = ParsivelTelegram(*args, **kwargs)
        telegram_objs.append(parsivel_telegram)
    return telegram_objs

def side_effect(*args, **kwargs):
    '''
    Side effect for the NetCDF object, called in the testing txt_loop and in csv_loop'''
    instance = NetCDF(*args, **kwargs)
    instance.logger = Mock()
    return instance

class ExportCSV_TXT(unittest.TestCase):
    """
    Test class for the ExportCSV class
    """
    def setUp(self):
        self.thies_config_dict = yaml2dict("configs_netcdf/config_general_thies.yml")
        self.parsivel_config_dict = yaml2dict("configs_netcdf/config_general_parsivel.yml")

        # Create a temporary directory for the test
        self.test_dir = tempfile.mkdtemp()
        
        # Create a sample input CSV file
        self.input_csv_path = os.path.join(self.test_dir, 'sample_PAR.csv')
        with open(self.input_csv_path, 'w') as f:
            f.write("Timestamp (UTC);Value1;Value2;Value3\n")
            f.write("2023-04-03T06:48:00.223978;1609459200.0;1;2;3\n")
            f.write("2023-04-03T06:49:00.207302;1609459201.0;4;5;6\n")

        # Create a sample configuration YAML file
        self.config_yaml_path = os.path.join(self.test_dir, 'config_sample.yml')
        self.netcdf_config_path = os.path.join(self.test_dir, 'config_general_parsivel.yml')
        with open(self.netcdf_config_path, 'w') as f:
            f.write("telegram_fields:\n")
            f.write("  1: {dtype: 'i4'}\n")
            f.write("  2: {dtype: 'i4'}\n")
            f.write("  3: {dtype: 'i4'}\n")

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_parsivel_telegram_to_dict(self):
        '''
        Test the parsivel_telegram_to_dict function
        '''
        telegram = '0000.246;0100.87;61;61;  -RA;  R-;16.854;17943;00060;21567;00083;006;450541;2.11.4;2.11.1;2.31;17.9;0; ;00:00:00;06.11.2023;PAR007;007;010.087;000;020;010;009;00.246;0000.2;0100.87;16.85;0001.79;0000.00;00000086;-9.999;-9.999;01.218;02.614;02.609;02.086;01.615;01.580;01.585;01.528;00.792;00.387;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;00.000;00.000;01.500;01.652;01.794;02.427;03.080;03.320;03.966;03.759;04.099;05.199;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001001003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002007000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004003004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001002003001000000000000000000000000000000000000000000000000000000000000000000000000000000000000001001003003002000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000002002002000000000000000000000000000000000000000000000000000000000000000000000000000000000000001001001002001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003001001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        dt = datetime(2023, 11, 6, 0, 1, 51)
        ts = 1699225311.829183
        telegram_dict = parsival_telegram_to_dict(telegram=telegram.split(";"), dt=dt, ts=ts, config_telegram_fields=self.parsivel_config_dict['telegram_fields'])
        assert telegram_dict['01'] == 0.246
        assert telegram_dict['02'] == 100.87
        assert telegram_dict['03'] == 61
        assert telegram_dict['04'] == 61
        assert telegram_dict['05'] ==  '  -RA'
        assert telegram_dict['06'] == '  R-'
        assert telegram_dict['07'] == 16.854


    def test_choose_sensor(self):
        '''
        Test the choose_sensor function
        '''
        self.assertEqual(choose_sensor("PAR008"), "PAR")
        self.assertEqual(choose_sensor("THIES001"), "THIES")
        self.assertIsNone(choose_sensor("OTHER"))

    def test_thies_telegram_to_dict(self):
        '''
        Test the thies_telegram_to_dict function
        '''
        telegram = '0205;0459;2.11;27.02.14;10:03:00;00;00;NP   ;000.000;00;00;NP   ;000.000;000.000;000.000;0147.32;99999;-9.9;069;0.0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;+10;15;1713;4011;2886;213;148;152;+06.3;999;9999;9999;9999;00139;00000.000;00003;00000.000;00000;00000.000;00000;00000.000;00027;00000.124;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00109;00000.524;00000;00000.000;000;001;010;014;013;035;028;014;005;003;000;001;001;000;000;000;000;000;000;000;000;000;000;003;001;002;001;003;001;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;99999;99999;9999;999;72;\r\n'

        dt = datetime(2021, 1, 1, 0, 0, 0)
        ts = datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        result = thies_telegram_to_dict(telegram.split(";"), dt=dt, ts=ts, config_telegram_fields=self.thies_config_dict['telegram_fields'])
        expected_keys = [str(i) for i in range(2, 81)] + ['521', '522', '523', '524', '525']+["datetime", "timestamp"]
        self.assertTrue(all(key in result.keys() for key in expected_keys))
        self.assertEqual(result['3'], 459)
        self.assertEqual(result['4'], 2.11)
        self.assertEqual(len(result["81"]), 439)

    
    def test_process_row(self):
        '''
        Test if the process row method returns the correct dictionary for Parsivel and Thies,
        for all formats found in CSV files
        '''
        mock_logger = Mock()
        mock_logger.error = Mock()

        telegram_PAR_value_in_string = ["20210101-000000", "1609459200.0", "b'0000.246;0100.87;61;61;  -RA;  R-;16.854;17943;00060;21567;00083;006;450541;2.11.4;2.11.1;2.31;17.9;0; ;00:00:00;06.11.2023;PAR007;007;010.087;000;020;010;009;00.246;0000.2;0100.87;16.85;0001.79;0000.00;00000086;-9.999;-9.999;01.218;02.614;02.609;02.086;01.615;01.580;01.585;01.528;00.792;00.387;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;00.000;00.000;01.500;01.652;01.794;02.427;03.080;03.320;03.966;03.759;04.099;05.199;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001001003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002007000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004003004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001002003001000000000000000000000000000000000000000000000000000000000000000000000000000000000000001001003003002000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000002002002000000000000000000000000000000000000000000000000000000000000000000000000000000000000001001001002001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003001001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'"]
        telegram_THIES_value_in_string = ["20210101-000000", "1609459200.0", "b'\x0205;0459;2.11;27.02.14;10:03:00;00;00;NP   ;000.000;00;00;NP   ;000.000;000.000;000.000;0147.32;99999;-9.9;069;0.0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;+10;15;1713;4011;2886;213;148;152;+06.3;999;9999;9999;9999;00139;00000.000;00003;00000.000;00000;00000.000;00000;00000.000;00027;00000.124;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00109;00000.524;00000;00000.000;000;001;010;014;013;035;028;014;005;003;000;001;001;000;000;000;000;000;000;000;000;000;000;003;001;002;001;003;001;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;99999;99999;9999;999;72;\r\n'"]
        
        telegram_PAR_value_in_columns = ["2021-01-01T00:00:00.000000", "0000.246", "0100.87", "61", "61", "  -RA", "  R-", "16.854", "17943", "00060", "21567", "00083", "006", "450541", "2.11.4", "2.11.1", "2.31", "17.9", "0", " ", "00:00:00", "06.11.2023", "PAR007", "007", "010.087", "000", "020", "010", "009", "00.246", "0000.2", "0100.87", "16.85", "0001.79", "0000.00", "00000086", "-9.999", "-9.999", "01.218", "02.614", "02.609", "02.086", "01.615", "01.580", "01.585", "01.528", "00.792", "00.387", "-9.999", "-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999", "00.000", "00.000", "01.500", "01.652","01.794","02.427","03.080","03.320","03.966","03.759","04.099","05.199","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000", "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001001003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002007000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004003004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001002003001000000000000000000000000000000000000000000000000000000000000000000000000000000000000001001003003002000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000002002002000000000000000000000000000000000000000000000000000000000000000000000000000000000000001001001002001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003001001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000" ]
        telegram_Thies_value_in_columns = ["20210101-000000", "0459", "2.11", "27.02.14", "10:03:00", "00", "00", "NP   ", "000.000", "00", "00", "NP   ", "000.000", "000.000", "000.000", "0147.32", "99999", "-9.9", "069", "0.0", "0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","+10","15","1713","4011","2886","213","148","152","+06.3","999","9999","9999","9999","00139","00000.000","00003","00000.000","00000","00000.000","00000","00000.000","00027","00000.124","00000","00000.000","00000","00000.000","00000","00000.000","00000","00000.000","00000","00000.000","00000","00000.000","00000","00000.000","00000","00000.000","00109","00000.524","00000","00000.000","000","001","010","014","013","035","028","014","005","003","000","001","001","000","000","000","000","000","000","000","000","000","000","003","001","002","001","003","001","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","99999","99999","9999","999","72","\r\n'"]
        result_PAR_string, timestamp_PAR_string = process_row(telegram_PAR_value_in_string, "PAR", self.parsivel_config_dict['telegram_fields'], mock_logger)
        result_THIES_string, timestamp_THIES_string = process_row(telegram_THIES_value_in_string, "THIES", self.thies_config_dict['telegram_fields'], mock_logger)

        result_PAR_columns, timestamp_PAR_columns = process_row(telegram_PAR_value_in_columns, "PAR", self.parsivel_config_dict['telegram_fields'], mock_logger)
        result_THIES_columns, timestamp_THIES_columns = process_row(telegram_Thies_value_in_columns, "THIES", self.thies_config_dict['telegram_fields'], mock_logger)

        self.assertIsInstance(result_PAR_string, dict)
        self.assertIsInstance(result_THIES_string, dict)
        self.assertIsInstance(result_PAR_columns, dict)
        self.assertIsInstance(result_THIES_columns, dict)
        
        self.assertEqual(timestamp_PAR_string, datetime.strptime("20210101-000000", "%Y%m%d-%H%M%S"))
        self.assertEqual(timestamp_THIES_string, datetime.strptime("20210101-000000", "%Y%m%d-%H%M%S"))

    def test_process_txt_file(self):
        '''
        Test if the process txt file method returns the correct dictionary for Parsivel,
        for all formats found in TXT files
        '''
        expected_timestamp = datetime.strptime("2020-01-01 00:00:50", "%Y-%m-%d %H:%M:%S")
        
        expected_telegram_dict = {'01': 4.0, '06': 'haha', '91': [9, 9, 9], 'timestamp': '2020-01-01 00:00:50', 
                                  'datetime': datetime.fromtimestamp(expected_timestamp.timestamp(), tz=timezone.utc)}

        txt_list = ['01:4', '02:55', '20:00:00:50', '21:01.01.2020','06:haha', '91:9;9;9;']
        telegram_dict, timestamp = process_txt_file(txt_list, self.parsivel_config_dict['telegram_fields'])
        print(telegram_dict, timestamp)

        self.assertEqual(telegram_dict, expected_telegram_dict)
        self.assertEqual(timestamp, expected_timestamp)
        
    
    def test_sensor_not_found_bytestring_format(self):
        '''
        Test if the process row method calls the logger with an error if the sensor is not found,
        when a csv row is of length 3, this happens if all values of a telegram
        are in a bytestring
        '''
        csv_list = ['20220101-120000', '1641052800', "b'telegram;more_telegram'"]
        sensor = 'UNKNOWN'
        config_telegram_fields = {}
        mock_logger = Mock()
        process_row(csv_list, sensor, config_telegram_fields, mock_logger)
        mock_logger.error.assert_called_once_with(msg=f"Sensor {sensor} not found")

    def test_sensor_not_found_seperate_column_format(self):
        '''
        Test if the process row method calls the logger with an error if the sensor is not found,
        when a csv row is of a larger length than 3, this happens if all values of a telegram
        are in seperate columns
        '''
        csv_list = ['20220101-120000', '1641052800', 'telegram', 'more_telegram']
        sensor = 'UNKNOWN'
        config_telegram_fields = {}
        mock_logger = Mock()
        process_row(csv_list, sensor, config_telegram_fields, mock_logger)
        mock_logger.error.assert_called_once_with(msg=f"Sensor {sensor} not found")


    def test_csv_format_not_recognized(self):
        '''
        Test if the process row method calls the logger with an error if the CSV format is not recognized
        '''
        csv_list = ['20220101-120000', '1641052800']
        sensor = 'PAR'
        config_telegram_fields = {}
        mock_logger = Mock()
        process_row(csv_list, sensor, config_telegram_fields, mock_logger)
        mock_logger.error.assert_called_once_with(msg="CSV format not recognized")

    @patch('parse_disdro_csv_or_txt.NetCDF')
    @patch('parse_disdro_csv_or_txt.csv_loop')
    def test_main_csv(self, mock_csv_loop, mock_NetCDF):
        '''
        Test if the main function creates a NetCDF file for a CSV file
        '''

        output_file_path =  output_file_dir / '20230116_PAR008_Green_Village.nc'

        if os.path.exists(output_file_path):
            os.remove(output_file_path)

        mock_args = Mock()
        mock_args.config = 'configs_netcdf/config_008_GV.yml'	
        mock_args.input = 'sample_data/20230116.csv'
        mock_args.file_type = 'csv'

        telegram_objs = side_effect_parsival
        date = datetime(2023, 1, 16, 0, 0, 0)
        mock_NetCDF.side_effect = side_effect

        main(mock_args)

        assert output_file_path.exists()

        if os.path.exists(output_file_path):
            os.remove(output_file_path)
    
    @patch('parse_disdro_csv_or_txt.NetCDF')
    @patch('parse_disdro_csv_or_txt.txt_loop')
    def test_main_txt(self, mock_txt_loop, mock_NetCDF):
        '''
        Test if the main function creates a NetCDF file for a TXT file
        '''
        output_file_path =  output_file_dir / '20210129_PAR001_KNMI_Cabauw.nc'

        if os.path.exists(output_file_path):
            os.remove(output_file_path)

        mock_args = Mock()
        mock_args.config = 'configs_netcdf/config_001_CABAUW.yml'	
        mock_args.input = 'sample_data/20210129'
        mock_args.file_type = 'txt'

        telegram_objs = side_effect_parsival
        date = datetime(2021, 1, 29, 0, 0, 0)
        mock_NetCDF.side_effect = side_effect

        main(mock_args)

        assert output_file_path.exists()

        if os.path.exists(output_file_path):
            os.remove(output_file_path)

    @patch('csv.reader')
    @patch('parse_disdro_csv_or_txt.process_row')
    @patch('parse_disdro_csv_or_txt.telegrams')
    def test_csv_loop(self, mock_telegrams, mock_process_row, mock_csv_reader): 
        ''' 
        Test if the csv loop method returns a list of dictionaries
        '''
        # Arrange
        mock_csv_reader.return_value = [
            ['Timestamp (UTC)', 'Other data'],
            ['2022-01-01 00:00:00', 'Some data'],
            ['2022-01-02 00:00:00', 'Some other data'],
        ]
        mock_process_row.return_value = ('mocked telegram', 'mocked timestamp')
        mock_telegrams.__getitem__.return_value = Mock()

        mock_logger = Mock()
        input_path = Path('sample_data/20210129.csv')
        # Act
        with patch('builtins.open', mock_open(read_data='data')) as mock_file:
            result = csv_loop(input_path, 'THIES', 'config_dict', 'conf_telegram_fields', mock_logger)

        # Assert
        self.assertEqual(len(result), 2)
        mock_process_row.assert_called()
        mock_telegrams.__getitem__.assert_called_with('THIES')
        
    @patch('os.listdir')
    @patch('parse_disdro_csv_or_txt.process_txt_file')
    @patch('parse_disdro_csv_or_txt.telegrams')
    def test_txt_loop(self, mock_telegrams, mock_process_txt_file, mock_listdir):
        '''
        Test if the txt loop method returns a list of dictionaries
        '''
        # Arrange
        mock_listdir.return_value = ['file1.csv', 'file2.txt', 'file3.txt']
        mock_process_txt_file.return_value = ('mocked telegram', 'mocked timestamp')
        mock_telegrams.__getitem__.return_value = Mock()

        mock_logger = Mock()
        input_path = Path('sample_data/20210129')
        # Act
        with patch('builtins.open', mock_open(read_data='data')) as mock_file:
            result = txt_loop(input_path, 'PAR', 'config_dict', 'conf_telegram_fields', mock_logger)

        # Assert
        self.assertEqual(len(result), 2)
        mock_process_txt_file.assert_called()
        mock_telegrams.__getitem__.assert_called_with('PAR')

    @patch('parse_disdro_csv_or_txt.Path')
    @patch('parse_disdro_csv_or_txt.yaml2dict')
    @patch('parse_disdro_csv_or_txt.create_logger')
    @patch('parse_disdro_csv_or_txt.choose_sensor')
    def test_main_sensor_not_found(self, mock_choose_sensor, mock_create_logger, mock_yaml2dict, mock_path):
        '''
        Test if the main function exits with status 1 if the sensor is not found'''
        # Mock arguments
        mock_args = Mock()
        mock_args.input = 'input_file'
        mock_args.config = 'config_file'

        # Mock Path
        mock_path.return_value.stem.split.return_value = ['20220101']

        # Mock yaml2dict
        mock_yaml2dict.return_value = {
            'global_attrs': {'sensor_name': 'UNKNOWN', 'site_name': 'site'},
            'log_dir': 'log_dir'
        }

        # Mock create_logger
        mock_logger = Mock()
        mock_create_logger.return_value = mock_logger

        # Mock choose_sensor
        mock_choose_sensor.return_value = None

        with self.assertRaises(SystemExit) as cm:
            main(mock_args)

    @patch('parse_disdro_csv_or_txt.Path')
    @patch('parse_disdro_csv_or_txt.yaml2dict')
    @patch('parse_disdro_csv_or_txt.create_logger')
    def test_main_invalid_file_type(self, mock_create_logger, mock_yaml2dict, mock_path):
        '''
        Test if the main function calls the logger with an error and if it
        exits with status 1 if the file type is not recognized
        '''
        # Mock arguments
        mock_args = Mock()
        mock_args.input = 'input_file'
        mock_args.config = 'config_file'
        mock_args.file_type = 'invalid'  # This will trigger the else condition

        # Mock Path
        mock_path.return_value.stem.split.return_value = ['20220101']

        # Mock yaml2dict
        mock_yaml2dict.return_value = {
            'global_attrs': {'sensor_name': 'PAR008', 'site_name': 'site'},
            'log_dir': 'log_dir',
            'telegram_fields': 'telegram_fields'
        }

        # Mock create_logger
        mock_logger = Mock()
        mock_create_logger.return_value = mock_logger


        with self.assertRaises(SystemExit) as cm:
            main(mock_args)

        # Check that logger.error was called with the expected message
        mock_logger.error.assert_called_once_with(msg="File type invalid not recognized")

        # Check that the script exited with status 1
        self.assertEqual(cm.exception.code, 1)

