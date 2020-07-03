"""
System profiling base module abstraction
"""
import re
import os
import sys
import datetime
import platform
import yaml
import pkg_resources
from robot.libraries.BuiltIn import BuiltIn
from .utils import Utils

DEFAULT_PROFILE_KEY_ORDER = [
    'metadata',
    'system',
    'robot_framework',
    'python',
]

class SystemBase:
    """ Our base class for all system profile classes.
    """

    def __init__(self):
        # def __init__(self, config_file=False):
        self.config = {
            'secret_key_regex': re.compile('.*secret.*', re.IGNORECASE),
        }
        # TODO: @mdp parse a config file here if it's passed in

    def get_programs(self):
        # Override this in system specific profile classes
        return {}

    def system_info(self):
        """ Get System Info for profiling
        """
        info = {
            'system': platform.system(),
            'platform': platform.platform(),
            'processor': platform.processor(),
            'environment_variables': self.system_environment_variables(),
        }
        try:
            # Will fail in restricted shells
            info['system'] = os.getlogin()
        except OSError:
            pass

        return info

    def system_environment_variables(self):
        return Utils.dump_collection(os.environ)

    def python(self):
        """ List out all python information
        """
        return {
            'version': sys.version,
            'executable': sys.executable,
            'exec_prefix': sys.exec_prefix,
            'packages': self.python_packages(),
        }
        installed_packages = pkg_resources.working_set
        installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
                                          for i in installed_packages])
        return installed_packages_list

    def python_packages(self):
        """ List out all the installed python packages and versions
        """
        installed_packages = pkg_resources.working_set
        installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
                                          for i in installed_packages])
        return installed_packages_list

    def write_profile(self):
        """ Write out the system profile in the output directory """
        output_dir = BuiltIn().get_variable_value('${OUTPUT_DIR}')
        output_file = os.path.join(output_dir, "fa_report.yaml")
        variables = Utils.dump_collection(
            BuiltIn().get_variables(),
            secret_key_regex=self.config['secret_key_regex'])
        profile = {
            'metadata': {
                'run_at': datetime.datetime.utcnow(),
                'profiler': self.__class__.__name__,
            },
            'robot_framework': {
                'variables': variables,
            },
            'system': self.system_info(),
            'python': self.python(),
            'programs': self.get_programs(),
        }
        # TODO: @mdp allow for sending as JSON to a remote endpoint
        self.__write_orderly_yaml(profile, output_file)

    def __profile_key_order(self):
        return DEFAULT_PROFILE_KEY_ORDER

    def __sorted_profile(self, profile):
        """ Returns a multi-dimensional array of values
        eg. [[key, dict], [key, dict]]
        for the purpose of dumping to an specifically ordered yaml file
        """

        key_order = self.__profile_key_order()
        profile_arr = []

        for key in key_order:
            val = profile.pop(key, {})
            profile_arr.append([key, val])

        for key, val in profile.items():
            profile_arr.append([key, val])

        return profile_arr

    def __write_orderly_yaml(self, profile, outfile):
        """ Yaml autosorts keys alphabetically, but we don't want this at the
        top level, we want to be able to put the most important information
        first.
        """
        profile_arr = self.__sorted_profile(profile)
        with open(outfile, 'w+') as f:
            for item in profile_arr:
                yaml.dump({item[0]: item[1]},
                          f, default_flow_style=False)
