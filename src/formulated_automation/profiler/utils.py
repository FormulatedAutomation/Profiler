"""
Utils Modules for shared tasks
"""
from collections.abc import Mapping

class Utils:
    """ Simple Utils class for various shared tasks
    """

    @staticmethod
    def dump_collection(d, secret_key_regex=False):
        """ Dump out contents of a dict type and redact secrets
        """
        out = {}
        for k, v in d.items():
            # TODO: @mdp handle obscuring secrets here
            if isinstance(v, Mapping):
                out[k] = Utils.dump_collection(
                    v, secret_key_regex=secret_key_regex)
            elif secret_key_regex and secret_key_regex.match(k):
                out[k] = "***SECRET REDACTED***"
            else:
                out[k] = v
        return out
