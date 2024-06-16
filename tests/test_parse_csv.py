import datetime
import unittest
from pathlib import Path
from netCDF4 import Dataset
from cftime import num2date
from pydantic.v1.utils import deep_update
from modules.telegram import ParsivelTelegram
import modules.netCDF as netCDF
import tempfile
import os
import shutil
from unittest.mock import patch, Mock
from modules.util_functions import yaml2dict, create_logger
from datetime import datetime, timezone
from parse_disdro_csv import parsival_telegram_to_dict, thies_telegram_to_dict, \
    choose_sensor, process_row, process_txt_file, main, csv_loop, txt_loop # pylint: disable=import-error

output_file_dir = Path('sample_data/')

def side_effect(*args, **kwargs):
    """
    Side effect to replace 'data_dir' in mocked netCDF objects.
    :return: netCDF instance with substituted 'data_dir'
    """
    kwargs['data_dir'] = output_file_dir
    instance = netCDF(*args, **kwargs)
    instance.logger = Mock()
    return instance

class ExportCSV(unittest.TestCase):
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
        # with open('C:\Users\melsl\Documents\CSE\Y2\Software_Project\python-logging-software\config_007_CABAUW.yml', 'r') as template_file:
        #     template_content = template_file.read()
        
        # with open(self.config_yaml_path, 'w') as f:
        #     f.write(template_content.replace('log_dir: /path/to/log', f'log_dir: {self.test_dir}'))

        # Create a sample configuration for netCDF (used by the script)
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
        self.assertEqual(choose_sensor("sample_PAR.csv"), "PAR")
        self.assertEqual(choose_sensor("sample_THIES.csv"), "THIES")
        self.assertIsNone(choose_sensor("sample_OTHER.csv"))

    def test_thies_telegram_to_dict(self):
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
        telegram_PAR_value_in_string = ["20210101-000000", "1609459200.0", "b'0000.246;0100.87;61;61;  -RA;  R-;16.854;17943;00060;21567;00083;006;450541;2.11.4;2.11.1;2.31;17.9;0; ;00:00:00;06.11.2023;PAR007;007;010.087;000;020;010;009;00.246;0000.2;0100.87;16.85;0001.79;0000.00;00000086;-9.999;-9.999;01.218;02.614;02.609;02.086;01.615;01.580;01.585;01.528;00.792;00.387;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;-9.999;00.000;00.000;01.500;01.652;01.794;02.427;03.080;03.320;03.966;03.759;04.099;05.199;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;00.000;000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001001003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002007000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004003004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001002003001000000000000000000000000000000000000000000000000000000000000000000000000000000000000001001003003002000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000002002002000000000000000000000000000000000000000000000000000000000000000000000000000000000000001001001002001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003001001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'"]
        telegram_THIES_value_in_string = ["20210101-000000", "1609459200.0", "b'\x0205;0459;2.11;27.02.14;10:03:00;00;00;NP   ;000.000;00;00;NP   ;000.000;000.000;000.000;0147.32;99999;-9.9;069;0.0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;+10;15;1713;4011;2886;213;148;152;+06.3;999;9999;9999;9999;00139;00000.000;00003;00000.000;00000;00000.000;00000;00000.000;00027;00000.124;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00000;00000.000;00109;00000.524;00000;00000.000;000;001;010;014;013;035;028;014;005;003;000;001;001;000;000;000;000;000;000;000;000;000;000;003;001;002;001;003;001;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;99999;99999;9999;999;72;\r\n'"]
        
        telegram_PAR_value_in_columns = ["2021-01-01T00:00:00.000000", "0000.246", "0100.87", "61", "61", "  -RA", "  R-", "16.854", "17943", "00060", "21567", "00083", "006", "450541", "2.11.4", "2.11.1", "2.31", "17.9", "0", " ", "00:00:00", "06.11.2023", "PAR007", "007", "010.087", "000", "020", "010", "009", "00.246", "0000.2", "0100.87", "16.85", "0001.79", "0000.00", "00000086", "-9.999", "-9.999", "01.218", "02.614", "02.609", "02.086", "01.615", "01.580", "01.585", "01.528", "00.792", "00.387", "-9.999", "-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999","-9.999", "00.000", "00.000", "01.500", "01.652","01.794","02.427","03.080","03.320","03.966","03.759","04.099","05.199","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000","00.000", "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001001003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002007000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004003004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001002003001000000000000000000000000000000000000000000000000000000000000000000000000000000000000001001003003002000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000002002002000000000000000000000000000000000000000000000000000000000000000000000000000000000000001001001002001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003001001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000" ]
        telegram_Thies_value_in_columns = ["20210101-000000", "0459", "2.11", "27.02.14", "10:03:00", "00", "00", "NP   ", "000.000", "00", "00", "NP   ", "000.000", "000.000", "000.000", "0147.32", "99999", "-9.9", "069", "0.0", "0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","+10","15","1713","4011","2886","213","148","152","+06.3","999","9999","9999","9999","00139","00000.000","00003","00000.000","00000","00000.000","00000","00000.000","00027","00000.124","00000","00000.000","00000","00000.000","00000","00000.000","00000","00000.000","00000","00000.000","00000","00000.000","00000","00000.000","00000","00000.000","00109","00000.524","00000","00000.000","000","001","010","014","013","035","028","014","005","003","000","001","001","000","000","000","000","000","000","000","000","000","000","003","001","002","001","003","001","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","000","99999","99999","9999","999","72","\r\n'"]
        result_PAR_string, timestamp_PAR_string = process_row(telegram_PAR_value_in_string, "PAR", self.parsivel_config_dict['telegram_fields'])
        result_THIES_string, timestamp_THIES_string = process_row(telegram_THIES_value_in_string, "THIES", self.thies_config_dict['telegram_fields'])

        result_PAR_columns, timestamp_PAR_columns = process_row(telegram_PAR_value_in_columns, "PAR", self.parsivel_config_dict['telegram_fields'])
        result_THIES_columns, timestamp_THIES_columns = process_row(telegram_Thies_value_in_columns, "THIES", self.thies_config_dict['telegram_fields'])

        self.assertIsInstance(result_PAR_string, dict)
        self.assertIsInstance(result_THIES_string, dict)
        self.assertIsInstance(result_PAR_columns, dict)
        self.assertIsInstance(result_THIES_columns, dict)
        
        self.assertEqual(timestamp_PAR_string, datetime.strptime("20210101-000000", "%Y%m%d-%H%M%S"))
        self.assertEqual(timestamp_THIES_string, datetime.strptime("20210101-000000", "%Y%m%d-%H%M%S"))

    # def test_process_txt_file(self):
    #     input_txt_path = os.path.join(self.test_dir, 'sample_PAR.txt')
    #     output_csv_path = os.path.join(self.test_dir, 'sample_PAR.csv')
    #     telegram_dict, timestamp = process_txt_file(input_txt_path, output_csv_path, self.parsivel_config_dict['telegram_fields'])

    #     self.assertTrue(os.path.isfile(output_csv_path))

    # @patch('parse_disdro_csv.csv_loop')
    # @patch('parse_disdro_csv.NetCDF')
    # def test_main_loop(self, mock_csv_loop, mock_netcdf):

    #     output_file_path =  '20240101_Green_Village-GV_PAR008.nc'

    #     if os.path.exists(output_file_path):
    #         os.remove(output_file_path)

    #     mock_args = Mock()
    #     mock_logger = Mock()
    #     mock_args.config = self.config_yaml_path
    #     mock_args.input = self.input_csv_path
    #     mock_args.file_type = "csv"

    #     mock_csv_loop.return_value = csv_loop(self.input_csv_path, 'PAR', self.config_yaml_path, self.parsivel_config_dict['telegram_fields'], mock_logger)
    #     mock_netcdf.side = side_effect
        

    #     main(mock_args)

    #     assert output_file_path.exists()

    #     if os.path.exists(output_file_path):
    #         os.remove(output_file_path)
    
    
    # def test_main_integration(self):
    #     # Run the script with the sample input and configuration
    #     result = subprocess.run([
    #         'python3', 'parse_disdro_csv.py',
    #         '-c', self.config_yaml_path,
    #         '-i', self.input_csv_path
    #     ], capture_output=True, text=True)

    #     # Check if the script executed without errors
    #     self.assertEqual(result.returncode, 0, msg=result.stderr)

    #     # Verify the expected output netCDF file
    #     output_nc_path = os.path.join(self.test_dir, 'sample_PAR')
    #     self.assertTrue(os.path.isfile(output_nc_path), "NetCDF file was not created")
