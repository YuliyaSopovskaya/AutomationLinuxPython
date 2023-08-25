import pytest
# from checkers import checkout, getout
# import random, string
# import yaml
# from datetime import datetime

# with open('config.yaml') as f:
#     # читаем документ YAML
#     data = yaml.safe_load(f)


# @pytest.fixture()
# def make_folders():
#     return checkout("mkdir {} {} {} {}".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"]), "")


# @pytest.fixture()
# def clear_folders():
#     return checkout("rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"]), "")


# @pytest.fixture()
# def make_files():
#     list_off_files = [ ]
#     for i in range(data["count"]):
#         filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
#         if checkout("cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"], filename, data["bs"]), ""):
#             list_off_files.append(filename)
#     return list_off_files


# @pytest.fixture()
# def make_subfolder():
#     testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
#     subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
#     if not checkout("cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
#         return None, None
#     if not checkout("cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"], subfoldername, testfilename), ""):
#         return subfoldername, None
#     else:
#         return subfoldername, testfilename


# @pytest.fixture(autouse=True)
# def print_time():
#     print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
#     yield
#     print("Finish: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


# @pytest.fixture()
# def make_bad_arx():
#     checkout("cd {}; 7z a {}/arxbad -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok")
#     checkout("truncate -s 1 {}/arxbad.{}".format(data["folder_out"], data["type"]), "Everything is Ok")
#     yield "arxbad"
#     checkout("rm -f {}/arxbad.{}".format(data["folder_out"], data["type"]), "")


# @pytest.fixture(autouse=True)
# def stat():
#     yield
#     stat = getout("cat /proc/loadavg")
#     checkout("echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(datetime.now().strftime("%H:%M:%S.%f"), data["count"], data["bs"], stat), "")

#-------------------------------------------------------------

#ssh_host: 
#ssh_username: 
#ssh_password: 


#folder_in: папка входных файлов
#folder_ext: папка внешних файлов
#folder_ext2: 2 папка внешних файлов
#folder_out: папка выходных файлов
#count: 10
#bs: 1024
#type: zip


import pytest
import paramiko
import random
import string
import yaml
from datetime import datetime


with open('config.yaml') as f:
    data = yaml.safe_load(f)


ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(data["ssh_host"], username=data["ssh_username"], password=data["ssh_password"])


def checkout(command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    return stdout.channel.recv_exit_status()


@pytest.fixture()
def make_folders():
    checkout("mkdir {} {} {} {}".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"]))
    yield
    checkout("rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"]))


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        command = "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"], filename, data["bs"])
        if checkout(command):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if checkout("cd {}; mkdir {}".format(data["folder_in"], subfoldername)):
        return None, None
    if checkout("cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"], subfoldername, testfilename)):
        return subfoldername, None
    else:
        return subfoldername, testfilename



@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print("Finish: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture()
def make_bad_arx():
    checkout("cd {}; 7z a {}/arxbad -t{}".format(data["folder_in"], data["folder_out"], data["type"]))
    checkout("truncate -s 1 {}/arxbad.{}".format(data["folder_out"], data["type"]))
    yield "arxbad"
    checkout("rm -f {}/arxbad.{}".format(data["folder_out"], data["type"]))


@pytest.fixture(autouse=True)
def stat():
    yield
    stdin, stdout, stderr = ssh_client.exec_command("cat /proc/loadavg")
    stat = stdout.read().decode().strip()
    checkout("echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(datetime.now().strftime("%H:%M:%S.%f"), data["count"], data["bs"], stat))
