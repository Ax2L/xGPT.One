import os
import glob
import datetime

import luigi

from convert_py_to_md import ConvertPytoMd

from utils.logger import Logger
from utils.config import ACTION, STAT, DATA

logger = Logger()

class DeleteNonMdFiles(luigi.Task):
    """
    Task to delete all non-Markdown (.md) files from a specified directory
    and its subdirectories.

    Parameters:
    directory: str
        The directory from which non-.md files should be deleted.
        Default is DATA['LAKE'].
    date_time: str
        The date and time when the task is run, used for logging.
        Default is the current date and time.

    Attributes:
    total_files: int
        The total number of files processed.
    exceptions: list
        List of tuples containing file paths and associated exceptions.
    total_success_count: int
        The total number of successful deletions.
    total_exception_count: int
        The total number of deletions that resulted in exceptions.

    Returns:
    This task does not return any value. The result is the deletion of non-.md files.
    """

    default_directory = DATA['LAKE_EXTRAS']
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
        of the ConvertPytoMd task.

        Returns:
        An instance of the ConvertPytoMd task.
        """
        return ConvertPytoMd()

    def run(self):
        """
        The main execution method for this task. Walks through the specified directory
        and deletes all non-.md files.

        Returns:
        None
        """
        DIRECTORY = os.path.join(os.getcwd(), self.directory)
        for filename in glob.iglob(f"{DIRECTORY}/**", recursive=True):
            if os.path.isfile(filename):
                self.total_files += 1
                if not filename.endswith(".md"):
                    try:
                        logger.ok(ACTION['START'], f"remove {filename}")
                        os.remove(filename)
                        self.total_success_count += 1
                        logger.ok(ACTION['END'], f"remove {filename}")
                    except Exception as e:
                        logger.walk(ACTION['EXCEPTION'], f"{filename}")
                        self.total_exception_count += 1
                        self.exceptions.append((str(filename), str(e)))

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
        the status of each deletion.

        Returns:
        An instance of luigi.LocalTarget representing the log file.
        """
        return luigi.LocalTarget(f'{DATA["LOGS"]}/{self.date_time}_delete_non_md_files.log')

if __name__ == "__main__":
    luigi.build([DeleteNonMdFiles()], local_scheduler=False)
