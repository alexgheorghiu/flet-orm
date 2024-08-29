import flet as ft
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connect to DB
engine = create_engine("sqlite:///db/dbperson.db")

# Mapping
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


class MyClass(ft.UserControl):
    def __init__(self):
        super(MyClass, self).__init__()
        self.selectId = ft.Text("", size=30)
        self.addBtn = ft.ElevatedButton("Add",
                                        on_click=self.addNewData,
                                        )
        self.editBtn = ft.ElevatedButton("Edit",
                                         bgcolor=ft.colors.ORANGE,
                                         on_click=self.saveEditData,
                                         )
        self.addBtn.visible = True
        self.editBtn.visible = False
        self.selectId.visible = False
        self.alldata = ft.Column()

    def addNewData(self, e):
        user = User(name=self.nameInput.value, age=self.ageInput.value)
        Session = sessionmaker(bind=engine)
        session = Session()

        # add new user
        session.add(user)
        session.commit()

        # refresh
        self.alldata.controls.clear()
        self.CallFromDatabase()
        self.page.update()

    def saveEditData(self, e):
        self.addBtn.visible = True
        Session = sessionmaker(bind=engine)
        session = Session()

        # grab proper entry from DB
        the_id = self.selectId.value
        user_to_update = session.query(User).filter(User.id == int(the_id)).first()

        # update proper entry in DB
        user_to_update.name = self.nameInput.value
        user_to_update.age = self.ageInput.value
        session.commit()

        # clear input
        self.nameInput.value = ""
        self.ageInput.value = ""
        self.editBtn.visible = False
        self.selectId.visible = False

        # refresh
        self.alldata.controls.clear()
        self.CallFromDatabase()
        self.page.update()

    def build(self) -> ft.Column:
        self.nameInput = ft.TextField(label="User name")
        self.ageInput = ft.TextField(label="Age")
        return ft.Column(
            [
                self.selectId,
                self.nameInput,
                self.ageInput,
                self.addBtn,
                self.editBtn,
                self.alldata,
            ]
        )

    def addNewData(self, e):
        new_user = User(name=self.nameInput.value, age=self.ageInput.value)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(new_user)

        # commit
        session.commit()

        # refresh data
        self.alldata.controls.clear()
        self.CallFromDatabase()
        self.page.update()

        # call render function

    def did_mount(self):
        self.CallFromDatabase()

    def CallFromDatabase(self):
        Session = sessionmaker(bind=engine)
        session = Session()

        # get all data from db
        users = session.query(User).all()
        for u in users:
            self.alldata.controls.append(
                ft.Container(
                    bgcolor=ft.colors.RED,
                    padding=10,
                    content=ft.Column([
                        ft.Text(f"name: {u.name}", color=ft.colors.WHITE, size=20),
                        ft.Text(f"age: {u.age}", color=ft.colors.WHITE, size=20),
                        ft.Row([
                            ft.ElevatedButton("Edit", data=u, on_click=lambda e: self.processEdit(e)),
                            ft.ElevatedButton("Delete", data=u, on_click=lambda e: self.processDelete(e))
                        ])
                    ])
                )
            )
        self.update()

    def processEdit(self, e):
        self.addBtn.visible = False
        self.selectId.visible = True

        self.selectId.value = e.control.data.id  # things that came through data
        the_id = self.selectId.value

        Session = sessionmaker(bind=engine)
        session = Session()

        self.nameInput.value = e.control.data.name
        self.ageInput.value = e.control.data.age
        self.editBtn.visible = True
        self.update()

    def processDelete(self, e):
        self.selectId.value = e.control.data.id  # things that came through data
        the_id = self.selectId.value

        Session = sessionmaker(bind=engine)
        session = Session()

        # delete user
        user_to_delete = session.query(User).filter(User.id == int(the_id)).first()
        session.delete(user_to_delete)
        session.commit()

        # refresh data
        self.alldata.controls.clear()

        self.CallFromDatabase()
        self.page.update()


def main(page: ft.Page):
    # page.update()
    myclass = MyClass()
    page.add(myclass)


ft.app(target=main)
