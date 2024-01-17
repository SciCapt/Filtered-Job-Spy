# Filtered Job Spy
The main program (get_jobs) for running jobs searches from anywhere. Uses [Job Spy](https://github.com/Bunsly/JobSpy) to preform user searches, then applies the user-inputted filters.

The remaining filtered jobs are saved to a CSV, and the user can immediately run through the jobs, choosing which to open to apply to. If not, the secondary program (apply_from_csv) can be used to run through the jobs in the CSV at any later time.

# Usage (EXE Files)
The primary EXE files are in the dist folder -- these were made using PyInstaller from the Python code in src. These are straight-forward click and go programs to run the job searching (get_jobs) or use a previous search's CSV to apply to some jobs (apply_from_csv). 

The Python source files are also given and explained below should you want to use them instead.

# Usage & Dependancies (Python Files)
For now, the way to use the Python files is to use them with either a virtual environment or some other Python path that has the following:

## Python
Requires version >=3.10

## Modules
- webbrowser
  - With Python versions 2.1.3 and later by default
  - Used for opening job URLs after completing the filtered search
- Pandas (handling CSVs and dataframes, EXE made with version 2.1.4)
  - Made with version 2.1.4
  - Used for handling CSVs and dataframes given by the main Job Spy function
- Job Spy (python-jobspy on PyPI)
  - Made with version 1.1.34
  - Used for the scrape_jobs function to get the job post data
