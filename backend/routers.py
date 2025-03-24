import csv
import datetime
import io

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy import extract, text
from sqlalchemy.orm import Session, joinedload

from backend.database import get_db
from backend.models import Credit, Dictionary, Payment, Plan, User
from backend.schemas import PlanResponseSchema, UserCreditResponseSchema

router = APIRouter()


@router.get(
    "/user_credit/{user_id}",
    response_model=UserCreditResponseSchema,
    summary="Get user credits",
    description="Method for retrieving information about a user's credits by their ID.",
)
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
    summary="Add plans from a CSV file",
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

    try:
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
                .filter(
                    Plan.period == period, Dictionary.name == category_name
                )
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
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail="Please input the correct document structure",
        )
    db.commit()

    return {"message": "Plans successfully added"}


@router.get(
    "/plans_performance",
    summary="Get plans performance",
    description="A method for obtaining information about "
    "the implementation of plans for a specific date.",
)
def get_plans_performance(
    check_date: datetime.date = Query(
        description="Date for checking plan execution in YYYY-MM-DD format",
    ),
    db: Session = Depends(get_db),
):
    results = []
    plans = (
        db.query(Plan)
        .join(Dictionary, Plan.category_id == Dictionary.id)
        .options(joinedload(Plan.category))
        .filter(
            extract("month", Plan.period) == check_date.month,
            extract("year", Plan.period) == check_date.year,
        )
        .all()
    )

    for plan in plans:

        total_amount = None
        if plan.category.name == "видача":
            total_amount = sum(
                c.body
                for c in db.query(Credit)
                .filter(
                    extract("month", Credit.issuance_date) == check_date.month,
                    extract("year", Credit.issuance_date) == check_date.year,
                    extract("day", Credit.issuance_date) >= 1,
                )
                .all()
            )

        elif plan.category.name == "збір":
            total_amount = sum(
                p.sum
                for p in db.query(Payment)
                .filter(
                    extract("month", Payment.payment_date) == check_date.month,
                    extract("year", Payment.payment_date) == check_date.year,
                    extract("day", Payment.payment_date) >= 1,
                )
                .all()
            )

        performance = (total_amount / plan.sum) * 100 if plan.sum else 0

        results.append(
            {
                "month": plan.period.strftime("%Y-%m"),
                "category": plan.category.name,
                "plan_amount": plan.sum,
                "actual_amount": total_amount,
                "performance_percentage": round(performance, 2),
            }
        )

    return results
