from pydantic import BaseModel


class PredefinedTaskInterface(BaseModel):
    name: str
    description: str
    input_schema:  str
    running_function: str