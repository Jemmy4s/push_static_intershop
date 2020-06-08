import os
import logging
import yaml

# create logger with 'spam_application'
logger = logging.getLogger('FileConverter')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('FileConverter.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

with open('configuration.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    serveur_path = data['serveur_path']
    ssh_key_dir = data['ssh_key_dir']
    ssh_key_path = data['ssh_key_path']
    serv_dev = data['serv_dev']
    commande = data['commande']
    projet_path = data['projet_path']

SLASH = "\\"
ROOT = 'opt/intershop/eserver1/share/system/cartridges'


def convert_java_to_target(path: str):
    list_dir = path.split('/')
    while list_dir[0] != 'src':
        del list_dir[0]
    list_dir[0] = 'target'
    list_dir[2] = 'release' + SLASH + 'lib'
    result = 'C:' + SLASH + 'ish' + SLASH + 'projects' + SLASH + 'ish-rajasmart-7' + SLASH
    element_last = ''
    for element in list_dir:
        result += element + SLASH
        element_last = element
    result = result.replace(element_last + SLASH, '')
    logger.debug("Result convert java target:{}".format(result))
    return [result, element_last]


def get_target_file(path: str):
    result_fn = convert_java_to_target(path)
    path = result_fn[0]
    result_filename = result_fn[1]
    filename = result_filename.split('.')[0]
    tab = []
    for element in os.listdir(path):
        if filename in element:
            tab.append(result_fn[0] + element)
    logger.debug(tab)
    return tab


def convert_path_windows_linux(s: str) -> str:
    return s.replace('/', '\\')


def convert_git_to_windows_path(s: str) -> str:
    return s.replace('src', projet_path)


def convert_path(line: str) -> str:
    logger.debug("convert_path  : {}".format(line))
    if line == '':
        return ''
    # VERRU :
    if 'java' in line:
        logger.error('Bad file : {}'.format(line))
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


def convert_path_target(line: str) -> str:
    if line == '':
        return ''
    line = line.split('target\\')[1]
    line = line.replace('\\', '/')
    line = '/' + ROOT + '/' + line

    return line


class Tuple:
    module_logger = logging.getLogger('')

    def __init__(self, source):
        self.source = source
        self.dest = ""
        self.status = ""
        if 'target' in source:
            self.status = 'target'
            self.dest = convert_path_target(self.source)
            self.dest = self.dest.replace('$', '\\$')
        elif 'src' in source:
            self.status = 'src'
            tmp = convert_path_windows_linux(source)
            self.source = convert_git_to_windows_path(tmp)
            self.dest = convert_path(source)


        self.source.replace('\C:', 'C:')
        logger.debug(self.toString())

    def toString(self):
        return "source : {}\n dest:{} \nstatus:{}".format(self.source, self.dest, self.status)

    def absolute_path_source(self):
        self.source = convert_git_to_windows_path(self.source)


class FileConverter:
    def __init__(self):
        self.command_file = []  # : Array(Tuple)
        self.static_file = []
        self.target_file = []

    def read(self, path):
        file = open(path, 'r')
        str_file = file.read()
        all_line = str_file.split('\n')
        # Genere les sources
        for line in all_line:
            if line == '':
                continue
            if 'java' in line:
                tab = get_target_file(line)
                for element in tab:
                    logger.debug('Ajout de :{}'.format(element))
                    self.command_file.append(Tuple(element))
            else:
                self.command_file.append(Tuple(line))

    def write(self, path):
        result = ""
        for line in self.command_file:
            result += (commande + " " + ssh_key_path + " " + line.source + " "
                       + serv_dev + "" + line.dest + "" + '\n')
        logger.debug('write() in {} : \n'.format(path) + result)
        file = open(path, 'w')
        file.write(result)

    def write_src(self):
        result = ""
        for i in range(0, len(self.command_file)):
            print(i)
            result += (commande + " " + ssh_key_path + " '" + self.command_file[i].source + "' "
                       + serv_dev + "'" + self.command_file[i].dest + "'" + '\n')
        print('write file source.bat')
        print(result)


fileConvert = FileConverter()
fileConvert.read('in.txt')
fileConvert.write(ssh_key_dir + "source.bat")
