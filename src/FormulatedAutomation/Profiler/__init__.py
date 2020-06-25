import platform

if platform.system() == 'Windows':
    from .SystemWin import SystemWin as System
else:
    from .SystemPosix import SystemPosix as System
