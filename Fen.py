# -*- coding:utf-8 -*-
#

import sys
import re
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *


class DataGrid(QWidget):
    def __init__(self):
        super(DataGrid, self).__init__()
        self.setWindowIcon(QIcon("./images/Python2.ico"))
        self.setWindowTitle("分页查询示例")
        self.resize(750, 300)
        # 查询模型
        self.queryModel = None
        # 数据表
        self.tableView = None
        # 总数页文本
        self.totalPageLabel = None
        # 当前页文本
        self.currentPageLabel = None
        self.totalRecordLabel = None
        # 转到页输入框
        self.switchPageLineEdit = None
        # 前一页按钮
        self.prevButton = None
        # 后一页按钮
        self.nextButton = None
        # 转到页按钮
        self.switchPageButton = None
        # 当前页
        self.currentPage = 0
        # 总页数
        self.totalPage = 0
        # 总记录数
        self.totalRecrodCount = 0
        # 每页显示记录数
        self.PageRecordCount = 5

        self.db = None
        self.initUI()

    def initUI(self):
        self.createWindow()
        self.setTableView()
        self.prevButton.clicked.connect(self.onPrevButtonClick)
        self.nextButton.clicked.connect(self.onNextButtonClick)
        self.switchPageButton.clicked.connect(self.onSwitchPageButtonClick)

    def closeEvent(self, event):
        self.db.close()

    def createWindow(self):
        # 操作布局
        operatorLayout = QHBoxLayout()
        self.prevButton = QPushButton("前一页")
        self.nextButton = QPushButton("后一页")
        self.switchPageButton = QPushButton("Go")
        self.switchPageLineEdit = QLineEdit()
        self.switchPageLineEdit.setFixedWidth(40)
        switchPage = QLabel("转到第")
        page = QLabel("页")
        operatorLayout.addWidget(self.prevButton)
        operatorLayout.addWidget(self.nextButton)
        operatorLayout.addWidget(switchPage)
        operatorLayout.addWidget(self.switchPageLineEdit)
        operatorLayout.addWidget(page)
        operatorLayout.addWidget(self.switchPageButton)
        operatorLayout.addWidget(QSplitter())
        # 状态布局
        statusLayout = QHBoxLayout()
        self.totalPageLabel = QLabel()
        self.totalPageLabel.setFixedWidth(70)
        self.currentPageLabel = QLabel()
        self.currentPageLabel.setFixedWidth(70)
        self.totalRecordLabel = QLabel()
        self.totalRecordLabel.setFixedWidth(70)
        statusLayout.addWidget(self.totalPageLabel)
        statusLayout.addWidget(self.currentPageLabel)
        statusLayout.addWidget(QSplitter())
        statusLayout.addWidget(self.totalRecordLabel)
        # 设置表格属性
        self.tableView = QTableView()
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 创建界面
        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(operatorLayout)
        mainLayout.addWidget(self.tableView)
        mainLayout.addLayout(statusLayout)
        self.setLayout(mainLayout)

    def setTableView(self):
        print('*** step2 SetTableView')
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('./db/datagrid.db')
        self.db.open()
        self.queryModel = QSqlQueryModel(self)
        self.currentPage = 1
        self.totalRecrodCount = self.getTotalRecordCount()
        self.totalPage = self.getPageCount()
        self.updateStatus()
        self.setTotalPageLabel()
        self.setTotalRecordLabel()
        self.recordQuery(0)
        self.tableView.setModel(self.queryModel)
        print('totalRecordCount=' + str(self.totalRecrodCount))
        print('totalPage=' + str(self.totalPage))
        self.queryModel.setHeaderData(0, Qt.Horizontal, '编号')
        self.queryModel.setHeaderData(1, Qt.Horizontal, '姓名')
        self.queryModel.setHeaderData(2, Qt.Horizontal, '性别')
        self.queryModel.setHeaderData(3, Qt.Horizontal, '年龄')
        self.queryModel.setHeaderData(4, Qt.Horizontal, '院系')

    def getTotalRecordCount(self):
        self.queryModel.setQuery("select * from people")
        rowCount = self.queryModel.rowCount()
        print('rowCount=' + str(rowCount))
        return rowCount

    def getPageCount(self):
        if self.totalRecrodCount % self.PageRecordCount == 0:
            return self.totalRecrodCount / self.PageRecordCount
        else:
            return self.totalRecrodCount / self.PageRecordCount + 1

    def recordQuery(self, limitIndex):
        szQuery = ("select * from student limit %d,%d" % (limitIndex, self.PageRecordCount))
        print('query sql=' + szQuery)
        self.queryModel.setQuery(szQuery)

    def updateStatus(self):
        szCurrentText = ("当前第%d页" % self.currentPage)
        self.currentPageLabel.setText(szCurrentText)
        if self.currentPage == 1:
            self.prevButton.setEnabled(False)
            self.nextButton.setEnabled(True)
        elif self.currentPage == self.totalPage:
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(False)
        else:
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(True)

    def setTotalPageLabel(self):
        szPageCountText = ("总共%d页" % self.totalPage)
        self.totalPageLabel.setText(szPageCountText)

    def setTotalRecordLabel(self):
        szTotalRecordText = ("共%d条" % self.totalRecrodCount)
        print('*** setTotalRecordLabel szTotalRecordText=' + szTotalRecordText)
        self.totalRecordLabel.setText(szTotalRecordText)

    def onPrevButtonClick(self):
        print('*** onPrevButtonClick ');
        limitIndex = (self.currentPage - 2) * self.PageRecordCount
        self.recordQuery(limitIndex)
        self.currentPage -= 1
        self.updateStatus()

    def onNextButtonClick(self):
        print('*** onNextButtonClick ');
        limitIndex = self.currentPage * self.PageRecordCount
        self.recordQuery(limitIndex)
        self.currentPage += 1
        self.updateStatus()

    def onSwitchPageButtonClick(self):
        # 得到输入字符串
        szText = self.switchPageLineEdit.text()
        # 数字正则表达式
        pattern = re.compile(r'^[0-9]*[1-9][0-9]*$')
        match = pattern.match(szText)

        # 判断是否为数字
        if not match:
            QMessageBox.information(self, "提示", "请输入数字")
            return

        # 是否为空
        if szText == '':
            QMessageBox.information(self, "提示", "请输入跳转页面")
            return

        # 得到页数
        pageIndex = int(szText)
        # 判断是否有指定页
        if pageIndex > self.totalPage or pageIndex < 1:
            QMessageBox.information(self, "提示", "没有指定的页面，请重新输入")
            return

        # 得到查询起始行号
        limitIndex = (pageIndex - 1) * self.PageRecordCount

        # 记录查询
        self.recordQuery(limitIndex);
        # 设置当前页
        self.currentPage = pageIndex
        # 刷新状态
        self.updateStatus();


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = DataGrid()
    win.show()
    sys.exit(app.exec_())
