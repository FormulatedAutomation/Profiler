"""
System profiling module for windows
"""

import winreg
from .system_base import SystemBase


class SystemWin(SystemBase):
    """Library for generating a profile report on the current system

    """

    def get_profile(self):
        profile = super().get_profile()
        profile['windows'] = {
            'programs': self.get_programs(),
        }
        return profile

    def get_programs(self):
        return {
            'uninstall_list': self._get_uninstall_list(),
            'office_info': self._get_office_info(),
        }

    def _dump_program_list_from_hive(self, hive, flag):
        """ Dump the registry listed programs"""
        a_reg = winreg.ConnectRegistry(None, hive)
        a_key = winreg.OpenKey(
            a_reg,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            0, winreg.KEY_READ | flag)

        count_subkey = winreg.QueryInfoKey(a_key)[0]

        software_list = []

        for i in range(count_subkey):
            software = {}
            try:
                asubkey_name = winreg.EnumKey(a_key, i)
                asubkey = winreg.OpenKey(a_key, asubkey_name)
                software['name'] = winreg.QueryValueEx(
                    asubkey, "DisplayName")[0]
                software['data_source'] = "Uninstall List"

                try:
                    software['version'] = winreg.QueryValueEx(
                        asubkey, "DisplayVersion")[0]
                except EnvironmentError:
                    software['version'] = 'undefined'
                try:
                    software['publisher'] = winreg.QueryValueEx(
                        asubkey, "Publisher")[0]
                except EnvironmentError:
                    software['publisher'] = 'undefined'
                software_list.append(software)
            except EnvironmentError:
                continue

        return sorted(software_list, key=lambda p: p['name'])

    def _get_office_info(self):
        """ Get information about Office manually """
        a_reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        a_key = winreg.OpenKey(
            a_reg,
            r"SOFTWARE\Microsoft\Office\ClickToRun\Configuration",
            0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        office_details = {
            'name': 'Office 365',
            'data_source': 'Registry Lookup',
        }
        office_details['version'] = winreg.QueryValueEx(
            a_key, "VersionToReport")[0]
        office_details['account'] = winreg.QueryValueEx(
            a_key, "O365HomePremRetail.EmailAddress")[0]
        return office_details

    def _get_uninstall_list(self):
        return(
            self._dump_program_list_from_hive(
                winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY)
            + self._dump_program_list_from_hive(
                winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY)
            + self._dump_program_list_from_hive(
                winreg.HKEY_CURRENT_USER, 0)
        )
