import os
import subprocess
import shutil
import datetime

import luigi

from utils.logger import Logger
from utils.config import ACTION, DATA

logger = Logger()

class BuildDataLake(luigi.Task):
    """
    Task for building a data lake from a git repository.

    :param repo_url: URL of the git repository
    :type repo_url: str
    :param directory: Directory where the data lake will be built
    :type directory: str
    :param date_time: Current date and time
    :type date_time: str
    """
    default_repo_url = DATA["URL"]
    default_directory = DATA["LAKE"]
    default_date_time = datetime.datetime.now().strftime(DATA["DATETIME"])

    repo_url = luigi.Parameter(default=default_repo_url)
    directory = luigi.Parameter(default=default_directory)
    date_time = luigi.Parameter(default=default_date_time)

    def requires(self):
        """
        Function to define the dependencies of the BuildDataLake task.

        :return: List of dependencies of the BuildDataLake task
        :rtype: list
        """
        return None

    def run(self):
        """
        Function to run the BuildDataLake task.

        This function clones the git repository and builds a data lake in the specified directory.
        """
        DIRECTORY = os.path.join(os.getcwd(), self.directory)
        with self.output().open('w') as f:
            try:
                logger.ok(ACTION['START'], f"Build Data Lake")
                if os.path.isdir(DIRECTORY):
                    # Backup "data lake" `DIRECTORY`
                    backup_dir = f"{DIRECTORY}_{DATA['BACKUPS']}"
                    if not os.path.exists(backup_dir):
                        os.makedirs(backup_dir)
                        logger.ok(ACTION['OK'], f"Directory Creation Succeeded: {DATA['BACKUPS']}")

                    # Move the existing data lake to the backup directory
                    shutil.move(DIRECTORY, f"{backup_dir}/{self.date_time}")
                    logger.ok(ACTION['OK'], f"Backup Succeeded: {backup_dir}/{self.date_time}")
                    f.write(f"{ACTION['OK']} - Backup Succeeded: {backup_dir}/{self.date_time}\n")

                logger.walk(ACTION['START'], f"Git Clone: {self.repo_url} into {DIRECTORY}")
                # Create Git command
                command = ['git', 'clone', self.repo_url, DIRECTORY]
                # Run Git command
                process = subprocess.Popen(command, stdout=subprocess.DEVNULL)
                # Wait for the git command process to finish
                process.wait()
                logger.walk(ACTION['END'], f"Git Clone: {self.repo_url} into {DIRECTORY}")
                f.write(f"{ACTION['OK']} - Git Clone: {self.repo_url} into {DIRECTORY}\n")
                logger.ok(ACTION['END'], f"Build Data Lake")
            except Exception:
                f.write(f"{ACTION['ERROR']} - Git Clone: {self.repo_url} into {DIRECTORY}\n")
                logger.error(ACTION['ERROR'], f"Git Clone: {self.repo_url} into {DIRECTORY}")

    def output(self):
        """
        Function to define the output of the BuildDataLake task.

        :return: Output of the BuildDataLake task
        :rtype: luigi.LocalTarget
        """
        return luigi.LocalTarget(f'{DATA["LOGS"]}/{self.date_time}_build_data_lake.log')

# Run the BuildDataLake task
if __name__ == "__main__":
    luigi.build([BuildDataLake()], local_scheduler=False)
