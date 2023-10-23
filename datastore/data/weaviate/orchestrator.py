import os
import datetime

import luigi

from upsert import Upsert

from utils.config import ACTION, DATA
from utils.logger import Logger

logger = Logger()

class Orchestrator(luigi.WrapperTask):
    """
    Orchestrator class is a luigi.WrapperTask for managing all the tasks of the data pipeline.

    :param repo_url: URL of the repository
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
        Function to define the dependencies of the Orchestrator task.

        :return: The final task, which through the requires method is sequestially linked with the rest of the tasks
        :rtype: list
        """
        logger.ok(ACTION['OK'], "Build Data Lake - Begin - Requires")

        DIRECTORY = os.path.join(os.getcwd(), self.directory)

        with self.output().open('w') as out_file:
            out_file.write(f"{ACTION['START']} - {datetime.datetime.now().strftime(DATA['DATETIME'])}\n")

        logger.ok(ACTION['OK'], "Build Data Lake - End - Requires")
        return Upsert(DIRECTORY, self.date_time)

    def run(self):
        """
        Function to run the Orchestrator task.
        """
        logger.ok(ACTION['OK'], "Build Data Lake - Begin - Run")

        with self.output().open('w') as out_file:
            out_file.write(f"{ACTION['END']} - {datetime.datetime.now().strftime(DATA['DATETIME'])}\n")

        logger.ok(ACTION['OK'], "Build Data Lake - Begin - End")

    def output(self):
        """
        Function to define the output of the Orchestrator task.

        :return: Output of the Orchestrator task
        :rtype: luigi.LocalTarget
        """
        return luigi.LocalTarget(f'{DATA["LOGS"]}/{self.date_time}_orchestrator.log')

# Run the Orchestrator task
if __name__ == "__main__":
    luigi.build([Orchestrator()], local_scheduler=False)
