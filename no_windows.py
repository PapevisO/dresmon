def is_windows_host():
    try:
        with open('/proc/version', 'r') as f:
            if 'microsoft' in f.read().lower():
                return True
    except FileNotFoundError:
        pass
    return False

def check_hosts_file_for_crlf():
    with open('/etc/hosts', 'r') as f:
        content = f.read()
        if '\r' in content:
            return True
    return False

def terminate_if_windows_assumed():
    if is_windows_host():
        raise SystemExit("The application does not support Windows host systems.")
    if check_hosts_file_for_crlf():
        raise SystemExit("Detected CRLF in /etc/hosts. Microsoft host "
                            "systems are not supported. If you know what "
                            "you're doing and want to continue, please "
                            "remove carriage return characters from the "
                            "hosts file and restart the app.")
