import datetime

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import sqlite3
from PyQt5.uic import loadUiType
import matplotlib.pyplot as plt
import datetime

#################START############################3
hostal,_ = loadUiType('HostalManagementSystem.ui')
login,_ = loadUiType("LogIn.ui")


class LogIn(QWidget , login ):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.login_page)



    def login_page(self):
        self.mydb = sqlite3.connect("hostalmanagementsystem.db")
        self.cursor = self.mydb.cursor()
        u_name = self.lineEdit.text()
        u_password = self.lineEdit_2.text()
        print(u_name, u_password)

        sql_login = '''SELECT usr_name, user_password, user_email FROM user WHERE usr_name=? AND user_password=?'''

        self.cursor.execute(sql_login, (u_name, u_password))
        data = self.cursor.fetchone()
        if data:
            print('Correct Username and Password')
            self.win2 = mainwindow()
            self.close()
            self.win2.show()
        else:
            self.label.setText('Invalid Username or Password')



class mainwindow(QMainWindow, hostal ) :
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.the_ui_changes()
        self.all_working_btns()
        self.room_table()
        self.apart_table()
        self.aid_table()

        self.room_combo()
        self.apart_combo()
        self.aid_combo()
        
        self.show_all_staff()
        self.show_all_students()




    def the_ui_changes(self):

        self.tabWidget.tabBar().setVisible(False)


    def all_working_btns(self):

        self.pushButton.clicked.connect(self.operation_tab)
        self.pushButton_2.clicked.connect(self.student_tab)
        self.pushButton_3.clicked.connect(self.staff_tab)
        self.pushButton_32.clicked.connect(self.user_tab)
        self.pushButton_4.clicked.connect(self.setting_tab)
        self.pushButton_5.clicked.connect(self.bar_plot)

        self.pushButton_8.clicked.connect(self.add_student)
        self.pushButton_11.clicked.connect(self.search_student)
        self.pushButton_10.clicked.connect(self.update_student)
        self.pushButton_12.clicked.connect(self.delete_student)


        self.pushButton_15.clicked.connect(self.rooms)
        self.pushButton_16.clicked.connect(self.apart)
        self.pushButton_14.clicked.connect(self.aids)

        self.pushButton_7.clicked.connect(self.add_user)
        self.pushButton_9.clicked.connect(self.login)
        self.pushButton_13.clicked.connect(self.update_user)

        self.pushButton_22.clicked.connect(self.add_staff)
        self.pushButton_24.clicked.connect(self.search_staff)
        self.pushButton_23.clicked.connect(self.update_staff)
        self.pushButton_25.clicked.connect(self.delete_staff)


        self.pushButton_6.clicked.connect(self.operation_day)


##########################3ALL THE TABS ################################
    ##############################################3
###############################################333##3
    def operation_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def student_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def staff_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def user_tab(self):
        self.tabWidget.setCurrentIndex(3)

    def setting_tab(self):
        self.tabWidget.setCurrentIndex(4)

    def bar_plot(self):
        # Count the number of students and employees
        num_students, num_employees = count_students_and_employees()

        # Create the bar plot
        plt.bar(["Students", "Employees"], [num_students, num_employees])
        plt.xlabel("Type")
        plt.ylabel("Count")
        plt.title("Number of Students and Employees")

        # Display the plot in the bar_plot tab
        self.tabWidget.setCurrentIndex(5)
        plt.show()

    ##########################Day to Day Operation ################################
    def operation_day(self):
        stu = self.lineEdit.text()
        fee = self.comboBox.currentText()
        license = self.comboBox_2.currentIndex()+ 1
        date = datetime.date.today()
        end = date + datetime.timedelta(days=int(license))
        print(end)
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()
        op_query = 'INSERT INTO daytoday (stu_name , fees , lisc , date , to_date) VALUES(?,?,?,?,?)'
        self.cursor.execute(op_query, (stu, fee, license, date, end ))
        self.mydb.commit()
        self.statusBar().showMessage('New Activity Added')
        self.show_all_operation()

    def show_all_operation(self):
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()
        sho_all_oper = 'SELECT stu_name, fees, lisc, date, to_date FROM daytoday'
        self.cursor.execute(sho_all_oper)
        all_oper = self.cursor.fetchall()
        print(all_oper)
        self.tableWidget2.setRowCount(0)
        self.tableWidget2.insertRow(0)
        for row, form in enumerate(all_oper):
            for column, item in enumerate(form):
                self.tableWidget2.setItem(row, column, QTableWidgetItem(str(item)))
                column +=1
            rp = self.tableWidget2.rowCount()
            self.tableWidget2.insertRow(rp)


