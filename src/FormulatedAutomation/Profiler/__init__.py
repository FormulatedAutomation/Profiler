""" Platform selector for System
"""

import platform

system = platform.system().lower()
if system == 'windows':
    from .SystemWin import SystemWin as System
elif system == 'darwin':
    from .SystemDarwin import SystemDarwin as System
else:
    from .SystemLinux import SystemLinux as System
