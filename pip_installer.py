#!/usr/bin/python
# -*-encoding: utf-8 -*-

# By:
#   ali elainous
#   telegram: @ba3lwan
#

from http.client import HTTPSConnection as Https

import subprocess, re, os

class PipInstaller:
    '''
    >>> from ae_libs import PipInstaller

    . Install & Update pip
    >>> PipInstaller()()

    . install module(s) / requirements.txt
    >>> PipInstaller.install_module("requests")

    . (code, status, msg) returned of functions
    (0, 'NOT_UPDATED)
    (1, 'UPDATED')
    (2, 'INSTALLED')
    (3, 'DOMAIN_ERR', domain)
    (4, 'NOT_INSTALLED')
    (5, 'ELSE', err)
    '''
    
    def __init__(self):
        pass
    
    def _get(self, domain, url_path='/'):
        f'''
        returned:
            3- {domain}{url_path} error.
            5- else (network).
        '''
        try:
            print()
            print(f'\n[ .... ] Downloading "{domain}{url_path}"', end='\r')
            conn = Https(domain)
            conn.request('GET', url_path)
            response = conn.getresponse()
            assert response.status == 200
            content = response.read().decode()
            conn.close()
            print('[ DONE ]')
            return content
        except AssertionError:
            print('[ FAIL ]')
            return (3, 'DOMAIN_ERR', domain)
        except Exception as err:
            print('[ FAIL ]')
            return (5, 'ELSE', err)
    
    def _is_updated(self, is_installed=False):
        '''
        returned:
            0- pip not updated.
            1- pip updated.
            2- pip installed.
            3- pipi.org error.
            4- pip not installed.
            5- else (network).
        '''
        try:
            from pip import __version__ as this_version
            
            if  is_installed:
                return (2, 'INSTALLED')
            content = self._get('pypi.org', '/project/pip/')

            new_version = re.findall(r'class="package-header__name">([\w\W]+?)<', content)
            new_version = new_version[0].strip().split()[-1]
            
            assert this_version >= new_version, 'update'
            self._update_pip_version(new_version)
            return (1, 'UPDATED')
        except TypeError:
            return content # 3 or 4, pypi_err or else
        except AssertionError as err:
            return (0, 'NOT_UPDATED') if err.args else content
        except ImportError as err:
            # module = err.args[0].split("'")[-2]
            # return 3 if module == 'pip' else 4
            
            return (4, 'NOT_INSTALLED')
        except Exception as err:
            return (5, 'ELSE', err)
    
    def update(self):
        print('\n[ ..... ] Updating pip', end='\r')
        if  'INSTALLED' not in self._is_updated(is_installed=True):
            print('[ FAIL  ]\nNOT_INSTALLED')
            return (4, 'NOT_INSTALLED')
        if  'UPDATED' in self._is_updated():
            print('[ Updte ]')
            return (1, 'UPDATED')
        
        try:
            from pip._internal.cli.main import main as pip_install
        
            assert pip_install(['install', '-U', 'pip']) == 0
            print('[ Updte ]')
            return (1, 'UPDATED')
        except:
            pass
        # TODO using system cmd
        py = self.get_py()
        try:
            assert os.system(f'{py} -m pip install -U pip')
            print('[ FAIL  ]')
            return (0, 'NOT_UPDATED')
        except:
            print('[ Updte ]')
            return (1, 'UPDATED')

    def get_py(self):
        for interpreter in ('py', 'python', 'python3'):
            if  self._exec_cmd(interpreter):
                return interpreter
        else:
            quit('ERROR: please check for your python interpreter; "py" or "python"')

    def _exec_cmd(self, cmd):
        try:
            proc = subprocess.Popen(cmd)
            proc.kill()
            return True
        except:
            return False

    def install_pip(self):
        print('\n[ ..... ] Installing pip', end='\r')
        if  'INSTALLED' in self._is_updated(is_installed=True):
            print('[ Exist ]')
            return ('2', 'INSTALLED')

        # python interpreter
        py = self.get_py()

        print('\nfrom bootstrap.pypa.io ...\n')
        try:
            # install pip from get-pip.
            module = 'get_pip'
            content = self._get('bootstrap.pypa.io', '/get-pip.py')

            if  os.path.exists(f'{module}.py'):
                module += '_1'
            with open(f'{module}.py', 'w') as file:
                file.write(content)
            del content
            assert not os.system(f'{py} -m {module}')

            print('[ DONE  ]')
            return (2, 'INSTALLED')
        except AssertionError:
            print('[ FAIL  ]')
            return (4, 'NOT_INSTALLED')
        except Exception as err:
            print(f'[ FAIL  ]\nerr: {err}')
        
        # install pip from ensurepip
        assert not os.system(f'{py} -m ensurepip --upgrade'), 'pip installation failed !!'
        return (2, 'INSTALLED')
    
    def __call__(self, modules=[]):
        self.run()
        self.install_module(modules)

    def run(self):
        try:
            assert 'INSTALLED' not in self.install_pip()
            assert 'INSTALLED' not in self.install_pip()
            quit('pip installation FAILED.')
        except AssertionError:
            pass # OK
        except Exception as err:
            print(f'runErr: {err}')

        self.update()

    
    def install_module(self, modules=''):
        print('\nInstalling modules/ requirements.txt')

        if  type(modules) == str:
            modules = [modules]
        else:
            modules = list(modules) * 2
        try:
            from pip._internal.cli.main import main as pip_install
        except:
            pip_install = lambda module:None
        
        py = self.get_py()
        
        try:
            req = 'requirements.txt'
            assert os.path.exists(req)
            print(f'Install from "{req}" ...')
            assert pip_install(['install', '-r', req]) == 0, 'again'
        except AssertionError as err:
            if  err.args:
                os.system(f'{py} -m pip install -r {req}')
            else:
                print('Warning: "requirements.txt" not found !!')

        for module in modules:
            try:
                exec(f'import {module}')
                assert 0
            except ImportError:
                print(f'Install {module} ...')
            except:
                print(f'Exists: {module}')
                continue
            try:
                assert pip_install(['install', '-U', module]) == 0
                print('[ OK ]')
                continue
            except:
                pass
            os.system(f'{py} -m pip install -U {module}')

if  __name__ == '__main__':
    PipInstaller()()
