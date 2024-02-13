"""Contains names of files, folders and paths to files and folders."""
from os import path


# Name of folder where test reports are stored (it is under folder "Tests" where file with test and other test related files reside).
reports_folder = "Reports"

# Name and location of folder where screenshots are stored in case of failed assertion, exception or error for actual test.
# It is stored under "Reports" folder.
screenshots_folder = "Screenshots"
path_screenshots_folder = path.join(reports_folder, screenshots_folder)

# Filename and location of temporary file that stores urls recorded in case of failed assertion, exception or error for actual test.
# It is stored under "Reports" folder.
urls_filename = "urls.txt"
path_urls_file = path.join(reports_folder, urls_filename)
