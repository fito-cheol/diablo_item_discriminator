import psutil

# Get the list of running processes
def get_running_processes():
    process_list = []
    for proc in psutil.process_iter():
        try:
            process_info = proc.as_dict(attrs=['pid', 'name'])
            process_list.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return process_list


if __name__ == '__main__':
  # name 'Diablo IV.exe'
  processes = get_running_processes()
  for process in processes:
      print(f"PID: {process['pid']}, Name: {process['name']}")