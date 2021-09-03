try:
    import selfpy
except:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "sreq.txt"])