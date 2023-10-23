import os
import re
import datetime

import luigi

from remove_empty_directories import RemoveEmptyDirectories

from utils.logger import Logger
from utils.config import ACTION, STAT, DATA

logger = Logger()

class CleanupCode(luigi.Task):
    """
    Task to clean up code in Markdown (.md) files within a specified directory
    and its subdirectories. The cleanup is performed using regular expressions to
    find and replace or remove certain patterns in the code.

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

    Returns:
    This task does not return any value. The result is the cleanup of code in .md files.
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

    def requires(self):
        """
        Specifies the dependency of this task. This task requires the completion
        of the RemoveEmptyDirectories task.

        Returns:
        An instance of the RemoveEmptyDirectories task.
        """
        return RemoveEmptyDirectories()

    def run(self):
        """
        The main execution method for this task. Walks through the specified directory
        and cleans up code in all .md files.

        Returns:
        None
        """
        DIRECTORY = os.path.join(os.getcwd(), self.directory)
        for root, dirs, files in os.walk(DIRECTORY):
            for file in files:
                if file.endswith('.md'):
                    self.total_files += 1
                    try:
                        logger.ok(ACTION['START'], f"cleanup {file}")
                        self.update_md_file_by_regexp(os.path.join(root, file))
                        self.total_success_count += 1
                        logger.ok(ACTION['START'], f"cleanup {file}")
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

    def update_md_file_by_regexp(self, file_path):
        """
        Reads a .md file, performs the cleanup operations, and writes the cleaned-up
        content back to the file.

        Parameters:
        file_path: str
            The path to the .md file to be cleaned up.

        Returns:
        None
        """
        with open(file_path, 'r') as file:
            data = file.read()

        # Update by these patterns
        remove_empty_code_blocks = re.sub(r"```\n\n```({code-cell} ipython[23]?|python)", "", data, flags=re.DOTALL)
        replace_code_cell_blocks = re.sub(r"```{code-cell} ipython[23]?", "```python", remove_empty_code_blocks, flags=re.DOTALL)
        remove_extra_newlines = re.sub(r"(\n+)?```", "\n```", replace_code_cell_blocks, flags=re.DOTALL)
        remove_triple_plus_blocks = re.sub(r"[\n+]?\+\+\+( \{.*\})?", "", remove_extra_newlines, flags=re.DOTALL)
        remove_id_blocks = re.sub(r":id: [a-zA-Z0-9-_]+\n", "", remove_triple_plus_blocks, flags=re.DOTALL)
        remove_empty_python_blocks = re.sub(r"```python\n```", "", remove_id_blocks, flags=re.DOTALL)
        replace_remaining_code_blocks = re.sub(r"```({code-cell}|pycon)", "```python", remove_empty_python_blocks, flags=re.DOTALL)

        # Write the updated data back to the file
        with open(file_path, 'w') as file:
            file.write(replace_remaining_code_blocks)

    def output(self):
        """
        Specifies the output of this task. The output is a log file containing
        the status of each cleanup operation.

        Returns:
        An instance of luigi.LocalTarget representing the log file.
        """
        return luigi.LocalTarget(f'{DATA["LOGS"]}/{self.date_time}_cleanup_code.log')

if __name__ == "__main__":
    luigi.build([CleanupCode()], local_scheduler=False)
