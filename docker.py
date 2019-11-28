import os

docker_ps_a = os.popen('docker ps -a')

std_lines= docker_ps_a.readlines()

for line in std_lines:
    print(line)
