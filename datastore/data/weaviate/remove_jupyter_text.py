import os
import re
import datetime
from pathlib import Path

import luigi

from cleanup_code import CleanupCode

from utils.logger import Logger
from utils.config import ACTION, STAT, DATA

logger = Logger()

class RemoveJupyterText(luigi.Task):
    """
    Task to remove Jupyter-specific text from Markdown (.md) files
    within a specified directory and its subdirectories. The cleanup is performed
    using regular expressions to find and remove the Jupyter-specific text.

    Parameters:
    directory: str
        The directory where the .md files to be cleaned up are located.
        Default is DATA['LAKE'].
    date_time: str
        The date and time when the task is run, used for logging.
        Default is the current date and time.

    Attributes:
    total_files: int
        The total number of .md files processed.
    exceptions: list
        List of tuples containing file paths and associated exceptions.
    total_success_count: int
        The total number of successful cleanups.
    total_exception_count: int
        The total number of cleanups that resulted in exceptions.
    pattern: str
        The regular expression pattern for the Jupyter-specific text to be removed.

    Returns:
    This task does not return any value. The result is the removal of Jupyter-specific text from .md files.
    """

    default_directory = DATA["LAKE_EXTRAS"]
    default_date_time = datetime.datetime.now().strftime(DATA["DATETIME"])

    directory = luigi.Parameter(default=default_directory)
    date_time = luigi.Parameter(default=default_date_time)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_files = 0
        self.exceptions = []
        self.total_success_count = 0
        self.total_exception_count = 0
        self.pattern = r'---\njupytext.*name: python3\n---\n'

    def requires(self):
        """
        Specifies the dependency of this task. This task requires the completion
        of the CleanupCode task.

        Returns:
        An instance of the CleanupCode task.
        """
        return CleanupCode()

    def run(self):
        """
        The main execution method for this task. Walks through the specified directory
        and removes Jupyter-specific text from all .md files.

        Returns:
        None
        """
        DIRECTORY = os.path.join(os.getcwd(), self.directory)
        for dirpath, dirnames, filenames in os.walk(DIRECTORY):
            for file in Path(dirpath).glob('*.md'):
                self.total_files += 1
                try:
                    logger.ok(ACTION['START'], f"md {file}")
                    # Read the file
                    with open(file, 'r') as f:
                        text = f.read()
                    # Remove the pattern
                    new_text = re.sub(self.pattern, '', text, flags=re.DOTALL)
                    # Write the modified contents back to the file
                    with open(file, 'w') as f:
                        f.write(new_text)
                    self.total_success_count += 1
                    logger.ok(ACTION['END'], f"md {file}")
                except Exception as e:
                    self.exceptions.append((str(file), str(e)))
                    self.total_exception_count += 1

        with self.output().open('w') as out_file:
            logger.ok(STAT['TOTAL_OK'], self.total_success_count)
            logger.walk(STAT['TOTAL_EXCEPTION'], self.total_exception_count)

            out_file.write(f"{STAT['TOTAL_PROCESSED']}: {self.total_files}\n")
            out_file.write(f"{STAT['TOTAL_OK']}: {self.total_success_count}\n")
            out_file.write(f"{STAT['TOTAL_EXCEPTION']}: {self.total_exception_count}\n")

            if self.exceptions:
                out_file.write("\n{ACTION['EXCEPTION']} - Exception List:\n")
                for full_file_path, error in self.exceptions:
                    out_file.write(f"{ACTION['EXCEPTION']} - File: {full_file_path}\n")
            else:
                out_file.write(f"{ACTION['OK']} - No Exceptions Found!\n")

    def output(self):
        """
        Specifies the output of this task. The output is a log file containing
        the status of each cleanup operation.

        Returns:
        An instance of luigi.LocalTarget representing the log file.
        """
        return luigi.LocalTarget(f'{DATA["LOGS"]}/{self.date_time}_remove_jupyter_text.log')

if __name__ == "__main__":
    luigi.build([RemoveJupyterText()], local_scheduler=False)
