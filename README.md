# UI test automation of Alza webpage
Basic automated UI tests of Alza webpage build on Python, Selenium and pytest, using page object model. Tests are run in Chrome and Firefox browsers, include mixed assertions (soft by default, each can be set as hard) and html report (logging steps, failures, capturing screenshots and recording URL in case of failure, located under "Tests\Reports"). Code is stored in „Python_Selenium“ folder.\
Following steps describe actions needed to run tests in PyCharm on Windows operating system. The steps are mostly described briefly so they don't cover all possible issues though some specific actions are described in more detail.

## Python installation
- Go to https://www.python.org/downloads/.
- Under „Download the latest version for Windows“ click button „Download Python \<version number\>“ and save the file.
- Run downloaded .exe file. It is OK to select „Install Now“ without any further configuration.

## Getting repository content
GitHub repository content can be downloaded in 2 ways:
1) By cloning the repository:
   - In desired folder run command "git clone https://github.com/OMGitH/Alza-Selenium-Python.git".
   - Note: A Git has to be installed on local computer. Can be downloaded from https://git-scm.com/. It is OK to leave all settings default during installation.
2) As a zip file:
   - Click green "\<\> Code" button.
   - Select "Download ZIP" and save it to desired folder.
   - Unzip downloaded .zip file.

## PyCharm installation
- Go to https://www.jetbrains.com/pycharm/download/#section=windows.
- Click „Download“ button under „PyCharm Community Edition“ and save the file.
- Run downloaded .exe file and install PyCharm. There is no need to change anything during installation.

## PyCharm configuration
- Run PyCharm. At „Import PyCharm Settings“ dialog, choose whether you want to import settings or not.
- At „Data Sharing“ choose whether you want to share data or not.
- At „Welcome to PyCharm“, click „Open“ button, go to location where „Alza-Selenium-Python“ folder is located. Open „Alza-Selenium-Python“ folder, select „Python_Selenium“ folder and click „OK“. If there is a question about trust, click „Trust Project“.
- If there is a message about Java options environment variables displayed, it is OK to close it.
- If there is a message about Invalid VCS root mapping, it is OK to close it.
- Click hamburger menu in top left corner, go to „File“ – „Settings“ – „Project: Python_Selenium“ – „Python Interpreter“ and click „Add Interpreter“ – „Add Local Interpreter...“. In following window in field „Base interpreter“ there shall be prefilled path to installled Python. If not, select it there. Click „OK“ button, virtual environment will be created. In „Python Interpreter“ field there is now path to Python in virtual environment displayed. Click „Apply“ button, close window by „OK“ button and wait for the project to get updated.
- Click hamburger menu in top left corner, go to „File“ – „Settings“ – „Tools“ – „Python Integrated Tools“:
   - In field „Package requirements file“ select „requirements.txt“ file that is in „Alza-Selenium-Python\Python_Selenium\Config“.
   - In field „Default test runner“ select „pytest“.
   - Click „Apply“ button and close window by „OK“ button.
- In project navigator go to „Python_Selenium\Tests“ and open file „tests_Alza.py“. Once file is opened, at the top of the screen there is shown message saying that package requirements are not satisfied. In the message click „Install requirements“, in displayed window leave all packages ticked, click „Install“ button and wait for the packages to get installed.

## Test execution
- In PyCharm in project navigator open file „tests_Alza.py“ that is in „Python_Selenium\Tests“.
- At „class TestsAlza“ and each test (def \<name of test\>) there is a green arrow on the left.
- Click the arrow and select „Run 'pytest for tests_Alz...'“ at particular test to run it or at class to run all tests.
- Note: First run may take longer to start as webdrivers are downloaded.
