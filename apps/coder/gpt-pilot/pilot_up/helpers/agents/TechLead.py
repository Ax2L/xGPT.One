from utils.utils import step_already_finished
from helpers.Agent import Agent
from utils.style import color_green_bold
from helpers.AgentConvo import AgentConvo

from utils.utils import should_execute_step, generate_app_data
from database.database import save_progress, get_progress_steps, save_feature, get_features_by_app_id
from logger.logger import logger
from const.function_calls import DEVELOPMENT_PLAN

DEVELOPMENT_PLANNING_STEP = 'development_planning'


class TechLead(Agent):
    def __init__(self, project):
        super().__init__('tech_lead', project)

    def create_development_plan(self):
        self.project.current_step = DEVELOPMENT_PLANNING_STEP
        self.convo_development_plan = AgentConvo(self)

        # If this app_id already did this step, just get all data from DB and don't ask user again
        step = get_progress_steps(self.project.args['app_id'], DEVELOPMENT_PLANNING_STEP)
        if step and not should_execute_step(self.project.args['step'], DEVELOPMENT_PLANNING_STEP):
            step_already_finished(self.project.args, step)
            self.project.development_plan = step['development_plan']
            return

        # DEVELOPMENT PLANNING
        print(color_green_bold("Starting to create the action plan for development...\n"))
        logger.info("Starting to create the action plan for development...")

        # TODO add clarifications
        llm_response = self.convo_development_plan.send_message('development/plan.prompt',
            {
                "name": self.project.args['name'],
                "app_type": self.project.args['app_type'],
                "app_summary": self.project.project_description,
                "clarifications": self.project.clarifications,
                "user_stories": self.project.user_stories,
                "user_tasks": self.project.user_tasks,
                "technologies": self.project.architecture
            }, DEVELOPMENT_PLAN)
        self.project.development_plan = llm_response['plan']

        logger.info('Plan for development is created.')

        save_progress(self.project.args['app_id'], self.project.current_step, {
            "development_plan": self.project.development_plan, "app_data": generate_app_data(self.project.args)
        })

        return

    def create_feature_plan(self, feature_description):
        self.convo_feature_plan = AgentConvo(self)
        previous_features = get_features_by_app_id(self.project.args['app_id'])

        llm_response = self.convo_feature_plan.send_message('development/feature_plan.prompt',
            {
                "name": self.project.args['name'],
                "app_type": self.project.args['app_type'],
                "app_summary": self.project.project_description,
                "clarifications": self.project.clarifications,
                "user_stories": self.project.user_stories,
                "user_tasks": self.project.user_tasks,
                "technologies": self.project.architecture,
                "directory_tree": self.project.get_directory_tree(True),
                "development_tasks": self.project.development_plan,
                "files": self.project.get_all_coded_files(),
                "previous_features": previous_features,
                "feature_description": feature_description,
            }, DEVELOPMENT_PLAN)

        self.project.development_plan = llm_response['plan']

        logger.info('Plan for feature development is created.')
        return

    def create_feature_summary(self, feature_description):
        self.convo_feature_summary = AgentConvo(self)

        llm_response = self.convo_feature_summary.send_message('development/feature_summary.prompt',
            {
                "name": self.project.args['name'],
                "app_type": self.project.args['app_type'],
                "app_summary": self.project.project_description,
                "feature_description": feature_description,
                "development_tasks": self.project.development_plan,
            })

        self.project.feature_summary = llm_response

        save_feature(self.project.args['app_id'], self.project.feature_summary, self.convo_feature_plan.messages)
        logger.info('Summary for new feature is created.')
        return
