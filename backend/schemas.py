from datetime import datetime
from typing import Union

import sqlalchemy
from pydantic import BaseModel


class UserCreditBaseSchema(BaseModel):
    issuance_date: datetime
    returned: bool
    body: float
    percent: float


class ActiveCreditSchema(UserCreditBaseSchema):
    return_date: datetime
    overdue_days: int
    body_payments: float
    percent_payments: float


class ClosedCreditSchema(UserCreditBaseSchema):
    actual_return_date: datetime
    total_payment: float


UserCreditResponseSchema = list[Union[ActiveCreditSchema, ClosedCreditSchema]]


class PlanResponseSchema(BaseModel):
    message: str


class PlanPerformanceSchema(BaseModel):
    month: str
    category: str
    plan_amount: float
    actual_amount: float
    performance_percentage: float


ListPlanPerformanceSchema = list[PlanPerformanceSchema]
