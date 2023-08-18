import subprocess


def checkout(cmd, text): 
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8') 
    print(result.stdout) 

    
    if text in result.stdout and result.returncode == 0: 
        return True 
    else: return False
    
    


falderin = '/home/user/tst'
falderout = '/home/user/out'

#def test_step1():
    #assert checkout('cd /home/user/tst; 7z a /home/user/arh1', 'Everything is OK')



def test_step1():
    assert checkout(f'cd {falderin}; 7z a {falderout}/arh1', 'Everything is Ok'), 'test1 FAIL'


def test_step2():
    assert checkout(f'cd {falderin}; 7z u {falderout}/arh1', 'Everything is OK'), 'test2 FAIL'


def test_step3():
    assert checkout(f'cd {falderin}; 7z d {falderout}/arh1', 'Everything is Ok'), 'test3 FAIL'

# Добавить в проект тесты, проверяющие работу команд
# d (удаление из архива) и u (обновление архива). Вынести
# в отдельные переменные пути к папкам с файлами, с архивом
# и с распакованными файлами. Выполнить тесты с ключом -v.
