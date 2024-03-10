"""Contains basic configuration like default timeout for waits, browsers, names of files, folders and paths to files and folders."""
from os import path


# Default timeout for waits in seconds.
timeout_default = 20

# Browsers for which tests shall be run. Conftest.py is prepared to run tests in "chrome" and "firefox".
browsers = ["chrome", "firefox"]

# Name of folder where test reports are stored (it is under folder "Tests" where file with test and other test related files reside).
reports_folder = "Reports"

# Name and location of folder where screenshots are stored in case of failed assertion or exception for actual test.
# It is stored under "Reports" folder.
screenshots_folder = "Screenshots"
path_screenshots_folder = path.join(reports_folder, screenshots_folder)

# Filename of temporary file that stores URLs recorded in case of failed assertions or exception for actual test.
# It is stored via pytest fixture "tmp_path".
urls_filename = "urls.txt"
