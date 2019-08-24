import subprocess
import Web
import WBAuxiliaries

ip = Web.startServer()
with open(WBAuxiliaries.IpSettingsPath(), 'w') as f:
    f.write(str(ip[0]) + "#" + str(ip[1]))
    f.close()

arg1 = str(ip[0])
arg2 = str(ip[1])
subprocess.Popen([WBAuxiliaries.autoItExePath(), WBAuxiliaries.scriptHotKeysPath(), arg1, arg2])