import json
import os

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from components.demogpt.controllers import checkDTypes
from components.demogpt.utils import refine

from . import prompts


class Chains:
    @classmethod
    def setLlm(
        cls,
        model,
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        temperature=0.0,
        openai_api_base=None,
    ):
        cls.llm = ChatOpenAI(
            model=model,
            openai_api_key=openai_api_key,
            temperature=temperature,
            openai_api_base=openai_api_base,
        )

    @classmethod
    def getChain(cls, system_template="", human_template="", **kwargs):
        prompts = []
        if system_template:
            prompts.append(SystemMessagePromptTemplate.from_template(system_template))
        if human_template:
            prompts.append(HumanMessagePromptTemplate.from_template(human_template))
        chat_prompt = ChatPromptTemplate.from_messages(prompts)
        return LLMChain(llm=cls.llm, prompt=chat_prompt).run(**kwargs)

    @classmethod
    def plan(cls, instruction):
        return cls.getChain(
            system_template=prompts.plan.system_template,
            human_template=prompts.plan.human_template,
            instruction=instruction,
        )

    @classmethod
    def tasks(cls, instruction, plan):
        task_list = cls.getChain(
            system_template=prompts.tasks.system_template,
            human_template=prompts.tasks.human_template,
            instruction=instruction,
            plan=plan,
        )
        return json.loads(task_list)

    @classmethod
    def taskController(cls, tasks):
        return checkDTypes(tasks)

    @classmethod
    def refineTasks(cls, instruction, tasks, feedback):
        task_list = cls.getChain(
            system_template=prompts.task_refiner.system_template,
            human_template=prompts.task_refiner.human_template,
            instruction=instruction,
            tasks=tasks,
            feedback=feedback,
        )

        return json.loads(task_list)

    @classmethod
    def draft(cls, instruction, code_snippets, plan):
        code = cls.getChain(
            system_template=prompts.combine.system_template,
            human_template=prompts.combine.human_template,
            instruction=instruction,
            code_snippets=code_snippets,
            plan=plan,
        )
        return refine(code)

    @classmethod
    def feedback(cls, instruction, code):
        return cls.getChain(
            system_template=prompts.feedback.system_template,
            human_template=prompts.feedback.human_template,
            instruction=instruction,
            code=code,
        )

    @classmethod
    def refine(cls, instruction, code, feedback):
        code = cls.getChain(
            system_template=prompts.refine.system_template,
            human_template=prompts.refine.human_template,
            instruction=instruction,
            code=code,
            feedback=feedback,
        )
        return refine(code)

    @classmethod
    def final(cls, draft_code):
        code = cls.getChain(
            system_template=prompts.final.system_template,
            human_template=prompts.final.human_template,
            draft_code=draft_code,
        )
        return refine(code)
