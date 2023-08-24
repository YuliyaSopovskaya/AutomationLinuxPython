# import pytest
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


# Задание:
# Дополнить проект фикстурой, которая после каждого шага теста дописывает 
# в заранее созданный файл stat.txt строку вида: время, 
# количество файлов из конфига, размер файла из конфига, 
# статистика загрузки процессора из файла /proc/loadavg 
# (можно писать просто всё содержимое этого файла)



# config.py
import yaml


def load_config():
    with open('config.yaml') as f:
        return yaml.safe_load(f)

data = load_config()

# file_operations.py
import random
import string
from checkers import checkout


def make_folders(data):
    return checkout("mkdir {} {} {} {}".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"]), "")


def clear_folders(data):
    return checkout("rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"]), "")


def make_files(data):
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout("cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"], filename, data["bs"]), ""):
            list_of_files.append(filename)
    return list_of_files

# stat_operations.py
from checkers import getout, checkout
from datetime import datetime


def get_load_average():
    return getout("cat /proc/loadavg")


def write_to_stat_file(data, stat):
    checkout("echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(datetime.now().strftime("%H:%M:%S.%f"), data["count"], data["bs"], stat), "")

# fixtures.py
import pytest
from datetime import datetime
from config import data
from file_operations import make_folders, clear_folders, make_files
from stat_operations import get_load_average, write_to_stat_file


@pytest.fixture()
def make_folders_fixture():
    return make_folders(data)


@pytest.fixture()
def clear_folders_fixture():
    return clear_folders(data)

# main_test_file.py
import pytest
from config import data
from fixtures import make_folders_fixture, clear_folders_fixture, make_files_fixture, make_subfolder_fixture, print_time_fixture, make_bad_arx_fixture, stat_fixture


