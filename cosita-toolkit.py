import ctypes
import win32gui
import psutil
import requests
import json
from time import gmtime, strftime
# variables needed for code to work
PROCESS_ALL_ACCESS = 0x1F0FFF
PROCESS_VM_READ = 0x0010
SIZEOF_INT = ctypes.sizeof(ctypes.c_int)
# end of variables

# MAIN
def main():
    print ("yet not supported")
# windows memory editor
class memMod:
    @staticmethod
    def pid_by_name(target_string,exe_name):
        for proc in psutil.process_iter(['pid', 'name', 'create_time']):
            try:
                hwnds = []
                # Enumerate all windows and add the handle to the list if the target string is in the title
                def callback(hwnd, hwnds):
                    if win32gui.IsWindowVisible(hwnd):
                        title = win32gui.GetWindowText(hwnd)
                        if target_string in title:
                            hwnds.append(hwnd)
                win32gui.EnumWindows(callback, hwnds)
                # If we found a matching window, check the parent process
                if hwnds:
                    try:
                        pid = proc.pid
                        parent_pid = proc.ppid()
                        parent_name = psutil.Process(parent_pid).name()
                        exe_name = psutil.Process(proc.pid).exe()
                        if proc.name() == exe_name:
                            #print(f"Found process with window title containing {target_string} and PID {pid} and name: {exe_name}")
                            return pid
                    except psutil.AccessDenied:
                # Access denied - ignore this process
                        pass
                    except psutil.NoSuchProcess:
                # Process may have terminated while iterating
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
class github_api:
    @staticmethod
    def get_last_info_raw(name,save_place=None,file_name=None):
        url = f"https://api.github.com/users/{name}/events/public"
        page = requests.get(url)
        if file_name is None:
            file_name = strftime(f"{name}%Y-%m-%d-%H-%M-%S-last-info-raw.json", gmtime())
        if save_place is not None and not save_place.endswith("/"):
            save_place = save_place + "/"
        if save_place is None:
            save_place = ""
        final = str(save_place+file_name)
        with open(final, "w") as f:
            json.dump(json.loads(page.text), f, indent=4)
        return "OK"
    def get_info_usr(name):
        url = f"https://api.github.com/users/{name}/events/public"
        page = requests.get(url)
        text = page.text
github_api.get_last_info_raw("xxcosita3czxx")