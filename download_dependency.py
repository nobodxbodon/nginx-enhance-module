#! python3

import os
import sys
import argparse
import yaml

parser = argparse.ArgumentParser(description='This program can download the third-party modules contained in this library', usage='Scattered dependent file management script')
parser.add_argument('-m', '--module', dest='module', type=str,nargs='*', help='Select the module to enable')
args = parser.parse_args()

if args.module != None:
    有效模块 = args.module

print(args.module)

当前目录 = os.getcwd()

yaml文件 = 'modules.yaml'
临时目录 = 'tmp'

def 读取配置(名称):
    文件 = open(名称,'r',encoding='utf-8')
    数据 = yaml.load(文件,Loader=yaml.SafeLoader)
    return 数据

def 处理(模块,配置):
    if args.module != None and 模块 not in 有效模块:
        print(f'I: Module {模块} is not enabled, skip')
        return None
    if 'type' not in 配置:
        print(f'E: Module {模块} is missing the type field, skip')
        return
    if 'mode' not in 配置:
        print(f'E: Module {模块} is missing the mode field, skip')
        return
    类型 = 配置['type']
    模式 = 配置['mode']
    print(f'I: {模块} is the {类型} type')
    print(f'I: {模块} uses {模式} method to obtain')
    if 模式 == 'git_repo':
        if 'git_repo' not in 配置:
            print(f'E: Module {模块} is missing the download git_repo field, skip')
            return
        if 'paths' not in 配置:
            print(f'E: Module {模块} is missing the download paths field, skip')
            return
        源码库 = 配置['git_repo']
        各路径 = 配置['paths']
        print(f'I: Module {模块} performs cloning {当前目录}/{临时目录}/{类型}/{模块}')
        if os.system(f'git clone --recurse-submodules {源码库} {当前目录}/{临时目录}/{类型}/{模块}'):
            print(f'E: Module {模块} Execution command error, termination')
            sys.exit(1)
        else:
            if 类型 == 'modules':
                for 某路径 in 各路径:
                    源码路径 = f'{当前目录}/{临时目录}/{类型}/{模块}/{某路径}/*'
                    目标路径 = f'{当前目录}/{类型}/{模块}/'
                    print(f'I: Module {模块} copy {源码路径} to {目标路径} ')
                    if os.system(f'mkdir -p {目标路径} && cp -r {源码路径} {目标路径}'):
                        print(f'E: Module {模块} Execution command error, termination')
                        sys.exit(1)
            else:
                print(f'E: Modules {模块} not support {类型} type')
                sys.exit(1)
    elif 模式 == 'wget':
        if 'wget' not in 配置:
            print(f'E: Module {模块} is missing the download wget field, skip')
            return
        if 'filename' not in 配置:
            print(f'E: Module {模块} is missing the download filename field, skip')
            return
        if 'dest' not in 配置:
            print(f'E: Module {模块} is missing the download dest field, skip')
            return
        下载路径 = 配置['wget']
        文件名称 = 配置['filename']
        目标文件 = 配置['dest']
        print(f'I: Module {模块} performs download {当前目录}/{临时目录}/{类型}/{文件名称}')
        if os.system(f'wget {下载路径} -P {当前目录}/{临时目录}/{类型}'):
            print(f'E: Module {模块} Execution command error, termination')
            sys.exit(1)
        else:
            print(f'Module {模块} Start unpacking Tar.gz')
            if os.system(f'mkdir -p {当前目录}/{临时目录}/{类型}/{模块} && tar xvf {当前目录}/{临时目录}/{类型}/{文件名称} -C {当前目录}/{临时目录}/{类型}/{模块}'):
                print(f'E: Module {模块} Execution command error, termination')
                sys.exit(1)
            if 类型 == 'depends':
                源码路径 = f'{当前目录}/{临时目录}/{类型}/{模块}'
                目标路径 = f'{当前目录}/{目标文件}/{类型}/{模块}'
                print(f'I: Module {模块} copy {源码路径} to {目标路径} ')
                if os.system(f'mkdir -p {目标路径} && cp -r {源码路径} {目标路径}'):
                        print(f'E: Module {模块} Execution command error, termination')
                        sys.exit(1)
            else:
                print(f'E: Modules {模块} not support {类型} type')
                sys.exit(1)
if __name__ == '__main__':
    print('I: Check the temporary folder')
    if not os.path.exists(f'{当前目录}/{临时目录}'):
        print('I: Temporary folder does not exist, create now')
        os.mkdir(f'{当前目录}/{临时目录}')
        print('I: Temporary folder does not exist, creation' + f' {当前目录}/{临时目录}' + ' is complete')
        print('I: Check the temporary modules folder')
        if not os.path.exists(f'{当前目录}/{临时目录}/modules'):
            print('I: Temporary modules folder does not exist, create now')
            os.mkdir(f'{当前目录}/{临时目录}/modules')
            print('I: Temporary modules folder does not exist, creation' + f' {当前目录}/{临时目录}/modules' + ' is complete')
        print('I: Check the temporary depend folder')
        if not os.path.exists(f'{当前目录}/{临时目录}/depend'):
            print('I: Temporary depend folder does not exist, create now')
            os.mkdir(f'{当前目录}/{临时目录}/depend')
            print('I: Temporary depend folder does not exist, creation' + f' {当前目录}/{临时目录}/depend' + ' is complete')
        
    yaml数据 = 读取配置(f'{当前目录}/{yaml文件}')
    if yaml数据:
        for 模块,配置 in yaml数据.items():
            print(f'I: Start processing {模块} 模块')
            处理(模块,配置)
            print(f'I: Module {模块} is processed')
