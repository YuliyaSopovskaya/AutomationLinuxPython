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

import pytest
from checkers import checkout, getout
import random, string
import yaml
from datetime import datetime


@pytest.fixture()
def append_stat_line():
    def _append_stat_line():
        stat = getout("cat /proc/loadavg")
        with open('stat.txt', 'a') as stat_file:
            stat_file.write("time: {} count: {} size: {} load: {}\n".format(
                datetime.now().strftime("%H:%M:%S.%f"), data["count"], data["bs"], stat))
    
    yield _append_stat_line


def test_example(make_folders, clear_folders, make_files, make_subfolder, make_bad_arx, append_stat_line):

    # вызов фикстуры
    append_stat_line()
