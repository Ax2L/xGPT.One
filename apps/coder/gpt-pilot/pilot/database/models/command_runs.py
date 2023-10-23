from peewee import *

from database.models.components.base_models import BaseModel
from database.models.app import App


class CommandRuns(BaseModel):
    id = AutoField()
    app = ForeignKeyField(App, on_delete='CASCADE')
    command = TextField(null=True)
    cli_response = TextField(null=True)
    previous_step = ForeignKeyField('self', null=True, column_name='previous_step')
    high_level_step = CharField(null=True)

    class Meta:
        table_name = 'command_runs'
        indexes = (
            (('app', 'previous_step', 'high_level_step'), True),
        )