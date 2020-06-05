import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *


def createDB():
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('./db/datagrid.db')

    if not db.open():
        QMessageBox.critical(None, ("无法打开数据库连接"), ("无法建立到数据库的连接，这个例子需要SQLite支持"), QMessageBox.Cancel)
        return False

    query = QSqlQuery()
    query.exec_("create table student(id int primary key, name varchar(20),ssex char(2),age int, department varchar(30))")
    query.exec_("insert into student values(1, 'zhangsan', '男','20','计算机')")
    query.exec_("insert into student values(2, 'wangwu',  '女','21','数学')")
    query.exec_("insert into student values(3, 'lisi', '男','23','英语')")
    query.exec_("insert into student values(4, 'zhaoliu', '女','24','马克思')")
    db.close()
    return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    createDB()
    sys.exit(app.exec_())
