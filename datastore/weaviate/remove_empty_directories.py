import os
import datetime

import luigi

from delete_non_md_files import DeleteNonMdFiles

from utils.logger import Logger
from utils.config import ACTION, STAT, DATA

logger = Logger()

class RemoveEmptyDirectories(luigi.Task):
    """
    Task to remove all empty directories from a specified directory
    and its subdirectories.

    Parameters:
    directory: str
        The directory from which empty directories should be removed.
        Default is DATA['LAKE'].
    date_time: str
        The date and time when the task is run, used for logging.
        Default is the current date and time.

    Attributes:
    total_files: int
        The total number of directories processed.
    exceptions: list
        List of tuples containing directory paths and associated exceptions.
    total_success_count: int
        The total number of successful deletions.
    total_exception_count: int
        The total number of deletions that resulted in exceptions.

    Returns:
    This task does not return any value. The result is the removal of empty directories.
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
        of the DeleteNonMdFiles task.

        Returns:
        An instance of the DeleteNonMdFiles task.
        """
        return DeleteNonMdFiles()

    def run(self):
        """
        The main execution method for this task. Traverses the specified directory
        and removes all empty directories.

        Returns:
        None
        """
        DIRECTORY = os.path.join(os.getcwd(), self.directory)
        if not os.path.exists(DIRECTORY):
            with self.output().open('w') as out_file:
                logger.error(ACTION['ERROR'], f"No Directory found: {DIRECTORY}")
                out_file.write(f"{STAT['ERROR']} - No Directory found: {DIRECTORY}\n")
                logger.halt()

        # Traverse directory recursively
        for root, dirs, _ in os.walk(DIRECTORY, topdown=False):
            for name in dirs:
                full_dir_path = os.path.join(root, name)
                self.total_files += 1
                # Check if the directory is empty
                if not os.listdir(full_dir_path):
                    try:
                        logger.ok(ACTION['START'], f"remove {full_dir_path}")
                        os.rmdir(full_dir_path)
                        self.total_success_count += 1
                        logger.ok(ACTION['END'], f"remove {full_dir_path}")
                    except Exception as e:
                        logger.walk(ACTION['EXCEPTION'], f"{str(full_dir_path)}")
                        self.exceptions.append((str(full_dir_path), str(e)))
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
        the status of each deletion.

        Returns:
        An instance of luigi.LocalTarget representing the log file.
        """
        return luigi.LocalTarget(f'logs/{self.date_time}_remove_empty_directories.log')

if __name__ == "__main__":
    luigi.build([RemoveEmptyDirectories()], local_scheduler=False)
