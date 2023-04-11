#!/usr/bin/python3
# -*- encoding: utf-8 -*-

def wdm(browser=1, download=False, latest=False):
    '''
    wdm : webdriver_manager
    #TODO
    # import WebDriverService and Options of any browser selected.
    # [firefox, chrome, edge, ie]
    # and install there wdm if not exists

    #  . geckodriver    for firefox
    #  . chromedriver   for chrome
    #  . edgedriver     for edge
    #  . IEDriverServer for ie
    
    PipManager
    #TODO
    # Install pip if not installed
    # Update  pip if not updated
    # Install "selenium" & "webdriver_manager"
    # Install requirements.txt if exists

    >>> from ae_libs.pip_installer import PipInstaller
    >>> 
    >>> PipInstaller()(['selenium', 'webdriver_manager'])
    
    Usage of wdm(browser='', download=False, latest=False)
    >>> 
    >>> from ae_libs.wdm import wdm
    >>> 
    
    # parameters:
        # Firefox, Chrome, Edge or Ie.
        browser = 1, 2, 3 or 4

        # check for webdriver in localstorage if False else from net.
        download = False or True

        # the latest version in localstorage only.
        latest = False or True
    
    >>> info = wdm(browser=1, download=False, latest=False)
    >>> BROWSER, WebDriver, DriverOptions, wdm_path, Service = info
    >>> 
    >>> options = DriverOptions()
    >>> options.headless = False
    >>> 
    >>> dr = WebDriver(options=options, service=Service(wdm_path))
    >>> dr.get("https://google.com")
    >>> dr.quit()
    >>> 
    '''
    import os
    print('cwd: ', os.getcwd())
    
    try:
        from ae_libs.pip_installer import PipInstaller
        PipInstaller()(['selenium', 'webdriver_manager'])
    except:
        pass
    print('\n\n====[ WDM ]======')
    try:
        browsers = {
                1: ('Firefox', 'geckodriver'),
                2: ('Chrome', 'chromedriver'),
                3: ('Edge', 'edgedriver'),
                4: ('Ie', 'IEDriverServer')
                }
        BROWSER  = browser or input('''
        1 - Firefox
        2 - Chrome
        3 - Edge
        4 - Ie
        default(1): Firefox
        > ''').strip()
        BROWSER = int(BROWSER)
        assert BROWSER in browsers
    except:
        BROWSER = 1

    BROWSER, DRIVER = browsers[BROWSER]

    # browser, Service, driver, DriverOptions, DriverManager
    if  BROWSER  == 'Edge':
        from    selenium.webdriver.edge.service     import  Service
        from    selenium.webdriver                  import  Edge as WebDriver, EdgeOptions as DriverOptions
        from    webdriver_manager.microsoft         import  EdgeChromiumDriverManager as DriverManager
    elif BROWSER == 'Ie':
        from    selenium.webdriver.id.service       import  Service
        from    selenium.webdriver                  import  Ie as WebDriver, IeOptions as DriverOptions
        from    webdriver_manager.microsoft         import  IeDriverManager as DriverManager
    elif BROWSER == 'Chrome':
        from    selenium.webdriver.chrome.service   import  Service
        from    selenium.webdriver                  import  Chrome as WebDriver, ChromeOptions as DriverOptions
        from    webdriver_manager.chrome            import  ChromeDriverManager as DriverManager
    else:          # Firefox
        from    selenium.webdriver.firefox.service  import  Service
        from    selenium.webdriver                  import  Firefox as WebDriver, FirefoxOptions as DriverOptions
        from    webdriver_manager.firefox           import  GeckoDriverManager as DriverManager
    
    # wdm_path
    # /home/ali/.wdm/drivers/geckodriver/linux64/0.33/geckodriver
    # /home/ali/.wdm/drivers/IEDriverServer/linux64/latest/IEDriverServer.exe
    
    from datetime import datetime
    from json import load
    from time import sleep
    from os import getlogin, sep, path

    if  sep == '/':
        wdm = f'/home/{getlogin()}/.wdm/'
    else:
        wdm = 'C:\\Users\\{}\\.wdm\\'
        if  not path.exists(wdm.format('Administrator')):
            wdm = wdm.format(getlogin())
    try:
        assert not download
        drivers = load(open(f'{wdm}drivers.json'))
    except:
        drivers = {}
    
    old_timestamp = datetime.fromisoformat('2022-02-22')
    
    options = DriverOptions()
    options.headless = True
    
    wdm_path = ''

    for _wdm, wdm_info in drivers.items():
        print(f'\n[ .. ] check wdm: {_wdm}', end='\r')
        if  DRIVER not in _wdm:
            print('[ NO ]')
            continue
        try:
            # get latest one
            assert latest
            timestamp = '-'.join(wdm_info['timestamp'].split('-')[::-1])
            assert timestamp > old_timestamp
            wdm_path = wdm_info['binary_path']
            old_timestamp = timestamp
        except:pass
        try:
            # get any one
            assert not latest
            _wdm_path = wdm_info['binary_path']
            dr = WebDriver(options=options, service=Service(_wdm_path))
            print('[ OK ]')
            sleep(6)
            dr.quit()
            wdm_path = _wdm_path
            break
        except:
            sleep(2)

    # Download wdm .
    print(f'Installing {BROWSER} - {DRIVER} wdm...')
    if  not wdm_path or download:
        wdm_path = DriverManager().install()
    else:
        print(':: Exist ::')
    print(f'\nwdm_path: "{wdm_path}"\n')
    return BROWSER, WebDriver, DriverOptions, wdm_path, Service
