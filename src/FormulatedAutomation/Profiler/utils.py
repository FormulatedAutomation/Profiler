from collections import Mapping

class Utils:

    @staticmethod
    def dump_collection(d):
        out = {}
        for k, v in d.items():
            # TODO: @mdp handle obscuring secrets here
            if isinstance(v, Mapping):
                out[k] = Utils.dump_collection(v)
            else:
                out[k] = v
        return out
