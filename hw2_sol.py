# Создать отдельный файл для негативных тестов. Функцию
# проверки вынести в отдельную библиотеку. Повредить архив
# (например, отредактировав его в текстовом редакторе). Написать
# негативные тесты работы архиватора с командами распаковки
# (e) и проверки (t) поврежденного архива.


#создать файл archive_tests.py для негативных тестов

import subprocess
import shutil
import os


def check_output(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    return text in result.stdout and result.returncode == 0


def corrupt_archive(archive_path):
    with open(archive_path, 'a') as archive:
        archive.write('corruption')


def test_unpack_corrupted_archive():
    falderin = '/home/user/tst'
    falderout = '/home/user/out'
    archive_path = f'{falderout}/arh1.7z'
    
    
    #повреждаем архив
    shutil.copy(f'{falderout}/arh1.7z', archive_path)
    corrupt_archive(archive_path)
    
    #тест распаковки поврежденного архива
    assert not check_output(f'7z e {archive_path} -o{falderout}', 'Everything is Ok'), 'test_unpack_corrupted_archive FAIL'


def test_test_corrupted_archive():
    falderin = '/home/user/tst'
    falderout = '/home/user/out'
    archive_path = f'{falderout}/arh1.7z'
    
    
    shutil.copy(f'{falderout}/arh1.7z', archive_path)
    corrupt_archive(archive_path)
    
    assert not check_output(f'7z t {archive_path}', 'Everything is Ok'), 'test_test_corrupted_archive FAIL'

if __name__ == '__main__':
    test_unpack_corrupted_archive()
    test_test_corrupted_archive()
    print('Tests completed.')

#создаем библиотеку archive_utils.py для функций

import subprocess


def check_output(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    return text in result.stdout and result.returncode == 0


def corrupt_archive(archive_path):
    with open(archive_path, 'a') as archive:
        archive.write('corruption')
