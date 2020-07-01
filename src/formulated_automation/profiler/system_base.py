"""
System profiling base module abstraction
"""
import re
import os
import datetime
import platform
import yaml
from robot.libraries.BuiltIn import BuiltIn
from .utils import Utils

class SystemBase:
    """ Our base class for all system profile classes.
    """

    def __init__(self):
        # def __init__(self, config_file=False):
        self.config = {
            'secret_key_regex': re.compile('.?secret*', re.IGNORECASE),
        }
        # TODO: @mdp parse a config file here if it's passed in

    def get_programs(self):
        # Override this in system specific profile classes
        return {}

    def system_info(self):
        return {
            'login': os.getlogin(),
            'system': platform.system(),
            'platform': platform.platform(),
            'processor': platform.processor(),
        }

    def system_environment_variables(self):
        return Utils.dump_collection(os.environ)

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
            'variables': variables,
            'system': self.system_info(),
            'environment_variables': self.system_environment_variables(),
            'programs': self.get_programs(),
        }
        # TODO: @mdp allow for sending as JSON to a remote endpoint
        self._write_orderly_yaml(profile, output_file)

    def _write_orderly_yaml(self, profile, outfile):
        """ Yaml autosorts keys alphabetically, but we don't want this at the
        top level, we want to be able to put the most important information
        first.
        """
        with open(outfile, 'w+') as f:
            yaml.dump({'metadata': profile['metadata']},
                      f, default_flow_style=False)
            yaml.dump({'system': profile['system']},
                      f, default_flow_style=False)
            yaml.dump({'variables': profile['variables']},
                      f, default_flow_style=False)
            yaml.dump(
                {'environment_variables': profile['environment_variables']},
                f, default_flow_style=False)
            yaml.dump({'programs': profile['programs']},
                      f, default_flow_style=False)
