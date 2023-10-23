import os
import subprocess
import glob
import datetime

import luigi

from convert_ipynb_to_myst import ConvertIPYNBtoMyst

from utils.logger import Logger
from utils.config import ACTION, STAT, DATA

logger = Logger()

class ConvertPytoMd(luigi.Task):
    """
    Task to convert Python (.py) files to markdown (.md) files
    using the jupytext command line tool. The conversion is done in two steps:
    first, the .py files are converted to Jupyter notebook (.ipynb) files,
    then the .ipynb files are converted to .md files.

    Parameters:
    directory: str
        The directory where the .py files to be converted are located.
        Default is DATA['LAKE'].
    date_time: str
        The date and time when the task is run, used for logging.
        Default is the current date and time.

    Attributes:
    total_files: int
        The total number of .py files processed.
    errors: list
        List of tuples containing file paths and associated errors.
    exceptions: list
        List of tuples containing file paths and associated exceptions.
    total_success_count: int
        The total number of successful conversions.
    total_error_count: int
        The total number of conversions that resulted in errors.
    total_exception_count: int
        The total number of conversions that resulted in exceptions.

    Returns:
    This task does not return any value. The result is the conversion of .py files to .md files.
    """

    default_directory = DATA['LAKE_EXTRAS']
    default_date_time = datetime.datetime.now().strftime(DATA["DATETIME"])

    directory = luigi.Parameter(default=default_directory)
    date_time = luigi.Parameter(default=default_date_time)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_files = 0
        self.errors = []
        self.exceptions = []
        self.total_success_count = 0
        self.total_error_count = 0
        self.total_exception_count = 0

    def requires(self):
        """
        Specifies the dependency of this task. This task requires the completion
        of the ConvertIPYNBtoMyst task.

        Returns:
        An instance of the ConvertIPYNBtoMyst task.
        """
        return ConvertIPYNBtoMyst()

    def run(self):
        """
        The main execution method for this task. Walks through the specified directory
        and converts all .py files to .md files using jupytext.

        Returns:
        None
        """
        DIRECTORY = os.path.join(os.getcwd(), self.directory)
        for file in glob.glob(f"{DIRECTORY}/**/*.py", recursive=True):
            if file.endswith(".py"):
                self.total_files += 1
                try:
                    logger.ok(ACTION['START'], f"{file} to md")
                    subprocess.check_call(['jupytext', '--to', 'ipynb', file])
                    ipynb_file = file.rsplit('.', 1)[0] + '.ipynb'
                    subprocess.check_call(['jupytext', '--to', 'md', ipynb_file])
                    os.remove(file)
                    os.remove(ipynb_file)
                    self.total_success_count += 1
                    logger.ok(ACTION['END'], f"{file} to md")

                except subprocess.CalledProcessError as e:
                    logger.walk(ACTION['EXCEPTION'], f"{file}")
                    self.total_error_count += 1
                    self.errors.append((file, str(e)))

                except Exception as e:
                    logger.walk(ACTION['EXCEPTION'], f"{file}")
                    self.total_exception_count += 1
                    self.exceptions.append((file, str(e)))

        with self.output().open('w') as out_file:
            logger.ok(STAT['TOTAL_OK'], self.total_success_count)
            logger.error(STAT['TOTAL_ERROR'], self.total_error_count)
            logger.walk(STAT['TOTAL_EXCEPTION'], self.total_exception_count)

            out_file.write(f"{STAT['TOTAL_PROCESSED']}: {self.total_files}\n")
            out_file.write(f"{STAT['TOTAL_OK']}: {self.total_success_count}\n")
            out_file.write(f"{STAT['TOTAL_ERROR']}: {self.total_error_count}\n")
            out_file.write(f"{STAT['TOTAL_EXCEPTION']}: {self.total_exception_count}\n")

            if self.errors:
                out_file.write(f"\n{ACTION['ERROR']} - Error List:\n")
                for full_file_path, error in self.errors:
                    out_file.write(f"{ACTION['ERROR']} - File: {full_file_path}\n")
            else:
                out_file.write(f"{ACTION['OK']} - No Errors Found!\n")

            if self.exceptions:
                out_file.write("\n{ACTION['EXCEPTION']} - Exception List:\n")
                for full_file_path, error in self.exceptions:
                    out_file.write(f"{ACTION['EXCEPTION']} - File: {full_file_path}\n")
            else:
                out_file.write(f"{ACTION['OK']} - No Exceptions Found!\n")

    def output(self):
        """
        Specifies the output of this task. The output is a log file containing
        the status of each conversion.

        Returns:
        An instance of luigi.LocalTarget representing the log file.
        """
        return luigi.LocalTarget(f'{DATA["LOGS"]}/{self.date_time}_convert_py_to_md.log')

if __name__ == "__main__":
    luigi.build([ConvertPytoMd()], local_scheduler=False)
