""" Platform selector for System
"""

import platform
from .DebugKeywords import Debug

system = platform.system().lower()
if system == 'windows':
    from .system_win import SystemWin as System
elif system == 'darwin':
    from .system_darwin import SystemDarwin as System
else:
    from .system_linux import SystemLinux as System
