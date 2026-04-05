from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Employee, ApplicationStatus, PriorityApplication
from utils import hash_password

Base.metadata.create_all(bind=engine)


def init():
    db: Session = SessionLocal()

    # Добавление администратора, если не существует
    if not db.query(Employee).filter(Employee.login == "admin").first():
        admin = Employee(
            full_name="Администратор Системы Тестовый",
            login="admin",
            hashed_password=hash_password("admin"),
            check_admin=True
        )
        db.add(admin)

    # Добавление статусов
    default_statuses = ["Новая", "В работе", "Завершена"]
    for i, name in enumerate(default_statuses, start=1):
        if not db.query(ApplicationStatus).filter(ApplicationStatus.id == i).first():
            db.add(ApplicationStatus(id=i, name=name))

    # Добавление приоритетов
    default_priorities = ["Низкий", "Средний", "Высокий"]
    for i, name in enumerate(default_priorities, start=1):
        if not db.query(PriorityApplication).filter(PriorityApplication.id == i).first():
            db.add(PriorityApplication(id=i, name=name))

    db.commit()
    db.close()


if __name__ == "__main__":
    init()
    print("База данных инициализирована.")
