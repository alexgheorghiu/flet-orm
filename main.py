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
        self.editBtn = ft.ElevatedButton("Update",
                                         bgcolor=ft.colors.ORANGE,
                                         on_click=self.saveEditData,
                                         )
        self.cancelEditBtn = ft.TextButton("Cancel", on_click=self.cancelEditData, visible=False)
        self.addBtn.visible = True
        self.editBtn.visible = False
        self.selectId.visible = False
        self.alldata = ft.Column()

        # self.dlg_modal = ft.AlertDialog(
        #     modal=True,
        #     title=ft.Text("Please confirm"),
        #     content=ft.Text("Do you really want to delete all those files?"),
        #     actions=[
        #         ft.TextButton("Yes", on_click=self.handle_close),
        #         ft.TextButton("No", on_click=self.handle_close),
        #     ],
        #     actions_alignment=ft.MainAxisAlignment.END,
        #     # on_dismiss=lambda e: self.page.add(
        #     #     ft.Text("Modal dialog dismissed"),
        #     # ),
        #
        # )
        # self.confirmDelete = False


    def addNewData(self, e):
        user = User(name=self.nameInput.value, age=self.ageInput.value)
        Session = sessionmaker(bind=engine)
        session = Session()

        # add new user
        session.add(user)
        session.commit()

        # refresh
        self.alldata.controls.clear()
        self.populate_list_from_db()
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
        self.populate_list_from_db()
        self.page.update()

    def cancelEditData(self, e):
        self.nameInput.value = ""
        self.ageInput.value = ""
        self.selectId.visible = False
        self.editBtn.visible = False
        self.cancelEditBtn.visible = False
        self.addBtn.visible = True

        self.update()

    def build(self) -> ft.Column:
        self.nameInput = ft.TextField(label="User name")
        self.ageInput = ft.TextField(label="Age")
        return ft.Column(
            [
                self.selectId,
                self.nameInput,
                self.ageInput,
                self.addBtn,
                ft.Row([
                    self.editBtn,
                    self.cancelEditBtn
                ]),
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

        # clear data
        self.nameInput.value = ""
        self.ageInput.value = ""

        # refresh data
        self.alldata.controls.clear()
        self.populate_list_from_db()
        self.page.update()


    def did_mount(self):
        self.populate_list_from_db()

    def populate_list_from_db(self):
        """populates the list of users"""
        Session = sessionmaker(bind=engine)
        session = Session()

        # get all data from db
        users = session.query(User).all()
        for u in users:
            self.alldata.controls.append(
                ft.Container(
                    # bgcolor=ft.colors.RED,
                    padding=10,
                    content=ft.Column([
                        ft.Text(f"name: {u.name}", color=ft.colors.BLACK, size=20),
                        ft.Text(f"age: {u.age}", color=ft.colors.BLACK, size=20),
                        ft.Row([
                            ft.ElevatedButton("Edit", data=u, on_click=lambda e: self.processEdit(e)),
                            ft.ElevatedButton("Delete", data=u, on_click=lambda e: self.processDelete(e))
                        ])
                    ]),
                    border=ft.border.all(1, ft.colors.GREY),
                    border_radius=ft.border_radius.all(10)
                )
            )

        # update UI
        self.update()

    def processEdit(self, e):
        self.addBtn.visible = False
        self.selectId.visible = True

        self.selectId.value = e.control.data.id  # things that came through data
        the_id = self.selectId.value

        # Session = sessionmaker(bind=engine)
        # session = Session()

        self.nameInput.value = e.control.data.name
        self.ageInput.value = e.control.data.age
        self.editBtn.visible = True

        self.cancelEditBtn.visible = True

        self.update()

    def processDelete(self, e):
        # self.page.open(self.dlg_modal)
        # self.page.dialog = self.dlg_modal
        # self.page.show_dialog(dialog=self.dlg_modal)

        # print(f"Returned from dialog")
        # print(f"Confirm delete: {self.confirmDelete}")
        # if self.confirmDelete:

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

        self.populate_list_from_db()
        self.page.update()

    # def handle_close(self, e):
    #     # self.page.close(self.dlg_modal)
    #     self.page.close_dialog()
    #     self.confirmDelete = True if e.control.text == "Yes" else False
    #     self.page.add(ft.Text(f"Modal dialog closed with action: {e.control.text}"))


def main(page: ft.Page):
    page.title = "ORM Example"
    page.window_width = 600
    page.window_height = 800
    page.window_center()
    myclass = MyClass()
    page.add(myclass)


ft.app(target=main)
