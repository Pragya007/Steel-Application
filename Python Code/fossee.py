from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
import sys
from PyQt5.QtWidgets import*
import sqlite3 
#each function is three for angle channel beam
class Steel():
    def __init__(self):
        #buiding connection to sqlite database
        self.conn=sqlite3.connect("steel_sections.sqlite")
        self.c=self.conn.cursor()
        
        
    #inserting to database    
    def AddAngle(self,id,desg,mass,area,axb,t,r1,r2,cz,cy,tan,iz,iy,iu,iv,rz,ry,ru,rv,zz,zy,zpz,zpy,s):
          
          try:
            self.c.execute("INSERT INTO angles VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(id,desg,mass,area,axb,t,r1,r2,cz,cy,tan,iz,iy,iu,iv,rz,ry,ru,rv,zz,zy,zpz,zpy,s))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Successful','Angle is added successfully to the database.')
          except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not add angle to the database.')

    def AddChannel(self,id,desg,mass,area,d,b,tw,t,fs,r1,r2,cy,iz,iy,rz,ry,zz,zy,zpz,zpy,s):
        
        try:
            self.c.execute("INSERT INTO channels VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(id,desg,mass,area,d,b,tw,t,fs,r1,r2,cy,iz,iy,rz,ry,zz,zy,zpz,zpy,s))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Successful','Channel is added successfully to the database.')
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not add channel to the database.')


    def AddBeam(self,id,desg,mass,area,d,b,tw,t,fs,r1,r2,iz,iy,rz,ry,zz,zy,zpz,zpy,s):
        try:
            self.c.execute("INSERT INTO beams VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(id,desg,mass,area,d,b,tw,t,fs,r1,r2,iz,iy,rz,ry,zz,zy,zpz,zpy,s))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Successful','Beam is added successfully to the database.')
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not add beam to the database.')

    #searching designation in database
    def searchAngle(self,desg):
        q="SELECT * from angles where Designation='{}'"
        self.c.execute(q.format(str(desg)))
        self.data=self.c.fetchone()
        if not self.data:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not find any angle with this designation ')
            return None
        self.list=[]
        for i in range(0,24):
            self.list.append(self.data[i])
            
        self.c.close()
        self.conn.close()
        
        showangle(self.list)


    def searchChannel(self,desg):
        q="SELECT * from channels where Designation='{}'"
        self.c.execute(q.format(str(desg)))
        self.data=self.c.fetchone()
        if not self.data:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not find any channel with this designation ')
            return None
        self.list=[]
        for i in range(0,21):
            self.list.append(self.data[i])
            
        self.c.close()
        self.conn.close()
        showChannel(self.list)

    def searchBeam(self,desg):
        d=str(desg)
        q="SELECT * from beams where Designation='{}'"
        self.c.execute(q.format(d))
        self.data=self.c.fetchone()
        if not self.data:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not find any beam with this designation ')
            return None
        self.list=[]
        for i in range(0,20):
            self.list.append(self.data[i])
        self.c.close()
        self.conn.close()
        showBeam(self.list)


    #displaying current designation in database    
    def searchLoad(self):
        q="SELECT Designation from angles"
        self.c.execute(q)
        self.data=self.c.fetchall()
        self.list=[]
        for row_number, row_data in enumerate(self.data):
             for column_number, data in enumerate(row_data):
                self.list.append(data)
        self.c.close()
        self.conn.close()
        showload(self.list,row_number)    

                
    def searchcLoad(self):
        q="SELECT Designation from channels"
        self.c.execute(q)
        self.data=self.c.fetchall()
        self.list=[]
        for row_number, row_data in enumerate(self.data):
            for column_number, data in enumerate(row_data):
                self.list.append(data)
        self.c.close()
        self.conn.close()
        showcload(self.list,row_number)
    def searchbLoad(self):
        q="SELECT Designation from beams"
        self.c.execute(q)
        self.data=self.c.fetchall()
        
        self.list=[]
        for row_number, row_data in enumerate(self.data):
            
            
            for column_number, data in enumerate(row_data):
                self.list.append(data)
        
        
            
        self.c.close()
        self.conn.close()
        showbload(self.list,row_number)

#for login check    
class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.userNameLabel=QLabel("Username")
        self.userPassLabel=QLabel("Password")
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QGridLayout(self)
        layout.addWidget(self.userNameLabel, 1, 1)
        layout.addWidget(self.userPassLabel, 2, 1)
        layout.addWidget(self.textName,1,2)
        layout.addWidget(self.textPass,2,2)
        layout.addWidget(self.buttonLogin,3,1,1,2)
        self.setWindowTitle("Login")


    def handleLogin(self):
        if (self.textName.text() == '' and
            self.textPass.text() == ''):
            self.accept()
        else:
            QMessageBox.warning(
                self, 'Error', 'Incorrect username or password')

#to display the list of designations present in database            
def showload(list,n):
        table=QTableWidget()
        table.setRowCount(n+1)
        table.setColumnCount(1)
        for i in range(0,n+1):
            d=list[i]
            table.setItem(i, 0, QTableWidgetItem(str(d)))
        
        table.horizontalHeader().setStretchLastSection(True)
        dialog=QDialog()
        dialog.setWindowTitle("Angles Designation")
        dialog.resize(500,300)
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(table)
        dialog.exec()        


def showcload(list,n):
        table=QTableWidget()
        table.setRowCount(n+1)
        table.setColumnCount(1)
        for i in range(0,n+1):
            d=list[i]
            table.setItem(i, 0, QTableWidgetItem(str(d)))
        
        table.horizontalHeader().setStretchLastSection(True)
        
        dialog=QDialog()
        dialog.setWindowTitle("Channels Designation")
        dialog.resize(500,300)
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(table)
        dialog.exec()    

def showbload(list,n):
        table=QTableWidget()
        table.setRowCount(n+1)
        table.setColumnCount(1)
        for i in range(0,n+1):
            d=list[i]
            
            table.setItem(i, 0, QTableWidgetItem(str(d)))
        
        table.horizontalHeader().setStretchLastSection(True)
        
        dialog=QDialog()
        dialog.setWindowTitle("Beams Designation")
        dialog.resize(500,300)
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(table)
        dialog.exec()

#to show the further details of searched designation
def showangle(list):
        id=list[0]
        desg=list[1]
        mass=list[2]
        area=list[3]
        axb=list[4]
        t=list[5]
        r1=list[6]
        r2=list[7]
        cz=list[8]
        cy=list[9]
        tan=list[10]
        iz=list[11]
        iy=list[12]
        iu=list[13]
        iv=list[14]
        rz=list[15]
        ry=list[16]
        ru=list[17]
        rv=list[18]
        zz=list[19]
        zy=list[20]
        zpz=list[21]
        zpy=list[22]
        s=list[23]

        table=QTableWidget()
        tableItem=QTableWidgetItem()
        table.setWindowTitle("Angles Details")
        table.setRowCount(24)
        table.setColumnCount(2)

        table.setItem(0, 0, QTableWidgetItem("ID"))
        table.setItem(0, 1, QTableWidgetItem(str(id)))
        table.setItem(1, 0, QTableWidgetItem("Designation"))
        table.setItem(1, 1, QTableWidgetItem(str(desg)))
        table.setItem(2, 0, QTableWidgetItem("Mass"))
        table.setItem(2, 1, QTableWidgetItem(str(mass)))
        table.setItem(3, 0, QTableWidgetItem("Area"))
        table.setItem(3, 1, QTableWidgetItem(str(area)))
        table.setItem(4, 0, QTableWidgetItem("AXB"))
        table.setItem(4, 1, QTableWidgetItem(str(axb)))
        table.setItem(5, 0, QTableWidgetItem("t"))
        table.setItem(5, 1, QTableWidgetItem(str(t)))
        table.setItem(6, 0, QTableWidgetItem("R1"))
        table.setItem(6, 1, QTableWidgetItem(str(r1)))
        table.setItem(7, 0, QTableWidgetItem("R2"))
        table.setItem(7, 1, QTableWidgetItem(str(r2)))
        table.setItem(8, 0, QTableWidgetItem("Cz"))
        table.setItem(8, 1, QTableWidgetItem(str(cz)))
        table.setItem(9, 0, QTableWidgetItem("Cy"))
        table.setItem(9, 1, QTableWidgetItem(str(cy)))
        table.setItem(10, 0, QTableWidgetItem("Tan?"))
        table.setItem(10, 1, QTableWidgetItem(str(tan)))
        table.setItem(11, 0, QTableWidgetItem("Iz"))
        table.setItem(11, 1, QTableWidgetItem(str(iz)))
        table.setItem(12, 0, QTableWidgetItem("Iy"))
        table.setItem(12, 1, QTableWidgetItem(str(iy)))
        table.setItem(13, 0, QTableWidgetItem("Iu(max)"))
        table.setItem(13, 1, QTableWidgetItem(str(iu)))
        table.setItem(14, 0, QTableWidgetItem("Iv(min)"))
        table.setItem(14, 1, QTableWidgetItem(str(iv)))
        table.setItem(15, 0, QTableWidgetItem("rz"))
        table.setItem(15, 1, QTableWidgetItem(str(rz)))
        table.setItem(16, 0, QTableWidgetItem("ry"))
        table.setItem(16, 1, QTableWidgetItem(str(ry)))
        table.setItem(17, 0, QTableWidgetItem("ru(max)"))
        table.setItem(17, 1, QTableWidgetItem(str(ru)))
        table.setItem(18, 0, QTableWidgetItem("rv(min)"))
        table.setItem(18, 1, QTableWidgetItem(str(rv)))
        table.setItem(19, 0, QTableWidgetItem("Zz"))
        table.setItem(19, 1, QTableWidgetItem(str(zz)))
        table.setItem(20, 0, QTableWidgetItem("Zy"))
        table.setItem(20, 1, QTableWidgetItem(str(zy)))
        table.setItem(21, 0, QTableWidgetItem("Zpz"))
        table.setItem(21, 1, QTableWidgetItem(str(zpz)))
        table.setItem(22, 0, QTableWidgetItem("Zpy"))
        table.setItem(22, 1, QTableWidgetItem(str(zpy)))
        table.setItem(23, 0, QTableWidgetItem("Source"))
        table.setItem(23, 1, QTableWidgetItem(str(s)))
        table.horizontalHeader().setStretchLastSection(True)
        
        dialog=QDialog()
        dialog.setWindowTitle("Angle Details")
        dialog.resize(500,300)
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(table)
        dialog.exec()



def showChannel(list):
        

        id=list[0]
        desg=list[1]
        mass=list[2]
        area=list[3]
        d=list[4]
        b=list[5]
        tw=list[6]
        t=list[7]
        fs=list[8]
        r1=list[9]
        r2=list[10]
        cy=list[11]
        iz=list[12]
        iy=list[13]
        rz=list[14]
        ry=list[15]
        zz=list[16]
        zy=list[17]
        zpz=list[18]
        zpy=list[19]
        s=list[20]

        
        table=QTableWidget()
        tableItem=QTableWidgetItem()
        table.setWindowTitle("Channels Details")
        table.setRowCount(21)
        table.setColumnCount(2)

        table.setItem(0, 0, QTableWidgetItem("ID"))
        table.setItem(0, 1, QTableWidgetItem(str(id)))
        table.setItem(1, 0, QTableWidgetItem("Designation"))
        table.setItem(1, 1, QTableWidgetItem(str(desg)))
        table.setItem(2, 0, QTableWidgetItem("Mass"))
        table.setItem(2, 1, QTableWidgetItem(str(mass)))
        table.setItem(3, 0, QTableWidgetItem("Area"))
        table.setItem(3, 1, QTableWidgetItem(str(area)))
        table.setItem(4, 0, QTableWidgetItem("D"))
        table.setItem(4, 1, QTableWidgetItem(str(d)))
        table.setItem(5, 0, QTableWidgetItem("B"))
        table.setItem(5, 1, QTableWidgetItem(str(b)))
        table.setItem(6, 0, QTableWidgetItem("tw"))
        table.setItem(6, 1, QTableWidgetItem(str(tw)))
        table.setItem(7, 0, QTableWidgetItem("T"))
        table.setItem(7, 1, QTableWidgetItem(str(t)))
        table.setItem(8, 0, QTableWidgetItem("FlangeScope"))
        table.setItem(8, 1, QTableWidgetItem(str(fs)))
        table.setItem(9, 0, QTableWidgetItem("R1"))
        table.setItem(9, 1, QTableWidgetItem(str(r1)))
        table.setItem(10, 0, QTableWidgetItem("R2"))
        table.setItem(10, 1, QTableWidgetItem(str(r2)))
        table.setItem(11, 0, QTableWidgetItem("Cy"))
        table.setItem(11, 1, QTableWidgetItem(str(cy)))
        table.setItem(12, 0, QTableWidgetItem("Iz"))
        table.setItem(12, 1, QTableWidgetItem(str(iz)))
        table.setItem(13, 0, QTableWidgetItem("Iy"))
        table.setItem(13, 1, QTableWidgetItem(str(iy)))
        table.setItem(14, 0, QTableWidgetItem("rz"))
        table.setItem(14, 1, QTableWidgetItem(str(rz)))
        table.setItem(15, 0, QTableWidgetItem("ry"))
        table.setItem(15, 1, QTableWidgetItem(str(ry)))
        table.setItem(16, 0, QTableWidgetItem("Zz"))
        table.setItem(16, 1, QTableWidgetItem(str(zz)))
        table.setItem(17, 0, QTableWidgetItem("Zy"))
        table.setItem(17, 1, QTableWidgetItem(str(zy)))
        table.setItem(18, 0, QTableWidgetItem("Zpz"))
        table.setItem(18, 1, QTableWidgetItem(str(zpz)))
        table.setItem(19, 0, QTableWidgetItem("Zpy"))
        table.setItem(19, 1, QTableWidgetItem(str(zpy)))
        table.setItem(20, 0, QTableWidgetItem("Source"))
        table.setItem(20, 1, QTableWidgetItem(str(s)))
        table.horizontalHeader().setStretchLastSection(True)
        
        dialog=QDialog()
        dialog.setWindowTitle("Channel Details")
        dialog.resize(500,300)
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(table)
        dialog.exec()



def showBeam(list):
        
        
        id=list[0]
        desg=list[1]
        mass=list[2]
        area=list[3]
        d=list[4]
        b=list[5]
        tw=list[6]
        t=list[7]
        fs=list[8]
        r1=list[9]
        r2=list[10]
        iz=list[11]
        iy=list[12]
        rz=list[13]
        ry=list[14]
        zz=list[15]
        zy=list[16]
        zpz=list[17]
        zpy=list[18]
        s=list[19]

        
        table=QTableWidget()
        tableItem=QTableWidgetItem()
        table.setWindowTitle("Beams Details")
        table.setRowCount(20)
        table.setColumnCount(2)

        table.setItem(0, 0, QTableWidgetItem("ID"))
        table.setItem(0, 1, QTableWidgetItem(str(id)))
        table.setItem(1, 0, QTableWidgetItem("Designation"))
        table.setItem(1, 1, QTableWidgetItem(str(desg)))
        table.setItem(2, 0, QTableWidgetItem("Mass"))
        table.setItem(2, 1, QTableWidgetItem(str(mass)))
        table.setItem(3, 0, QTableWidgetItem("Area"))
        table.setItem(3, 1, QTableWidgetItem(str(area)))
        table.setItem(4, 0, QTableWidgetItem("D"))
        table.setItem(4, 1, QTableWidgetItem(str(d)))
        table.setItem(5, 0, QTableWidgetItem("B"))
        table.setItem(5, 1, QTableWidgetItem(str(b)))
        table.setItem(6, 0, QTableWidgetItem("tw"))
        table.setItem(6, 1, QTableWidgetItem(str(tw)))
        table.setItem(7, 0, QTableWidgetItem("T"))
        table.setItem(7, 1, QTableWidgetItem(str(t)))
        table.setItem(8, 0, QTableWidgetItem("FlangeScope"))
        table.setItem(8, 1, QTableWidgetItem(str(fs)))
        table.setItem(9, 0, QTableWidgetItem("R1"))
        table.setItem(9, 1, QTableWidgetItem(str(r1)))
        table.setItem(10, 0, QTableWidgetItem("R2"))
        table.setItem(10, 1, QTableWidgetItem(str(r2)))
        table.setItem(11, 0, QTableWidgetItem("Iz"))
        table.setItem(11, 1, QTableWidgetItem(str(iz)))
        table.setItem(12, 0, QTableWidgetItem("Iy"))
        table.setItem(12, 1, QTableWidgetItem(str(iy)))
        table.setItem(13, 0, QTableWidgetItem("rz"))
        table.setItem(13, 1, QTableWidgetItem(str(rz)))
        table.setItem(14, 0, QTableWidgetItem("ry"))
        table.setItem(14, 1, QTableWidgetItem(str(ry)))
        table.setItem(15, 0, QTableWidgetItem("Zz"))
        table.setItem(15, 1, QTableWidgetItem(str(zz)))
        table.setItem(16, 0, QTableWidgetItem("Zy"))
        table.setItem(16, 1, QTableWidgetItem(str(zy)))
        table.setItem(17, 0, QTableWidgetItem("Zpz"))
        table.setItem(17, 1, QTableWidgetItem(str(zpz)))
        table.setItem(18, 0, QTableWidgetItem("Zpy"))
        table.setItem(18, 1, QTableWidgetItem(str(zpy)))
        table.setItem(19, 0, QTableWidgetItem("Source"))
        table.setItem(19, 1, QTableWidgetItem(str(s)))
        table.horizontalHeader().setStretchLastSection(True)
        
        dialog=QDialog()
        dialog.setWindowTitle("Beam Details")
        dialog.resize(500,300)
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(table)
        dialog.exec()        

            
#to display the form to add/append 
class AddAngle(QDialog):
    def __init__(self):
        super().__init__()
        
        self.btnCancel=QPushButton("Cancel",self)
        self.btnReset=QPushButton("Reset",self)
        self.btnAdd=QPushButton("Add",self)

        self.btnCancel.setFixedHeight(30)
        self.btnReset.setFixedHeight(30)
        self.btnAdd.setFixedHeight(30)

        self.idLabel=QLabel("Id")
        self.desgLabel=QLabel("Designation")
        self.massLabel = QLabel("mass")
        self.areaLabel = QLabel("Area")
        self.axbLabel = QLabel("AXB")
        self.tLabel = QLabel("T")
        self.r1Label = QLabel("R1")
        self.r2Label = QLabel("R2")
        self.czLabel = QLabel("Cz")
        self.cyLabel = QLabel("Cy")
        self.tanLabel=QLabel("Tan?")
        self.izLabel = QLabel("Iz")
        self.iyLabel = QLabel("Iy")
        self.iuLabel = QLabel("Iu")
        self.ivLabel = QLabel("Iv")
        self.rzLabel = QLabel("rz")
        self.ryLabel = QLabel("ry")
        self.ruLabel = QLabel("ru")
        self.rvLabel = QLabel("rv")
        self.zzLabel = QLabel("Zz")
        self.zyLabel = QLabel("Zy")
        self.zpzLabel = QLabel("Zpz")
        self.zpyLabel = QLabel("Zpy")
        self.sLabel = QLabel("Source")
        

        self.idText=QLineEdit(self)
        self.desgText=QLineEdit(self)
        self.massText=QLineEdit(self)
        self.areaText=QLineEdit(self)
        self.axbText=QLineEdit(self)
        self.tText=QLineEdit(self)
        self.r1Text=QLineEdit(self)
        self.r2Text=QLineEdit(self)
        self.czText=QLineEdit(self)
        self.cyText=QLineEdit(self)
        self.tanText=QLineEdit(self)
        self.izText=QLineEdit(self)
        self.iyText=QLineEdit(self)
        self.iuText=QLineEdit(self)
        self.ivText=QLineEdit(self)
        self.rzText=QLineEdit(self)
        self.ryText=QLineEdit(self)
        self.ruText=QLineEdit(self)
        self.rvText=QLineEdit(self)
        self.zzText=QLineEdit(self)
        self.zyText=QLineEdit(self)
        self.zpzText=QLineEdit(self)
        self.zpyText=QLineEdit(self)
        self.sText=QLineEdit(self)
        

        self.grid=QGridLayout(self)
        self.grid.addWidget(self.idLabel,1,1)
        self.grid.addWidget(self.desgLabel,2,1)
        self.grid.addWidget(self.massLabel,3,1)
        self.grid.addWidget(self.areaLabel,4,1)
        self.grid.addWidget(self.axbLabel,5,1)
        self.grid.addWidget(self.tLabel,6,1)
        self.grid.addWidget(self.r1Label,7,1)
        self.grid.addWidget(self.r2Label,8,1)
        self.grid.addWidget(self.czLabel,9,1)
        self.grid.addWidget(self.cyLabel,10,1)
        self.grid.addWidget(self.tanLabel,11,1)
        self.grid.addWidget(self.izLabel,12,1)
        self.grid.addWidget(self.iyLabel,13,1)
        self.grid.addWidget(self.iuLabel,14,1)
        self.grid.addWidget(self.ivLabel,15,1)
        self.grid.addWidget(self.rzLabel,16,1)
        self.grid.addWidget(self.ryLabel,17,1)
        self.grid.addWidget(self.ruLabel,18,1)
        self.grid.addWidget(self.rvLabel,19,1)
        self.grid.addWidget(self.zzLabel,20,1)
        self.grid.addWidget(self.zyLabel,21,1)
        self.grid.addWidget(self.zpzLabel,22,1)
        self.grid.addWidget(self.zpyLabel,23,1)
        self.grid.addWidget(self.sLabel,24,1)
        

        self.grid.addWidget(self.idText,1,2)
        self.grid.addWidget(self.desgText,2,2)
        self.grid.addWidget(self.massText,3,2)
        self.grid.addWidget(self.areaText,4,2)
        self.grid.addWidget(self.axbText,5,2)
        self.grid.addWidget(self.tText,6,2)
        self.grid.addWidget(self.r1Text,7,2)
        self.grid.addWidget(self.r2Text,8,2)
        self.grid.addWidget(self.czText,9,2)
        self.grid.addWidget(self.cyText,10,2)
        self.grid.addWidget(self.tanText,11,2)
        self.grid.addWidget(self.izText,12,2)
        self.grid.addWidget(self.iyText,13,2)
        self.grid.addWidget(self.iuText,14,2)
        self.grid.addWidget(self.ivText,15,2)
        self.grid.addWidget(self.rzText,16,2)
        self.grid.addWidget(self.ryText,17,2)
        self.grid.addWidget(self.ruText,18,2)
        self.grid.addWidget(self.rvText,19,2)
        self.grid.addWidget(self.zzText,20,2)
        self.grid.addWidget(self.zyText,21,2)
        self.grid.addWidget(self.zpzText,22,2)
        self.grid.addWidget(self.zpyText,23,2)
        self.grid.addWidget(self.sText,24,2)

        
        self.grid.addWidget(self.btnReset,25,1)
        self.grid.addWidget(self.btnCancel,25,3)
        self.grid.addWidget(self.btnAdd,25,2)
        
        self.btnAdd.clicked.connect(self.addAngle)
        self.btnCancel.clicked.connect(QApplication.instance().quit)
        self.btnReset.clicked.connect(self.reset)

        self.setLayout(self.grid)
        self.setWindowTitle("Add Angle Details")
        self.resize(500,600)
        self.show()
        self.exec() 

    def reset(self):
        self.idText.setText("")
        self.desgText.setText("")
        self.massText.setText("")
        self.areaText.setText("")
        self.axbText.setText("")
        self.tText.setText("")
        self.r1Text.setText("")
        self.r2Text.setText("")
        self.czText.setText("")
        self.cyText.setText("")
        self.tanText.setText("")
        self.izText.setText("")
        self.iyText.setText("")
        self.iuText.setText("")
        self.ivText.setText("")
        self.rzText.setText("")
        self.ryText.setText("")
        self.ruText.setText("")
        self.rvText.setText("")
        self.zzText.setText("")
        self.zyText.setText("")
        self.zpzText.setText("")
        self.zpyText.setText("")
        self.sText.setText("")

    def addAngle(self):
     
        #to store in variable  
        self.id=int(self.idText.text())
        self.desg=self.desgText.text()
        self.mass=self.massText.text()
        self.area=self.areaText.text()
        self.axb=self.axbText.text()
        self.t=self.tText.text()
        self.r1=self.r1Text.text()
        self.r2=self.r2Text.text()
        self.cz=self.czText.text()
        self.cy=self.cyText.text()
        self.tan=self.tanText.text()
        self.iz=self.izText.text()
        self.iy=self.iyText.text()
        self.iu=self.iuText.text()
        self.iv=self.ivText.text()
        self.rz=self.rzText.text()
        self.ry=self.ryText.text()
        self.ru=self.ruText.text()
        self.rv=self.rvText.text()
        self.zz=self.zzText.text()
        self.zy=self.zyText.text()
        self.zpz=self.zpzText.text()
        self.zpy=self.zpyText.text()
        self.s=self.sText.text()
        

        #now passing the variable to function which will insert in database finally
        self.steel=Steel()
        self.steel.AddAngle(self.id,self.desg,self.mass,self.area,self.axb,self.t,self.r1,self.r2,self.cz,self.cy,self.tan,self.iz,self.iy,self.iu,self.iv,self.rz,self.ry,self.ru,self.rv,self.zz,self.zy,self.zpz,self.zpy,self.s)


class AddChannel(QDialog):
    def __init__(self):
        super().__init__()
        
        
        self.btnCancel=QPushButton("Cancel",self)
        self.btnReset=QPushButton("Reset",self)
        self.btnAdd=QPushButton("Add",self)

        self.btnCancel.setFixedHeight(30)
        self.btnReset.setFixedHeight(30)
        self.btnAdd.setFixedHeight(30)

        self.idLabel=QLabel("Id")
        self.desgLabel=QLabel("Designation")
        self.massLabel = QLabel("Mass")
        self.areaLabel = QLabel("Area")
        self.dLabel = QLabel("D")
        self.bLabel = QLabel("B")
        self.twLabel = QLabel("tw")
        self.tLabel = QLabel("T")
        self.fsLabel = QLabel("FlangeSlope")
        self.r1Label = QLabel("R1")
        self.r2Label = QLabel("R2")
        self.cyLabel = QLabel("Cy")
        self.izLabel = QLabel("Iz")
        self.iyLabel = QLabel("Iy")
        self.rzLabel = QLabel("rz")
        self.ryLabel = QLabel("ry")
        self.zzLabel = QLabel("Zz")
        self.zyLabel = QLabel("Zy")
        self.zpzLabel = QLabel("Zpz")
        self.zpyLabel = QLabel("Zpy")
        self.sLabel = QLabel("Source")
        

        self.idText=QLineEdit(self)
        self.desgText=QLineEdit(self)
        self.massText=QLineEdit(self)
        self.areaText=QLineEdit(self)
        self.dText=QLineEdit(self)
        self.bText=QLineEdit(self)
        self.twText=QLineEdit(self)
        self.tText=QLineEdit(self)
        self.fsText=QLineEdit(self)
        self.r1Text=QLineEdit(self)
        self.r2Text=QLineEdit(self)
        self.cyText=QLineEdit(self)
        self.izText=QLineEdit(self)
        self.iyText=QLineEdit(self)
        self.rzText=QLineEdit(self)
        self.ryText=QLineEdit(self)
        self.zzText=QLineEdit(self)
        self.zyText=QLineEdit(self)
        self.zpzText=QLineEdit(self)
        self.zpyText=QLineEdit(self)
        self.sText=QLineEdit(self)
        

        self.grid=QGridLayout(self)
        self.grid.addWidget(self.idLabel,1,1)
        self.grid.addWidget(self.desgLabel,2,1)
        self.grid.addWidget(self.massLabel,3,1)
        self.grid.addWidget(self.areaLabel,4,1)
        self.grid.addWidget(self.dLabel,5,1)
        self.grid.addWidget(self.bLabel,6,1)
        self.grid.addWidget(self.twLabel,7,1)
        self.grid.addWidget(self.tLabel,8,1)
        self.grid.addWidget(self.fsLabel,9,1)
        self.grid.addWidget(self.r1Label,10,1)
        self.grid.addWidget(self.r2Label,11,1)
        self.grid.addWidget(self.cyLabel,12,1)
        self.grid.addWidget(self.izLabel,13,1)
        self.grid.addWidget(self.iyLabel,14,1)
        self.grid.addWidget(self.rzLabel,15,1)
        self.grid.addWidget(self.ryLabel,16,1)
        self.grid.addWidget(self.zzLabel,17,1)
        self.grid.addWidget(self.zyLabel,18,1)
        self.grid.addWidget(self.zpzLabel,19,1)
        self.grid.addWidget(self.zpyLabel,20,1)
        self.grid.addWidget(self.sLabel,21,1)
        

        self.grid.addWidget(self.idText,1,2)
        self.grid.addWidget(self.desgText,2,2)
        self.grid.addWidget(self.massText,3,2)
        self.grid.addWidget(self.areaText,4,2)
        self.grid.addWidget(self.dText,5,2)
        self.grid.addWidget(self.bText,6,2)
        self.grid.addWidget(self.twText,7,2)
        self.grid.addWidget(self.tText,8,2)
        self.grid.addWidget(self.fsText,9,2)
        self.grid.addWidget(self.r1Text,10,2)
        self.grid.addWidget(self.r2Text,11,2)
        self.grid.addWidget(self.cyText,12,2)
        self.grid.addWidget(self.izText,13,2)
        self.grid.addWidget(self.iyText,14,2)
        self.grid.addWidget(self.rzText,15,2)
        self.grid.addWidget(self.ryText,16,2)
        self.grid.addWidget(self.zzText,17,2)
        self.grid.addWidget(self.zyText,18,2)
        self.grid.addWidget(self.zpzText,19,2)
        self.grid.addWidget(self.zpyText,20,2)
        self.grid.addWidget(self.sText,21,2)

        
        self.grid.addWidget(self.btnReset,22,1)
        self.grid.addWidget(self.btnCancel,22,3)
        self.grid.addWidget(self.btnAdd,22,2)
        
        self.btnAdd.clicked.connect(self.addChannel)
        self.btnCancel.clicked.connect(QApplication.instance().quit)
        self.btnReset.clicked.connect(self.reset)

        self.setLayout(self.grid)
        self.setWindowTitle("Add Channel Details")
        self.resize(500,600)
        self.show()
        self.exec()

    def reset(self):
        self.idText.setText("")
        self.desgText.setText("")
        self.massText.setText("")
        self.areaText.setText("")
        self.dText.setText("")
        self.bText.setText("")
        self.twText.setText("")
        self.tText.setText("")
        self.fsText.setText("")
        self.r1Text.setText("")
        self.r2Text.setText("")
        self.cyText.setText("")
        self.izText.setText("")
        self.iyText.setText("")
        self.rzText.setText("")
        self.ryText.setText("")
        self.zzText.setText("")
        self.zyText.setText("")
        self.zpzText.setText("")
        self.zpyText.setText("")
        self.sText.setText("")

    def addChannel(self):
        
        self.id=int(self.idText.text())
        self.desg=self.desgText.text()
        self.mass=self.massText.text()
        self.area=self.areaText.text()
        self.d=int(self.dText.text())
        self.b=int(self.bText.text())
        self.tw=self.twText.text()
        self.t=self.tText.text()
        self.fs=int(self.fsText.text())
        self.r1=self.r1Text.text()
        self.r2=self.r2Text.text()
        self.cy=self.cyText.text()
        self.iz=self.izText.text()
        self.iy=self.iyText.text()
        self.rz=self.rzText.text()
        self.ry=self.ryText.text()
        self.zz=self.zzText.text()
        self.zy=self.zyText.text()
        self.zpz=self.zpzText.text()
        self.zpy=self.zpyText.text()
        self.s=self.sText.text()
        
        
        self.steel=Steel()
        self.steel.AddChannel(self.id,self.desg,self.mass,self.area,self.d,self.b,self.tw,self.t,self.fs,self.r1,self.r2,self.cy,self.iz,self.iy,self.rz,self.ry,self.zz,self.zy,self.zpz,self.zpy,self.s)



class AddBeam(QDialog):
    def __init__(self):
        super().__init__()

        
        self.btnCancel=QPushButton("Cancel",self)
        self.btnReset=QPushButton("Reset",self)
        self.btnAdd=QPushButton("Add",self)

        self.btnCancel.setFixedHeight(30)
        self.btnReset.setFixedHeight(30)
        self.btnAdd.setFixedHeight(30)

        self.idLabel=QLabel("Id")
        self.desgLabel=QLabel("Designation")
        self.massLabel = QLabel("Mass")
        self.areaLabel = QLabel("Area")
        self.dLabel = QLabel("D")
        self.bLabel = QLabel("B")
        self.twLabel = QLabel("tw")
        self.tLabel = QLabel("T")
        self.fsLabel = QLabel("FlangeSlope")
        self.r1Label = QLabel("R1")
        self.r2Label = QLabel("R2")
        self.izLabel = QLabel("Iz")
        self.iyLabel = QLabel("Iy")
        self.rzLabel = QLabel("rz")
        self.ryLabel = QLabel("ry")
        self.zzLabel = QLabel("Zz")
        self.zyLabel = QLabel("Zy")
        self.zpzLabel = QLabel("Zpz")
        self.zpyLabel = QLabel("Zpy")
        self.sLabel = QLabel("Source")
        

        self.idText=QLineEdit(self)
        self.desgText=QLineEdit(self)
        self.massText=QLineEdit(self)
        self.areaText=QLineEdit(self)
        self.dText=QLineEdit(self)
        self.bText=QLineEdit(self)
        self.twText=QLineEdit(self)
        self.tText=QLineEdit(self)
        self.fsText=QLineEdit(self)
        self.r1Text=QLineEdit(self)
        self.r2Text=QLineEdit(self)
        self.izText=QLineEdit(self)
        self.iyText=QLineEdit(self)
        self.rzText=QLineEdit(self)
        self.ryText=QLineEdit(self)
        self.zzText=QLineEdit(self)
        self.zyText=QLineEdit(self)
        self.zpzText=QLineEdit(self)
        self.zpyText=QLineEdit(self)
        self.sText=QLineEdit(self)
        self.grid=QGridLayout(self)


        self.grid.addWidget(self.idLabel,1,1)
        self.grid.addWidget(self.desgLabel,2,1)
        self.grid.addWidget(self.massLabel,3,1)
        self.grid.addWidget(self.areaLabel,4,1)
        self.grid.addWidget(self.dLabel,5,1)
        self.grid.addWidget(self.bLabel,6,1)
        self.grid.addWidget(self.twLabel,7,1)
        self.grid.addWidget(self.tLabel,8,1)
        self.grid.addWidget(self.fsLabel,9,1)
        self.grid.addWidget(self.r1Label,10,1)
        self.grid.addWidget(self.r2Label,11,1)
        self.grid.addWidget(self.izLabel,12,1)
        self.grid.addWidget(self.iyLabel,13,1)
        self.grid.addWidget(self.rzLabel,14,1)
        self.grid.addWidget(self.ryLabel,15,1)
        self.grid.addWidget(self.zzLabel,16,1)
        self.grid.addWidget(self.zyLabel,17,1)
        self.grid.addWidget(self.zpzLabel,18,1)
        self.grid.addWidget(self.zpyLabel,19,1)
        self.grid.addWidget(self.sLabel,20,1)


        self.grid.addWidget(self.idText,1,2)
        self.grid.addWidget(self.desgText,2,2)
        self.grid.addWidget(self.massText,3,2)
        self.grid.addWidget(self.areaText,4,2)
        self.grid.addWidget(self.dText,5,2)
        self.grid.addWidget(self.bText,6,2)
        self.grid.addWidget(self.twText,7,2)
        self.grid.addWidget(self.tText,8,2)
        self.grid.addWidget(self.fsText,9,2)
        self.grid.addWidget(self.r1Text,10,2)
        self.grid.addWidget(self.r2Text,11,2)
        self.grid.addWidget(self.izText,12,2)
        self.grid.addWidget(self.iyText,13,2)
        self.grid.addWidget(self.rzText,14,2)
        self.grid.addWidget(self.ryText,15,2)
        self.grid.addWidget(self.zzText,16,2)
        self.grid.addWidget(self.zyText,17,2)
        self.grid.addWidget(self.zpzText,18,2)
        self.grid.addWidget(self.zpyText,19,2)
        self.grid.addWidget(self.sText,20,2)

       
        self.grid.addWidget(self.btnReset,21,1)
        self.grid.addWidget(self.btnCancel,21,3)
        self.grid.addWidget(self.btnAdd,21,2)
        
        self.btnAdd.clicked.connect(self.addBeam)
        self.btnCancel.clicked.connect(QApplication.instance().quit)
        self.btnReset.clicked.connect(self.reset)

        self.setLayout(self.grid)
        self.setWindowTitle("Add Beam Details")
        self.resize(500,600)
        self.show()
        self.exec()

    def reset(self):
        self.idText.setText("")
        self.desgText.setText("")
        self.massText.setText("")
        self.areaText.setText("")
        self.dText.setText("")
        self.bText.setText("")
        self.twText.setText("")
        self.tText.setText("")
        self.fsText.setText("")
        self.r1Text.setText("")
        self.r2Text.setText("")
        self.izText.setText("")
        self.iyText.setText("")
        self.rzText.setText("")
        self.ryText.setText("")
        self.zzText.setText("")
        self.zyText.setText("")
        self.zpzText.setText("")
        self.zpyText.setText("")
        self.sText.setText("")

    def addBeam(self):
        
        self.id=int(self.idText.text())
        self.desg=self.desgText.text()
        self.mass=self.massText.text()
        self.area=self.areaText.text()
        self.d=self.dText.text()
        self.b=self.bText.text()
        self.tw=self.twText.text()
        self.t=self.tText.text()
        self.fs=int(self.fsText.text())
        self.r1=self.r1Text.text()
        self.r2=self.r2Text.text()
        self.iz=self.izText.text()
        self.iy=self.iyText.text()
        self.rz=self.rzText.text()
        self.ry=self.ryText.text()
        self.zz=self.zzText.text()
        self.zy=self.zyText.text()
        self.zpz=self.zpzText.text()
        self.zpy=self.zpyText.text()
        self.s=self.sText.text()
        
        
        self.steel=Steel()
        self.steel.AddBeam(self.id,self.desg,self.mass,self.area,self.d,self.b,self.tw,self.t,self.fs,self.r1,self.r2,self.iz,self.iy,self.rz,self.ry,self.zz,self.zy,self.zpz,self.zpy,self.s)



class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
           
        #dialog generation to enter the designation for search
        self.rollToBeSearched=""
        self.vbox = QVBoxLayout()
        self.text = QLabel("Enter the Designation")
        self.editField = QLineEdit()
        self.btnSearch = QPushButton("Show", self)
        self.btnSearch.clicked.connect(self.showAngle)
        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.editField)
        self.vbox.addWidget(self.btnSearch)
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Show Angle Detail")
        self.dialog.setLayout(self.vbox)

        self.rollForChannel = ""
        self.vboxChannel = QVBoxLayout()
        self.textChannel = QLabel("Enter the Designation")
        self.editFieldChannel = QLineEdit()
        self.btnSearchChannel = QPushButton("Show", self)
        self.btnSearchChannel.clicked.connect(self.showAngleChannel)
        self.vboxChannel.addWidget(self.textChannel)
        self.vboxChannel.addWidget(self.editFieldChannel)
        self.vboxChannel.addWidget(self.btnSearchChannel)
        self.dialogChannel = QDialog()
        self.dialogChannel.setWindowTitle("Show Channel Detail")
        self.dialogChannel.setLayout(self.vboxChannel)

        self.rollForBeam = ""
        self.vboxBeam = QVBoxLayout()
        self.textBeam = QLabel("Enter the Designation")
        self.editFieldBeam = QLineEdit()
        self.btnSearchBeam = QPushButton("Show", self)
        self.btnSearchBeam.clicked.connect(self.showAngleBeam)
        self.vboxBeam.addWidget(self.textBeam)
        self.vboxBeam.addWidget(self.editFieldBeam)
        self.vboxBeam.addWidget(self.btnSearchBeam)
        self.dialogBeam = QDialog()
        self.dialogBeam.setWindowTitle("Show Beam Detail")
        self.dialogBeam.setLayout(self.vboxBeam)

        #whole gui layout
        self.btnEnterangle=QPushButton("Add/Append Angle ",self)
        self.btnEnterChannel=QPushButton("Add/Append Channel",self)
        self.btnShowangleDetails=QPushButton("Show Angle Details",self)
        self.btnShowChannelDetails=QPushButton("Show Channel Details",self)
        self.btnEnterBeam=QPushButton("Add/Append Beam",self)
        self.btnShowBeamDetails=QPushButton("Show Beam Details",self)
        self.btnload=QPushButton("Angles",self)
        self.btncload=QPushButton("Channels",self)
        self.btnbload=QPushButton("Beams",self)
        
        
        #pictures added
        self.picLabel=QLabel(self)
        self.picLabel.resize(100,100)
        self.picLabel.move(50,10)
        self.picLabel.setScaledContents(True)
        self.picLabel.setPixmap(QtGui.QPixmap("angle.png"))
        self.picLabel=QLabel(self)
        self.picLabel.resize(100,100)
        self.picLabel.move(250,10)
        self.picLabel.setScaledContents(True)
        self.picLabel.setPixmap(QtGui.QPixmap("channel.png"))
        self.picLabel=QLabel(self)
        self.picLabel.resize(100,100)
        self.picLabel.move(450,10)
        self.picLabel.setScaledContents(True)
        self.picLabel.setPixmap(QtGui.QPixmap("beam.png"))

        #each button take us to functions down
        self.btnload.move(15,120)
        self.btnload.resize(180,40)
        self.btnloadFont=self.btnload.font()
        self.btnloadFont.setPointSize(13)
        self.btnload.setFont(QtGui.QFont("Monospace"))
        self.btnload.clicked.connect(self.showload)   #here showload() is the function
        self.btnload.setStyleSheet("font-size:15px;")

        self.btncload.move(205,120)
        self.btncload.resize(180,40)
        self.btncloadFont=self.btncload.font()
        self.btncloadFont.setPointSize(13)
        self.btncload.setFont(QtGui.QFont("Monospace"))
        self.btncload.clicked.connect(self.showcload)
        self.btncload.setStyleSheet("font-size:15px;")

        self.btnbload.move(398,120)
        self.btnbload.resize(180,40)
        self.btnbloadFont=self.btnbload.font()
        self.btnbloadFont.setPointSize(13)
        self.btnbload.setFont(QtGui.QFont("Monospace"))
        self.btnbload.clicked.connect(self.showbload)
        self.btnbload.setStyleSheet("font-size:15px;")
        
        self.btnEnterangle.move(15,170)
        self.btnEnterangle.resize(180,40)
        self.btnEnterangleFont=self.btnEnterangle.font()
        self.btnEnterangleFont.setPointSize(13)
        self.btnEnterangle.setFont(QtGui.QFont("Monospace"))
        self.btnEnterangle.clicked.connect(self.enterangle)  #take to function below name enterangle()
        self.btnEnterangle.setStyleSheet("font-size:15px;")

        self.btnEnterChannel.move(205,170)
        self.btnEnterChannel.resize(180, 40)
        self.btnEnterChannelFont = self.btnEnterangle.font()
        self.btnEnterChannelFont.setPointSize(13)
        self.btnEnterChannel.setFont(QtGui.QFont("Monospace"))
        self.btnEnterChannel.setStyleSheet("font-size:15px;")
        self.btnEnterChannel.clicked.connect(self.enterchannel)

        self.btnEnterBeam.move(398,170)
        self.btnEnterBeam.resize(180, 40)
        self.btnEnterBeamFont = self.btnEnterangle.font()
        self.btnEnterBeamFont.setPointSize(13)
        self.btnEnterBeam.setFont(QtGui.QFont("Monospace"))
        self.btnEnterBeam.clicked.connect(self.enterbeam)
        self.btnEnterBeam.setStyleSheet("font-size:15px;")
        
        self.btnShowangleDetails.move(15, 220)
        self.btnShowangleDetails.resize(180, 40)
        self.btnShowangleDetailsFont = self.btnEnterangle.font()
        self.btnShowangleDetailsFont.setPointSize(13)
        self.btnShowangleDetails.setFont(QtGui.QFont("Monospace"))
        self.btnShowangleDetails.clicked.connect(self.showAngleDialog)   #take to function below name showAngleDialog()
        self.btnShowangleDetails.setStyleSheet("font-size:15px;")

        self.btnShowChannelDetails.move(205, 220)
        self.btnShowChannelDetails.resize(180, 40)
        self.btnShowChannelDetailsFont = self.btnEnterangle.font()
        self.btnShowChannelDetailsFont.setPointSize(13)
        self.btnShowChannelDetails.setFont(QtGui.QFont("Monospace"))
        self.btnShowChannelDetails.clicked.connect(self.showAngleChannelDialog)
        self.btnShowChannelDetails.setStyleSheet("font-size:15px;")


        self.btnShowBeamDetails.move(398, 220)
        self.btnShowBeamDetails.resize(180, 40)
        self.btnShowBeamDetailsFont = self.btnEnterangle.font()
        self.btnShowBeamDetailsFont.setPointSize(13)
        self.btnShowBeamDetails.setFont(QtGui.QFont("Monospace"))
        self.btnShowBeamDetails.clicked.connect(self.showangleBeamDialog)
        self.btnShowBeamDetails.setStyleSheet("font-size:15px;")
        
        self.resize(598,280)
        self.setWindowTitle("Steel Database Management System")

    
    #after clicking we come here            
    def enterangle(self):       
        enterangle=AddAngle()  #it will take to function above which generate form to fill for add/append
    def enterchannel(self):
        enterchannel=AddChannel()
    def showAngleDialog(self):
        self.dialog.exec()       #this will create above dialog
    def showAngleChannelDialog(self):
        self.dialogChannel.exec()
    def enterbeam(self):
        enterbeam=AddBeam()
    def showangleBeamDialog(self):
        self.dialogBeam.exec()
    def showload(self):  #this is the showload
        showLoad = Steel()
        showLoad.searchLoad() #it will go to Steel() class which will show the list of designation 
    def showcload(self):
        showcLoad = Steel()
        showcLoad.searchcLoad()
    def showbload(self):
        showbLoad = Steel()
        showbLoad.searchbLoad()    
    def showAngle(self):      #from dialog which we have entered come here and go to function which fetches all the details
        if self.editField.text() is "":
            QMessageBox.warning(QMessageBox(), 'Error',
                                'You must give the designation to show the results for.')
            return None
        showangle = Steel()
        showangle.searchAngle(str(self.editField.text()))
    def showAngleChannel(self):
        if self.editFieldChannel.text() is "":
            QMessageBox.warning(QMessageBox(), 'Error',
                                'You must give the designation to show the results for.')
            return None
        showchannel = Steel()
        showchannel.searchChannel(str(self.editFieldChannel.text()))

    def showAngleBeam(self):
        if self.editFieldBeam.text() is "":
            QMessageBox.warning(QMessageBox(), 'Error',
                                'You must give the designation to show the results for.')
            return None
        showbeam = Steel()
        showbeam.searchBeam(str(self.editFieldBeam.text()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Login()

    if login.exec_() == QDialog.Accepted:
        window = Window()
        window.show()
    sys.exit(app.exec_())
