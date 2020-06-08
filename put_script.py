import os
import git_status
import click
import yaml

with open('configuration.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    serveur_path = data['serveur_path']
    ssh_key_dir = data['ssh_key_dir']
    ssh_key_path = data['ssh_key_path']
    serv_dev = data['serv_dev']
    commande = data['commande']


def convert_path_windows_linux(s: str) -> str:
    return s.replace('/', '\\')


def convert_git_to_windows_path(s: str) -> str:
    return s.replace('src', 'C:\ish\projects\ish-rajasmart-7\src')


def windows_absolute_path(f):
    s = f.read()
    s = convert_path_windows_linux(s)
    s = convert_git_to_windows_path(s)
    file_result = open("convert.txt", 'w')
    file_result.write(s)
    file_result.close()
    return s


# src\rajasmart_app_bo_b2b\javasource\fr\rajasmart\intershop\bo\b2b\pipelet\GenerateExcelSelfStats.java"

# C:\ish\projects\ish - rajasmart - 7\target\rajasmart_app_bo_b2b\release\lib\fr\rajasmart\intershop\bo\b2b\pipelet\

def convert_java_to_target(path: str):
    slash = "/"
    list_dir = path.split('/')
    while list_dir[0] != 'src':
        del list_dir[0]
    list_dir[0] = 'target'
    list_dir[2] = 'release' + slash + 'lib'
    result = 'C:' + slash + 'ish' + slash + 'projects' + slash + 'ish-rajasmart-7' + slash
    elementlast = ''
    for element in list_dir:
        result += element + slash
        elementlast = element
    result = result.replace(elementlast + slash, '')
    return [result, elementlast]


def get_target_file(path: str):
    result_fn = convert_java_to_target(path)
    path = result_fn[0]
    result_filename = result_fn[1]
    filename = result_filename.split('.')[0]
    tab = []
    for element in os.listdir(path):
        if filename in element:
            tab.append(element)
    return tab


s2 = "src/rajasmart_app_bo_b2b/javasource/fr/rajasmart/intershop/bo/b2b/pipelet/GenerateExcelSelfStats.java"
print(convert_java_to_target(s2))
print(get_target_file(s2))


def convert_path(line: str) -> str:
    if line == '':
        return ''
    line = line.split('/')
    line[0] = 'opt/intershop/eserver1/share/system/cartridges'
    line[2] = 'release'
    line.remove('cartridge')
    result = ""
    for element in line:
        result = result + '/' + element
    print(result)
    return result


def create_file_with_tab(tab, filename):
    fichier = open(filename, "a")
    for element in tab:
        fichier.write(element + '\n')
    fichier.close()


def generate_serv_path(file):
    s: str = file.read()
    print(s)
    tab = s.split('\n')
    for i in range(0, len(tab)):
        tab[i] = convert_path(tab[i])
    return tab


# MAIN
def generate_push_file():
    print('read value in in.txt')
    file = open('in.txt', 'r')
    tab_dest = generate_serv_path(file)
    file = open('in.txt', 'r')
    print('convert value')
    swap = windows_absolute_path(file)
    tab_src = swap.split('\n')
    tab_result = []
    for i in range(0, len(tab_dest)):
        print(i)
        tab_result.append(commande + " " + ssh_key_path + " " + tab_src[i] + " " + serv_dev + tab_dest[i])
    print('write file source.bat')
    create_file_with_tab(tab_result, ssh_key_dir + "source.bat")


@click.group()
def cli():
    pass


@click.command()
def gitList():
    status = git_status.Status("C:/ish/projects/ish-rajasmart-7/")
    list_of_file = status.A + status.M + status.R
    create_file_with_tab(list_of_file, 'gitstatus.txt')


@click.command()
def push():
    generate_push_file()
    os.system('cd ' + ssh_key_dir)
    os.system('echo "exec source.bat"')
    print(ssh_key_dir)
    os.system('start /D "' + ssh_key_dir + '"/W source.bat')  # Pas sur que fonctionne.


@click.command()
def generateScript():
    pass


@click.command()
def start():
    pass


@click.command()
def exportLog():
    pass


@click.command()
@click.argument('id')
def restartAp(id):
    click.echo("todo")


cli.add_command(gitList)
cli.add_command(push)
cli.add_command(generateScript)
cli.add_command(restartAp)

# if __name__ == '__main__':
#     cli()