##########################Students ################################
    #######################STUDENTS###############3
###########################STUDENTS############333##3
    def show_all_students(self):
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()
        self.cursor.execute('''SELECT stu_code, stu_name, stu_dis,rooms ,apart ,aid ,ro_price FROM students''')
        data = self.cursor.fetchall()
        print(data)
        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_5.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_p = self.tableWidget_5.rowCount()
            self.tableWidget_5.insertRow(row_p)



    def add_student(self):
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()
        stuname = self.lineEdit_2.text()
        studis = self.textEdit.toPlainText()
        stuid = self.lineEdit_3.text()
        strooms = self.combobx.currentText()
        suapart = self.comboBox_4.currentText()
        stuaid = self.comboBox_5.currentText()
        sturoomsprice = self.lineEdit_4.text()
        add_student_query = 'INSERT INTO students(stu_name,stu_dis,stu_code,rooms,apart,aid,ro_price) VALUES(?,?,?,?,?,?,?)'
        self.cursor.execute(add_student_query,(stuname,studis,stuid,strooms,suapart,stuaid,sturoomsprice))
        self.mydb.commit()
        self.statusBar().showMessage('Student Added')
        self.lineEdit_2.setText('')
        self.textEdit.setPlainText('')
        self.lineEdit_3.setText('')
        self.combobx.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)
        self.lineEdit_4.setText('')
        self.show_all_students()

    def search_student(self):
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()
        search_name = self.lineEdit_7.text()
        sql  = '''SELECT * FROM students WHERE stu_name = ?'''
        self.cursor.execute(sql, [(search_name)])
        data = self.cursor.fetchone()
        print(data)

        self.lineEdit_21.setText(data[1])
        self.textEdit_2.setPlainText(data[2])
        self.lineEdit_5.setText(data[3])
        self.lineEdit_6.setText(str(data[7]))


    def update_student(self):
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()
        stuname = self.lineEdit_21.text()
        studis = self.textEdit_2.toPlainText()
        stuid = self.lineEdit_5.text()
        strooms = self.comboBox_7.currentIndex()
        suapart = self.comboBox_6.currentIndex()
        stuaid = self.comboBox_8.currentIndex()
        sturoomsprice = self.lineEdit_6.text()
        rstusearch = self.lineEdit_7.text()
        up_stu_data = '''UPDATE students SET stu_name =?, stu_dis=?, stu_code=?, rooms=?, apart=?,aid=?,ro_price=? WHERE stu_name=? '''
        self.cursor.execute(up_stu_data,(stuname,studis,stuid,strooms,suapart,stuaid,sturoomsprice,rstusearch))
        self.mydb.commit()
        self.statusBar().showMessage('Students Information Updated')
        self.show_all_students()


    def delete_student(self):
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()
        studeletename = self.lineEdit_7.text()
        sure_msg = QMessageBox.warning(self,'Delete a Student',"Are you Sure", QMessageBox.Yes | QMessageBox.No)
        if sure_msg == QMessageBox.Yes:
            delete_stu_data = '''DELETE FROM students WHERE stu_name=?'''
            self.cursor.execute(delete_stu_data,[(studeletename)])
            self.mydb.commit()
            self.statusBar().showMessage('Student Information Deleted')
            self.show_all_students()

    ########################Staff################################
    def show_all_staff(self):
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()

        self.cursor.execute('''SELECT emp_name, emp_email, emp_id FROM employee''')
        data = self.cursor.fetchall()
        print(data)
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_6.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_p = self.tableWidget_6.rowCount()
            self.tableWidget_6.insertRow(row_p)
        self.mydb.close()

    def add_staff(self):
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()
        st_name = self.lineEdit_26.text()
        st_email = self.lineEdit_28.text()
        st_id = self.lineEdit_25.text()

        employe_qury = 'INSERT INTO employee(emp_name,emp_email,emp_id) VALUES(?,?,?)'
        self.cursor.execute(employe_qury,(st_name,st_email,st_id))
        self.mydb.commit()

        self.statusBar().showMessage('New Staff Added')
        self.show_all_staff()

    def search_staff(self):
        Staff_id = self.lineEdit_27.text()

        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()

        search_stu_query = '''SELECT * FROM employee WHERE emp_id=?'''
        self.cursor.execute(search_stu_query, ([Staff_id]))
        stu_search_data = self.cursor.fetchall()
        print(stu_search_data)
        for row in stu_search_data:
            self.lineEdit_30.setText(row[1])
            self.lineEdit_31.setText(row[2])
            self.lineEdit_29.setText(row[3])

    def update_staff(self):
        staff_Origin_id = self.lineEdit_27.text()
        staff_name = self.lineEdit_30.text()
        staff_email = self.lineEdit_31.text()
        staff_id = self.lineEdit_29.text()
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()
        stf_update = 'UPDATE employee SET emp_name=?, emp_email=?, emp_id=? WHERE emp_id=?'
        self.cursor.execute(stf_update,(staff_name, staff_email, staff_id, staff_Origin_id))
        self.mydb.commit()
        self.mydb.close()
        self.statusBar().showMessage('Staff Information Updated')
        self.show_all_staff()
        self.show_all_staff()

    def delete_staff(self):
        delete_staff_name= self.lineEdit_27.text()
        msg = QMessageBox.warning(self, "Delete the staff", "Are you sure you want to delete the staff", QMessageBox.Yes | QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.mydb = sqlite3.connect('hostalmanagementsystem.db')
            self.cursor = self.mydb.cursor()
            delete_stf_data = 'DELETE FROM employee WHERE emp_id =?'
            self.cursor.execute(delete_stf_data, [(delete_staff_name)])
            self.mydb.commit()
            self.statusBar().showMessage('Staff information deleted')
            self.show_all_staff()
            self.show_all_staff()

########################Users################################
    #######################USERS###############3
###########################USERS############333##3
    def add_user(self):
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()

        username = self.lineEdit_8.text()
        email = self.lineEdit_9.text()
        password = self.lineEdit_10.text()
        password2 = self.lineEdit_11.text()

        if password == password2:
            user_pass_data = '''
                INSERT INTO user(usr_name, user_email, user_password)
                VALUES (?,?,?)'''
            self.cursor.execute(user_pass_data,(username,email,password))
            self.mydb.commit()
            self.statusBar().showMessage('New User Added')

        else:
            self.label_30.setText('please your password again')

    def login(self):
        self.mydb = sqlite3.connect("hostalmanagementsystem.db")
        self.cursor = self.mydb.cursor()

        u_name = self.lineEdit_13.text()
        u_password = self.lineEdit_12.text()
        print(u_name, u_password)

        sql_login = '''SELECT usr_name, user_password, user_email FROM user WHERE usr_name=? AND user_password=?'''

        self.cursor.execute(sql_login, (u_name, u_password))
        data = self.cursor.fetchone()
        if data:
            print('Correct Username and Password')
            self.statusBar().showMessage('Logged In')
            self.groupBox_3.setEnabled(True)
            self.lineEdit_17.setText(data[0])
            self.lineEdit_16.setText(data[2])


        else:
            print('Incorrect Entry')
            self.statusBar().showMessage('Incorrect username or password')



    def update_user(self):
        u_name = self.lineEdit_17.text()
        email = self.lineEdit_16.text()
        u_password = self.lineEdit_14.text()
        Conpassword = self.lineEdit_15.text()
        original_user = self.lineEdit_13.text()

        if u_password == Conpassword:
            self.mydb = sqlite3.connect("hostalmanagementsystem.db")
            self.cursor = self.mydb.cursor()

            self.cursor.execute('''
                UPDATE user SET usr_name = ? , user_email = ? , user_password = ? WHERE usr_name = ?
            ''', (u_name , email , u_password , original_user))

            self.mydb.commit()
            self.statusBar().showMessage('Data Updated')

        else:
            print('Incorrect Email or Password')


##########################SETTING################################
    #######################SETTING##############3
###########################SETTING###########333##3
    def rooms(self):
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()
        roomname = self.lineEdit_19.text()
        room_query = 'INSERT INTO room(room_name) VALUES(?)'
        self.cursor.execute(room_query,(roomname,))
        self.mydb.commit()
        self.statusBar().showMessage('Room Added')
        self.lineEdit_19.setText('')
        self.room_table()
        self.room_combo()
    def room_table(self):
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()
        self.cursor.execute( '''SELECT room_name FROM room''')
        room_data = self.cursor.fetchall()
        print(room_data)
        if room_data :
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row , form in enumerate(room_data):
                for column , item in enumerate(form):
                    self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                    column +=1
                rp = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(rp)
    def apart(self):
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()
        apartname = self.lineEdit_20.text()
        apart_query = 'INSERT INTO apart(apart_name) VALUES(?)'
        self.cursor.execute(apart_query, (apartname,))
        self.mydb.commit()
        self.statusBar().showMessage('Apartment Added')
        self.lineEdit_20.setText('')
        self.apart_table()
        self.apart_combo()

    def apart_table(self):
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()
        self.cursor.execute('''SELECT apart_name FROM apart''')
        apart_data = self.cursor.fetchall()
        print(apart_data)
        if apart_data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row, form in enumerate(apart_data):
                for column, item in enumerate(form):
                    self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                rp = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(rp)
    def aids(self):
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()
        aidname = self.lineEdit_18.text()
        aid_query = 'INSERT INTO aid(aid_type) VALUES(?)'
        self.cursor.execute(aid_query, (aidname,))
        self.mydb.commit()
        self.statusBar().showMessage('Students Aid Added')
        self.lineEdit_18.setText('')
        self.aid_table()
        self.aid_combo()
    def aid_table(self):
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()
        self.cursor.execute('''SELECT aid_type FROM aid''')
        aid_data = self.cursor.fetchall()
        print(aid_data)
        if aid_data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(aid_data):
                for column, item in enumerate(form):
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                rp = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(rp)
###############################COMBO BOXES#####################3
###############################COMBOXES#########################3
################################COMBOXES######################333
    def room_combo(self):
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()
        self.cursor.execute('''SELECT room_name FROM room''')
        room_combo_data = self.cursor.fetchall()
        self.combobx.clear()
        for room in room_combo_data:
            print(room[0])
            self.combobx.addItem(room[0])
            self.comboBox_7.addItem(room[0])
    def apart_combo(self):
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()
        self.cursor.execute('''SELECT apart_name FROM apart''')
        apart_combo_data = self.cursor.fetchall()
        self.comboBox_4.clear()

        for apart in apart_combo_data:
            print(apart[0])
            self.comboBox_4.addItem(apart[0])
            self.comboBox_6.addItem(apart[0])
    def aid_combo(self):
        self.mydb = sqlite3.connect('hostalmanagementsystem.db')
        self.cursor = self.mydb.cursor()
        self.cursor.execute('''SELECT aid_type FROM aid''')
        aid_combo_data = self.cursor.fetchall()
        self.comboBox_5.clear()
        for aid in aid_combo_data:
            print(aid[0])
            self.comboBox_5.addItem(aid[0])
            self.comboBox_8.addItem(aid[0])
    #########################STYLE#########################33
    ###################33#################################
    #####################STYLE#################33333333333



def count_students_and_employees():
        # Connect to the database
    db = sqlite3.connect("hostalmanagementsystem.db")
    cur = db.cursor()

        # Count the number of students
    cur.execute("SELECT COUNT(*) FROM students")
    num_students = cur.fetchone()[0]

        # Count the number of employees
    cur.execute("SELECT COUNT(*) FROM employee")
    num_employees = cur.fetchone()[0]

        # Close the connection to the database
    db.close()

        # Return the number of students and employees
    return num_students, num_employees


def main():
    myapp = QApplication(sys.argv)
    window = mainwindow()
    window.show()
    myapp.exec_()
if __name__ == '__main__':
    main()
