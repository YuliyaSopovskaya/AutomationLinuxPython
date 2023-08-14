#Тестирование cli в linux без использования фреймворков
#Задание 1.
#Условие:
#Написать функцию на Python, которой передаются в качестве параметров команда и текст.
#Функция должна возвращать True, если команда успешно выполнена и текст найден в её выводе и False в противном случае.
#Передаваться должна только одна строка, разбиение вывода использовать не нужно.

import subprocess

def test_command_output(command, text):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0 and text in result.stdout
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


#использование функции
command = "ls /home"
text_to_find = "user"
result = test_command_output(command, text_to_find)
if result:
    print("Текст найден в выводе команды.")
else:
    print("Текст не найден в выводе команды.")
