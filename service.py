from sqlalchemy.orm import Session
from models import Employee, Application
from datetime import datetime
from utils import generate_login, hash_password
from docxtpl import DocxTemplate


def find_employee_by_name(db: Session, query: str):
    return db.query(Employee).filter(Employee.full_name.ilike(f"%{query}%")).all()


def find_employee_by_login(db: Session, login: str):
    return db.query(Employee).filter(Employee.login == login).first()


def add_employee(db: Session, full_name: str, raw_password: str, is_admin: bool = False):
    try:
        login = generate_login(full_name)
        hashed = hash_password(raw_password)
        count = len(db.query(Employee).filter(Employee.login.like(str(f"{login}%"))).all())
        if count > 0:
            login += str(count)
        employee = Employee(full_name=full_name, login=login, hashed_password=hashed, check_admin=is_admin)
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return {"message": "done"}
    except Exception as ex:
        return ex


def update_employee(db: Session, employee_id: int, full_name: str, password: str, admin: bool):
    try:
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        employee.full_name = full_name
        employee.login = generate_login(full_name)
        if password != '':
            employee.hashed_password = hash_password(password)
        employee.check_admin = admin
        db.commit()
        return "done"
    except Exception as ex:
        return ex


def archive_employee(db: Session, employee_id: int):
    try:
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            return None
        if employee.check_admin:
            return "is_admin"
        if employee.is_archived:
            employee.is_archived = False
            message = "done_unarchive"
        else:
            employee.is_archived = True
            message = "done_archive"
        db.commit()
        return message
    except Exception as ex:
        return ex


def get_applications(db: Session, user_id: int = None, sort_by: str = None, order: str = "asc"):
    query = db.query(Application)
    if user_id:
        query = query.filter(Application.id_employee == user_id)
    if sort_by:
        col = getattr(Application, sort_by)
        query = query.order_by(col.desc() if order == "desc" else col.asc())
    return query.all()


def update_application_status(db: Session, application_id: int, new_status: int):
    app = db.query(Application).filter(Application.id == application_id).first()
    if app:
        app.id_status = new_status
        if new_status == 3:
            app.date_completion = str(datetime.now().strftime("%d.%m.%y"))
        db.commit()
        return app
    return None


def generate_docx(full_name, name_priority, name_status, **application_data):
    template = DocxTemplate("template_docx/template_all_task.docx")
    context = {
        'full_name': full_name,
        'name_priority': name_priority,
        'name_status': name_status,
        'id_application': application_data['id_application'],
        'date_submission': application_data['date_submission'],
        'date_completion': application_data['date_completion'],
        'cabinet_number': application_data['cabinet_number'],
        'title': application_data['title'],
        'problem_description': application_data['problem_description']}

    output_path = f"user_file/generated_application_{application_data["title"]}.docx"
    template.render(context)
    template.save(output_path)

    return output_path
