""" Keywords for generating a profile of the system we are running on"""

import os
import yaml
import platform
import winreg
from robot.libraries.BuiltIn import BuiltIn
from .utils import Utils

class SystemWin:
    """Library for generating a profile report on the current system

    """

    def write_profile(self):
        output_dir = BuiltIn().get_variable_value('${OUTPUT_DIR}')
        output_file = os.path.join(output_dir, "fa_report.yaml")
        variables = Utils.dump_collection(BuiltIn().get_variables())
        output = {
            'variables': variables,
            'system': self.system_info(),
            'programs': {
                'uninstall_list': self._get_uninstall_list(),
                'office_info': self._get_office_info(),
            }
        }
        with open(output_file, 'w') as f:
            yaml.dump(output, f, default_flow_style=False)

    def system_info(self):
        return {
            'system': platform.system(),
            'platform': platform.platform(),
            'processor': platform.processor(),
        }

    def _dump_program_list_from_hive(self, hive, flag):
        a_reg = winreg.ConnectRegistry(None, hive)
        a_key = winreg.OpenKey(a_reg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                            0, winreg.KEY_READ | flag)

        count_subkey = winreg.QueryInfoKey(a_key)[0]

        software_list = []

        for i in range(count_subkey):
            software = {}
            try:
                asubkey_name = winreg.EnumKey(a_key, i)
                asubkey = winreg.OpenKey(a_key, asubkey_name)
                software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]
                software['data_source'] = "Uninstall List"

                try:
                    software['version'] = winreg.QueryValueEx(asubkey, "DisplayVersion")[0]
                except EnvironmentError:
                    software['version'] = 'undefined'
                try:
                    software['publisher'] = winreg.QueryValueEx(asubkey, "Publisher")[0]
                except EnvironmentError:
                    software['publisher'] = 'undefined'
                software_list.append(software)
            except EnvironmentError:
                continue

        return sorted(software_list, key=lambda p:p['name'])

    def _get_office_info(self):
        a_reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        a_key = winreg.OpenKey(a_reg, r"SOFTWARE\Microsoft\Office\ClickToRun\Configuration",
                0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        office_details = {
            'name': 'Office 365',
            'data_source': 'Registry Lookup',
        }
        office_details['version'] = winreg.QueryValueEx(a_key, "VersionToReport")[0]
        office_details['account'] = winreg.QueryValueEx(a_key, "O365HomePremRetail.EmailAddress")[0]
        return office_details

    def _get_uninstall_list(self):
        return(
            self._dump_program_list_from_hive(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY)
            + self._dump_program_list_from_hive(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY)
            + self._dump_program_list_from_hive(winreg.HKEY_CURRENT_USER, 0)
        )
