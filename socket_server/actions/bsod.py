import ctypes


def trigger_bsod():
    ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
    ctypes.windll.ntdll.NtRaiseHardError(
        0xC000021A, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint())
    )
