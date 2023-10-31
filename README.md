# Alza
Basic automated UI tests of Alza webpage that use Python, Selenium and pytest. The tests can be found in folder „Python_Selenium“. Following steps describe actions needed to run tests on Windows operating system in Chrome web browser. The steps are mostly described briefly so they don't cover all possible issues though some specific actions are described in more detail.

## Python installation
- Go to https://www.python.org/downloads/.
- Under „Download the latest version for Windows“ click button „Download Python <version>“ and save the file.
- Run downloaded .exe file. It is OK to select „Install Now“ without any further configuration.

## Repository cloning and adding webdriver to Path
- Clone GitHub repository at https://github.com/OMGitH/Alza-Selenium-Python to desired folder.
- Chrome webdriver is located in „Alza-Selenium-Python\Python_Selenium\Config\chromedriver.exe”. Add this webdriver to „Path“:
```
- Right click on start icon and select „System“.
- Click „Advanced system settings“ on the right.
- Open „Advanced“ tab and click „Environment Variables…“.
- In window „User variables for <user name>“ select „Path“ and click „Edit…“.
- Click „New“ and provide path to driver (for example if driver is in folder „C:\Projects\Alza-Selenium-Python\Python_Selenium\Config\chromedriver.exe”, then in „Path“ shall be „C:\Projects\Alza-Selenium-Python\Python_Selenium\Config”).
- Close all the dialog windows by clicking „OK“ button.
- NOTE: If webdriver is added to „Path“ when PyCharm is running, then PyCharm has to be closed and run again in order for the change to take effect.
```

## PyCharm installation
- Go to https://www.jetbrains.com/pycharm/download/#section=windows.
- Click „Download“ button in „Community“ section and save the file.
- Run downloaded .exe file and install PyCharm. There is no need to change anything during installation.

## PyCharm configuration
- Run PyCharm. At „Import PyCharm Settings“ dialog, choose whether you want to import settings or not.
- At „Welcome to PyCharm“, click „Open“ icon, go to folder where „Alza-Selenium-Python“ folder is located. Open „Alza-Selenium-Python“ folder, select „Python_Selenium“ folder and click „OK“. If there is a question about trust, click „Trust Project“.
- If there is a message about Java options environment variables displayed, it is OK to close it.
- Go to „File“ – „Settings“ – „Project: Python_Selenium“ – „Python Interpreter“ and click „Add interpreter“ – „Add Local Interpreter“. In following window in field „Base interpreter“ there shall be prefilled path to installled Python. If not, select it there. Click „OK“ button. Virtual environment will be created. In „Python Interpreter“ field there is now path to Python in virtual environment displayed. Click „Apply“ button and close window by „OK“ button.
- Go to „File“ – „Settings“ – „Tools“ – „Python Integrated Tools“. In field „Package requirements file“ select „requirements.txt“ file that is in „Alza-Selenium-Python\Python_Selenium\Config\requirements.txt“. Click „Apply“ button and close window by „OK“ button.
- In project navigator go to „Python_Selenium\Tests“ and open file „tests_Alza.py“. Once file is opened, at the top of the screen there is shown message saying that requirements are not installed. In the message click „Install requirements“ and in displayed window leave all packages ticked and click „Install“ button.
- Once packages get installed, go to „File“ – „Settings“ – „Tools“ – „Python Integrated Tools“ and in field „Default test runner“ select „pytest“ and confirm by clicking „OK“ button.

## Test execution
- In PyCharm in project navigator open file „tests_Alza.py“ that is in „Python_Selenium\Tests“.
- At „class TestsAlza“ and each test (def) there is a green arrow on the left.
- Click the arrow and select „Run ‚pytest for …‘“ at particular test to run it or at class to run all tests.