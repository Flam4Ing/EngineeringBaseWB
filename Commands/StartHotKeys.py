import subprocess
import Web
import EB_Auxiliaries

ip = Web.startServer()
with open(EB_Auxiliaries.IpSettingsPath(), 'w') as f:
    f.write(str(ip[0]) + "#" + str(ip[1]))
    f.close()

arg1 = str(ip[0])
arg2 = str(ip[1])
subprocess.Popen([EB_Auxiliaries.autoItExePath(), EB_Auxiliaries.scriptHotKeysPath(), arg1, arg2])