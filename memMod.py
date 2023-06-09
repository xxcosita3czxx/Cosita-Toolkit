import ctypes
import win32gui
import psutil
PROCESS_ALL_ACCESS = 0x1F0FFF
PROCESS_VM_READ = 0x0010
SIZEOF_INT = ctypes.sizeof(ctypes.c_int)
def search_pid_bn(target_string):
    for proc in psutil.process_iter(['pid', 'name', 'create_time']):
        try:
            hwnds = []
            def callback(hwnd, hwnds):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if target_string in title:
                        hwnds.append(hwnd)
            win32gui.EnumWindows(callback, hwnds)
            if hwnds:
                try:
                    pid = proc.pid
                    parent_pid = proc.ppid()
                    parent_name = psutil.Process(parent_pid).name()
                    exe_name = psutil.Process(proc.pid).exe()
                    return pid
                except psutil.AccessDenied:
                    pass
                except psutil.NoSuchProcess:
                    pass
        except:
            pass
    else:
        print(f"No process found with window title containing {target_string}")
        return None
def modify(pid, address, new_value):
    new_value = ctypes.c_int(new_value)
    process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    buffer = ctypes.create_string_buffer(SIZEOF_INT)
    bytes_read = ctypes.c_size_t(0)
    ctypes.windll.kernel32.ReadProcessMemory(process_handle, address, buffer, SIZEOF_INT, ctypes.byref(bytes_read))
    value = ctypes.c_int.from_buffer(buffer)
    ctypes.windll.kernel32.WriteProcessMemory(process_handle, address, ctypes.byref(new_value), SIZEOF_INT, None)
    ctypes.windll.kernel32.CloseHandle(process_handle)
    return "OK"
def check(pid, address):
    process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_VM_READ, False, pid)
    buffer = ctypes.create_string_buffer(SIZEOF_INT)
    bytes_read = ctypes.c_size_t(0)
    ctypes.windll.kernel32.ReadProcessMemory(process_handle, address, buffer, SIZEOF_INT, ctypes.byref(bytes_read))
    value = ctypes.c_int.from_buffer(buffer).value
    ctypes.windll.kernel32.CloseHandle(process_handle)
    return value