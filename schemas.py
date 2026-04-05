from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    cabinet_number: str
    title: str
    problem_description: str
    id_employee: int
    id_priority: int


class ApplicationOut(BaseModel):
    id: int
    date_submission: str
    date_completion: str
    cabinet_number: str
    title: str
    problem_description: str
    id_employee: int
    id_priority: int
    id_status: int

    model_config = {
        "from_attributes": True
    }


class StatusUpdate(BaseModel):
    new_status: int
