import csv
import datetime
import io

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import text
from sqlalchemy.orm import Session, joinedload

from backend.database import get_db
from backend.models import Credit, Dictionary, Payment, Plan, User
from backend.schemas import PlanResponseSchema, UserCreditResponseSchema

router = APIRouter()


@router.get("/user_credit/{user_id}", response_model=UserCreditResponseSchema)
def get_user_credit(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_credits = (
        db.query(Credit)
        .filter_by(user_id=user_id)
        .options(joinedload(Credit.payments).joinedload(Payment.payment_type))
        .all()
    )

    credit_list = []
    for credit in user_credits:

        if not credit.actual_return_date:
            body_payments = sum(
                payment.sum
                for payment in credit.payments
                if payment.payment_type.name == "тіло"
            )
            percent_payments = sum(
                payment.sum
                for payment in credit.payments
                if payment.payment_type.name == "відсотки"
            )
            overdue_days = (
                (datetime.date.today() - credit.return_date.date()).days
                if datetime.date.today() > credit.return_date.date()
                else 0
            )

            credit_list.append(
                {
                    "issuance_date": credit.issuance_date,
                    "returned": False,
                    "return_date": credit.return_date,
                    "overdue_days": overdue_days,
                    "body": credit.body,
                    "percent": credit.percent,
                    "body_payments": body_payments,
                    "percent_payments": percent_payments,
                }
            )
        else:
            total_payment = sum(payment.sum for payment in credit.payments)
            credit_list.append(
                {
                    "issuance_date": credit.issuance_date,
                    "returned": True,
                    "actual_return_date": credit.actual_return_date,
                    "body": credit.body,
                    "percent": credit.percent,
                    "total_payment": total_payment,
                }
            )

    return credit_list


@router.post(
    "/plans_insert",
    response_model=PlanResponseSchema,
    description="Upload file in CSV format with similar stucture:<br>"
    "01.07.2023\t214000\tвидача<br>"
    "01.07.2023\t1179000\tзбір<br>"
    "\nFile must include the following columns:\n"
    "1. Period (date in format DD.MM.YYYY)\n"
    "2. Summa (Number)\n"
    "3. Category (String,Category name).",
)
def plans_insert(file: UploadFile = File(...), db: Session = Depends(get_db)):
    reader = csv.reader(
        io.TextIOWrapper(file.file, encoding="utf-8"), delimiter="\t"
    )
    categories = db.query(Dictionary).all()

    # Update autoincrement for plans table
    db.execute(
        text(
            "SELECT setval(pg_get_serial_sequence('plans', 'id'), (SELECT MAX(id) FROM plans), true);"
        )
    )
    db.commit()

    for row in reader:
        period = datetime.datetime.strptime(row[0], "%d.%m.%Y").date()
        category_name = row[2]
        sum = row[1]

        if period.day != 1:
            raise HTTPException(
                status_code=400,
                detail=f"Period {period} must be the first day of the month",
            )

        if not sum.isdigit():
            raise HTTPException(
                status_code=400, detail=f"Sum must be number {sum}"
            )

        if (
            db.query(Plan)
            .join(Dictionary)
            .filter(Plan.period == period, Dictionary.name == category_name)
            .first()
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Plan with period {period} and category {category_name} already exists",
            )
        else:
            category = [
                category
                for category in categories
                if category.name == category_name
            ][0]
            plan = Plan(period=period, sum=sum, category_id=category.id)
            db.add(plan)
    db.commit()

    return {"message": "Plans successfully added"}
