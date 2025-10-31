from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QInputDialog
)
from PyQt5.QtWidgets import QLineEdit, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QInputDialog, QMessageBox
import sys
import pymysql

class DalalBrosApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DalalBros Portfolio Manager")
        self.setGeometry(100, 100, 900, 600)
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.addTab(self.make_market_tab(), "Market")
        self.tabs.addTab(self.make_company_tab(), "Company")
        self.tabs.addTab(self.make_stock_tab(), "Stock")
        self.tabs.addTab(self.make_portfolio_tab(), "Portfolio")
        self.tabs.addTab(self.make_investor_tab(), "Investor")
        self.tabs.addTab(self.make_tradeorder_tab(), "TradeOrder")
        self.tabs.addTab(self.make_broker_tab(), "Broker")
        self.tabs.addTab(self.make_transaction_tab(), "Transaction")
        self.tabs.addTab(self.make_phone_tab(), "Phone")
        self.tabs.addTab(self.make_broker_investor_tab(), "Broker-Investor")
        self.tabs.addTab(self.make_function_tab(), "Function")




        
        # Repeat for Company, Stock, Portfolio, etc.

    def make_market_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Table to show market data
        self.market_table = QTableWidget()
        self.load_market_table()
        layout.addWidget(self.market_table)
        
        # Add CRUD buttons
        add_btn = QPushButton("Add Market")
        add_btn.clicked.connect(self.add_market)
        layout.addWidget(add_btn)

        delete_btn = QPushButton("Delete Market")
        delete_btn.clicked.connect(self.delete_market)
        layout.addWidget(delete_btn)

        update_btn = QPushButton("Update Market")
        update_btn.clicked.connect(self.update_market)
        layout.addWidget(update_btn)

        # You can add edit and delete buttons similarly here

        widget.setLayout(layout)
        return widget

    def add_market(self):
        # Prompt for Market ID
        mid, ok = QInputDialog.getInt(self, "New Market", "Enter Market ID:")
        if not ok:
            return
        name, ok = QInputDialog.getText(self, "New Market", "Enter Market Name:")
        if not ok or not name:
            return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Market (Mid, name) VALUES (%s, %s);", (mid, name))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", "Market added!")
            self.load_market_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not add market:\n{e}")

    

    def delete_market(self):
        # Ask the user to enter the Market ID to delete
        mid, ok = QInputDialog.getInt(self, "Delete Market", "Enter Market ID to delete:")
        if not ok:
            return

        # Confirm deletion
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete Market ID {mid}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Market WHERE Mid=%s;", (mid,))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", f"Market ID {mid} deleted!")
            self.load_market_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not delete market:\n{e}")

    def update_market(self):
        # Ask for Market ID to update
        mid, ok = QInputDialog.getInt(self, "Update Market", "Enter Market ID to update:")
        if not ok:
            return

        # Ask for new Market Name
        new_name, ok = QInputDialog.getText(self, "Update Market", "Enter new Market Name:")
        if not ok or not new_name:
            return
        
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("UPDATE Market SET name=%s WHERE Mid=%s;", (new_name, mid))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", f"Market ID {mid} updated!")
            self.load_market_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not update market:\n{e}")




    def load_market_table(self):
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Market;")
            rows = cursor.fetchall()
            self.market_table.setRowCount(0)
            self.market_table.setColumnCount(2)
            self.market_table.setHorizontalHeaderLabels(['Mid', 'Name'])
            for r, row in enumerate(rows):
                self.market_table.insertRow(r)
                self.market_table.setItem(r, 0, QTableWidgetItem(str(row[0])))
                self.market_table.setItem(r, 1, QTableWidgetItem(row[1]))
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load market data:\n{e}")


    #Company Tab
    def load_company_table(self):
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Company;")
            rows = cursor.fetchall()
            print("DEBUG: Rows fetched from DB:", rows)  # Add this line!
            self.company_table.setRowCount(0)
            self.company_table.setColumnCount(4)
            self.company_table.setHorizontalHeaderLabels(['Company_id', 'Name', 'Sector', 'Headquarters'])
            for r, row in enumerate(rows):
                self.company_table.insertRow(r)
                for c, value in enumerate(row):
                    self.company_table.setItem(r, c, QTableWidgetItem(str(value)))
            cursor.close()
            conn.close()
        except Exception as e:
            print("DEBUG: Exception in load_company_table:", e)
            QMessageBox.critical(self, "Error", f"Could not load company data:\n{e}")

        
    def make_company_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.company_table = QTableWidget()
        self.load_company_table()
        layout.addWidget(self.company_table)

        add_btn = QPushButton("Add Company")
        add_btn.clicked.connect(self.add_company)
        layout.addWidget(add_btn)

        delete_btn = QPushButton("Delete Company")
        delete_btn.clicked.connect(self.delete_company)
        layout.addWidget(delete_btn)

        update_btn = QPushButton("Update Company")
        update_btn.clicked.connect(self.update_company)
        layout.addWidget(update_btn)

        widget.setLayout(layout)
        return widget

    def add_company(self):
        # Prompt for Company details
        company_id, ok = QInputDialog.getInt(self, "New Company", "Enter Company ID:")
        if not ok:
            return
        name, ok = QInputDialog.getText(self, "New Company", "Enter Company Name:")
        if not ok or not name:
            return
        sector, ok = QInputDialog.getText(self, "New Company", "Enter Sector:")
        if not ok or not sector:
            return
        hq, ok = QInputDialog.getText(self, "New Company", "Enter Headquarters:")
        if not ok or not hq:
            return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Company (Company_id, Name, Sector, Headquarters) VALUES (%s, %s, %s, %s);",
                        (company_id, name, sector, hq))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", "Company added!")
            self.load_company_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not add company:\n{e}")
    
    def update_company(self):
        # Ask for Company ID to update
        company_id, ok = QInputDialog.getInt(self, "Update Company", "Enter Company ID to update:")
        if not ok:
            return

        # Ask for new Company Name
        name, ok = QInputDialog.getText(self, "Update Company", "Enter new Company Name:")
        if not ok or not name:
            return

        # Ask for new Sector
        sector, ok = QInputDialog.getText(self, "Update Company", "Enter new Sector:")
        if not ok or not sector:
            return

        # Ask for new Headquarters
        hq, ok = QInputDialog.getText(self, "Update Company", "Enter new Headquarters:")
        if not ok or not hq:
            return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Company SET Name=%s, Sector=%s, Headquarters=%s WHERE Company_id=%s;",
                (name, sector, hq, company_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", f"Company ID {company_id} updated!")
            self.load_company_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not update company:\n{e}")
    
    def delete_company(self):
        # Ask for Company ID to delete
        company_id, ok = QInputDialog.getInt(self, "Delete Company", "Enter Company ID to delete:")
        if not ok:
            return

        # Confirm deletion
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete Company ID {company_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Company WHERE Company_id=%s;", (company_id,))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", f"Company ID {company_id} deleted!")
            self.load_company_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not delete company:\n{e}")


    #Stock Tab
    def make_stock_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.stock_table = QTableWidget()
        layout.addWidget(self.stock_table)

        add_btn = QPushButton("Add Stock")
        add_btn.clicked.connect(self.add_stock)
        layout.addWidget(add_btn)

        delete_btn = QPushButton("Delete Stock")
        delete_btn.clicked.connect(self.delete_stock)
        layout.addWidget(delete_btn)

        update_btn = QPushButton("Update Stock")
        update_btn.clicked.connect(self.update_stock)
        layout.addWidget(update_btn)

        widget.setLayout(layout)
        self.load_stock_table()
        return widget
    
    def load_stock_table(self):
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Stock;")
            rows = cursor.fetchall()
            self.stock_table.setRowCount(0)
            self.stock_table.setColumnCount(5)
            self.stock_table.setHorizontalHeaderLabels(['stock_id', 'ListingPrice', 'CurrentPrice', 'C_id', 'Mid'])
            for r, row in enumerate(rows):
                self.stock_table.insertRow(r)
                for c, value in enumerate(row):
                    self.stock_table.setItem(r, c, QTableWidgetItem(str(value)))
            cursor.close()
            conn.close()
        except Exception as e:
            print("DEBUG Exception in load_stock_table:", e)
            QMessageBox.critical(self, "Error", f"Could not load stock data:\n{e}")
    
    def add_stock(self):
        stock_id, ok = QInputDialog.getInt(self, "New Stock", "Enter Stock ID:")
        if not ok:
            return
        listing_price, ok = QInputDialog.getDouble(self, "New Stock", "Enter Listing Price:")
        if not ok:
            return
        current_price, ok = QInputDialog.getDouble(self, "New Stock", "Enter Current Price:")
        if not ok:
            return
        c_id, ok = QInputDialog.getInt(self, "New Stock", "Enter Company ID (C_id):")
        if not ok:
            return
        mid, ok = QInputDialog.getInt(self, "New Stock", "Enter Market ID (Mid):")
        if not ok:
            return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Stock (stock_id, ListingPrice, CurrentPrice, C_id, Mid) VALUES (%s, %s, %s, %s, %s);",
                (stock_id, listing_price, current_price, c_id, mid)
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", "Stock added!")
            self.load_stock_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not add stock:\n{e}")

    def update_stock(self):
        stock_id, ok = QInputDialog.getInt(self, "Update Stock", "Enter Stock ID to update:")
        if not ok:
            return

        listing_price, ok = QInputDialog.getDouble(self, "Update Stock", "Enter new Listing Price:")
        if not ok:
            return
        current_price, ok = QInputDialog.getDouble(self, "Update Stock", "Enter new Current Price:")
        if not ok:
            return
        c_id, ok = QInputDialog.getInt(self, "Update Stock", "Enter new Company ID (C_id):")
        if not ok:
            return
        mid, ok = QInputDialog.getInt(self, "Update Stock", "Enter new Market ID (Mid):")
        if not ok:
            return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Stock SET ListingPrice=%s, CurrentPrice=%s, C_id=%s, Mid=%s WHERE stock_id=%s;",
                (listing_price, current_price, c_id, mid, stock_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", f"Stock ID {stock_id} updated!")
            self.load_stock_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not update stock:\n{e}")


    def delete_stock(self):
        stock_id, ok = QInputDialog.getInt(self, "Delete Stock", "Enter Stock ID to delete:")
        if not ok:
            return

        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete Stock ID {stock_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Stock WHERE stock_id=%s;", (stock_id,))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", f"Stock ID {stock_id} deleted!")
            self.load_stock_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not delete stock:\n{e}")

    #Portfolio Tab
    def make_portfolio_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.portfolio_table = QTableWidget()
        layout.addWidget(self.portfolio_table)

        add_btn = QPushButton("Add Portfolio")
        add_btn.clicked.connect(self.add_portfolio)
        layout.addWidget(add_btn)

        delete_btn = QPushButton("Delete Portfolio")
        delete_btn.clicked.connect(self.delete_portfolio)
        layout.addWidget(delete_btn)

        update_btn = QPushButton("Update Portfolio")
        update_btn.clicked.connect(self.update_portfolio)
        layout.addWidget(update_btn)

        widget.setLayout(layout)
        self.load_portfolio_table()
        return widget
    
    def load_portfolio_table(self):
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Portfolio;")
            rows = cursor.fetchall()
            self.portfolio_table.setRowCount(0)
            self.portfolio_table.setColumnCount(2)
            self.portfolio_table.setHorizontalHeaderLabels(['P_id', 'PortfolioValue'])
            for r, row in enumerate(rows):
                self.portfolio_table.insertRow(r)
                for c, value in enumerate(row):
                    self.portfolio_table.setItem(r, c, QTableWidgetItem(str(value)))
            cursor.close()
            conn.close()
        except Exception as e:
            print("DEBUG Exception in load_portfolio_table:", e)
            QMessageBox.critical(self, "Error", f"Could not load portfolio data:\n{e}")

    def add_portfolio(self):
        p_id, ok = QInputDialog.getInt(self, "New Portfolio", "Enter Portfolio ID (P_id):")
        if not ok:
            return
        value, ok = QInputDialog.getDouble(self, "New Portfolio", "Enter Portfolio Value:")
        if not ok:
            return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Portfolio (P_id, PortfolioValue) VALUES (%s, %s);",
                (p_id, value)
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", "Portfolio added!")
            self.load_portfolio_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not add portfolio:\n{e}")

    def update_portfolio(self):
        p_id, ok = QInputDialog.getInt(self, "Update Portfolio", "Enter Portfolio ID (P_id) to update:")
        if not ok:
            return

        value, ok = QInputDialog.getDouble(self, "Update Portfolio", "Enter new Portfolio Value:")
        if not ok:
            return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Portfolio SET PortfolioValue=%s WHERE P_id=%s;",
                (value, p_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", f"Portfolio {p_id} updated!")
            self.load_portfolio_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not update portfolio:\n{e}")

    def delete_portfolio(self):
        p_id, ok = QInputDialog.getInt(self, "Delete Portfolio", "Enter Portfolio ID (P_id) to delete:")
        if not ok:
            return

        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete Portfolio {p_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Portfolio WHERE P_id=%s;", (p_id,))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", f"Portfolio {p_id} deleted!")
            self.load_portfolio_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not delete portfolio:\n{e}")


    #Investor Tab
    def make_investor_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.investor_table = QTableWidget()
        layout.addWidget(self.investor_table)

        add_btn = QPushButton("Add Investor")
        add_btn.clicked.connect(self.add_investor)
        layout.addWidget(add_btn)

        delete_btn = QPushButton("Delete Investor")
        delete_btn.clicked.connect(self.delete_investor)
        layout.addWidget(delete_btn)

        update_btn = QPushButton("Update Investor")
        update_btn.clicked.connect(self.update_investor)
        layout.addWidget(update_btn)

        widget.setLayout(layout)
        self.load_investor_table()
        return widget
    
    def load_investor_table(self):
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Investor;")
            rows = cursor.fetchall()
            self.investor_table.setRowCount(0)
            self.investor_table.setColumnCount(5)
            self.investor_table.setHorizontalHeaderLabels(
                ['I_id', 'Email', 'Balance', 'T_id', 'Referrer_id']
            )
            for r, row in enumerate(rows):
                self.investor_table.insertRow(r)
                for c, value in enumerate(row):
                    self.investor_table.setItem(r, c, QTableWidgetItem(str(value) if value is not None else ''))
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load investor data:\n{e}")

    def add_investor(self):
        I_id, ok = QInputDialog.getInt(self, "New Investor", "Enter Investor ID (I_id):")
        if not ok:
            return
        email, ok = QInputDialog.getText(self, "New Investor", "Enter Email:")
        if not ok or not email:
            return
        balance, ok = QInputDialog.getDouble(self, "New Investor", "Enter Balance (optional):")
        if not ok:
            balance = None
        T_id, ok = QInputDialog.getInt(self, "New Investor", "Enter Trader ID (T_id, optional):")
        if not ok:
            T_id = None
        Referrer_id, ok = QInputDialog.getInt(self, "New Investor", "Enter Referrer ID (optional):")
        if not ok:
            Referrer_id = None

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Investor (I_id, Email, Balance, T_id, Referrer_id) VALUES (%s, %s, %s, %s, %s);",
                (I_id, email, balance, T_id, Referrer_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", "Investor added!")
            self.load_investor_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not add investor:\n{e}")

    def update_investor(self):
        I_id, ok = QInputDialog.getInt(self, "Update Investor", "Enter Investor ID (I_id) to update:")
        if not ok:
            return
        email, ok = QInputDialog.getText(self, "Update Investor", "Enter new Email:")
        if not ok or not email:
            return
        balance, ok = QInputDialog.getDouble(self, "Update Investor", "Enter new Balance:")
        if not ok:
            balance = None
        T_id, ok = QInputDialog.getInt(self, "Update Investor", "Enter new Trader ID (T_id, optional):")
        if not ok:
            T_id = None
        Referrer_id, ok = QInputDialog.getInt(self, "Update Investor", "Enter new Referrer ID (optional):")
        if not ok:
            Referrer_id = None
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Investor SET Email=%s, Balance=%s, T_id=%s, Referrer_id=%s WHERE I_id=%s;",
                (email, balance, T_id, Referrer_id, I_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", f"Investor {I_id} updated!")
            self.load_investor_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not update investor:\n{e}")

    def delete_investor(self):
        I_id, ok = QInputDialog.getInt(self, "Delete Investor", "Enter Investor ID (I_id) to delete:")
        if not ok:
            return
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete Investor {I_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Investor WHERE I_id=%s;", (I_id,))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", f"Investor {I_id} deleted!")
            self.load_investor_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not delete investor:\n{e}")

    #TradeOrder Tab
    def make_tradeorder_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.tradeorder_table = QTableWidget()
        layout.addWidget(self.tradeorder_table)

        add_btn = QPushButton("Add TradeOrder")
        add_btn.clicked.connect(self.add_tradeorder)
        layout.addWidget(add_btn)

        delete_btn = QPushButton("Delete TradeOrder")
        delete_btn.clicked.connect(self.delete_tradeorder)
        layout.addWidget(delete_btn)

        update_btn = QPushButton("Update TradeOrder")
        update_btn.clicked.connect(self.update_tradeorder)
        layout.addWidget(update_btn)

        widget.setLayout(layout)
        self.load_tradeorder_table()
        return widget

    
    def load_tradeorder_table(self):
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM TradeOrder;")
            rows = cursor.fetchall()
            self.tradeorder_table.setRowCount(0)
            self.tradeorder_table.setColumnCount(5)
            self.tradeorder_table.setHorizontalHeaderLabels(
                ['Order_id', 'Order_type', 'Quantity', 'S_id', 'P_id']
            )
            for r, row in enumerate(rows):
                self.tradeorder_table.insertRow(r)
                for c, value in enumerate(row):
                    self.tradeorder_table.setItem(r, c, QTableWidgetItem(str(value) if value is not None else ''))
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load trade order data:\n{e}")

    def add_tradeorder(self):
        Order_id, ok = QInputDialog.getInt(self, "New TradeOrder", "Enter Order ID:")
        if not ok:
            return
        Order_type, ok = QInputDialog.getText(self, "New TradeOrder", "Enter Order Type:")
        if not ok or not Order_type:
            return
        Quantity, ok = QInputDialog.getInt(self, "New TradeOrder", "Enter Quantity:")
        if not ok:
            return
        S_id, ok = QInputDialog.getInt(self, "New TradeOrder", "Enter Stock ID (S_id):")
        if not ok:
            return
        P_id, ok = QInputDialog.getInt(self, "New TradeOrder", "Enter Portfolio ID (P_id):")
        if not ok:
            return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO TradeOrder (Order_id, Order_type, Quantity, S_id, P_id) VALUES (%s, %s, %s, %s, %s);",
                (Order_id, Order_type, Quantity, S_id, P_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", "TradeOrder added!")
            self.load_tradeorder_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not add trade order:\n{e}")

    def update_tradeorder(self):
        Order_id, ok = QInputDialog.getInt(self, "Update TradeOrder", "Enter Order ID to update:")
        if not ok:
            return
        Order_type, ok = QInputDialog.getText(self, "Update TradeOrder", "Enter new Order Type:")
        if not ok or not Order_type:
            return
        Quantity, ok = QInputDialog.getInt(self, "Update TradeOrder", "Enter new Quantity:")
        if not ok:
            return
        S_id, ok = QInputDialog.getInt(self, "Update TradeOrder", "Enter new Stock ID (S_id):")
        if not ok:
            return
        P_id, ok = QInputDialog.getInt(self, "Update TradeOrder", "Enter new Portfolio ID (P_id):")
        if not ok:
            return
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE TradeOrder SET Order_type=%s, Quantity=%s, S_id=%s, P_id=%s WHERE Order_id=%s;",
                (Order_type, Quantity, S_id, P_id, Order_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", f"TradeOrder {Order_id} updated!")
            self.load_tradeorder_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not update trade order:\n{e}")

    def delete_tradeorder(self):
        Order_id, ok = QInputDialog.getInt(self, "Delete TradeOrder", "Enter Order ID to delete:")
        if not ok:
            return
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete TradeOrder {Order_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM TradeOrder WHERE Order_id=%s;", (Order_id,))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", f"TradeOrder {Order_id} deleted!")
            self.load_tradeorder_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not delete trade order:\n{e}")



    #Broker Tab

    def make_broker_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.broker_table = QTableWidget()
        layout.addWidget(self.broker_table)

        add_btn = QPushButton("Add Broker")
        add_btn.clicked.connect(self.add_broker)
        layout.addWidget(add_btn)

        delete_btn = QPushButton("Delete Broker")
        delete_btn.clicked.connect(self.delete_broker)
        layout.addWidget(delete_btn)

        update_btn = QPushButton("Update Broker")
        update_btn.clicked.connect(self.update_broker)
        layout.addWidget(update_btn)

        widget.setLayout(layout)
        self.load_broker_table()
        return widget
    
    def load_broker_table(self):
        try:
            conn = pymysql.connect(host='localhost', user='root', password='Harsh#2004', database='DalalBros')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Broker;")
            rows = cursor.fetchall()
            self.broker_table.setRowCount(0)
            self.broker_table.setColumnCount(4)
            self.broker_table.setHorizontalHeaderLabels(['Broker_id', 'License_no', 'Name', 'T_id'])
            for r, row in enumerate(rows):
                self.broker_table.insertRow(r)
                for c, value in enumerate(row):
                    self.broker_table.setItem(r, c, QTableWidgetItem(str(value) if value is not None else ''))
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load broker data:\n{e}")

    def add_broker(self):
        broker_id, ok = QInputDialog.getInt(self, "New Broker", "Enter Broker ID:")
        if not ok: return
        license_no, ok = QInputDialog.getText(self, "New Broker", "Enter License Number:")
        if not ok or not license_no: return
        name, ok = QInputDialog.getText(self, "New Broker", "Enter Name:")
        if not ok or not name: return
        t_id, ok = QInputDialog.getInt(self, "New Broker", "Enter T_id (Trader ID, optional):")
        if not ok:
            t_id = None

        try:
            conn = pymysql.connect(host='localhost', user='root', password='Harsh#2004', database='DalalBros')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Broker (Broker_id, License_no, Name, T_id) VALUES (%s, %s, %s, %s);",
                (broker_id, license_no, name, t_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", "Broker added!")
            self.load_broker_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not add broker:\n{e}")

            broker_id, ok = QInputDialog.getInt(self, "New Broker", "Enter Broker ID:")
            if not ok: return
            name, ok = QInputDialog.getText(self, "New Broker", "Enter Name:")
            if not ok or not name: return
            email, ok = QInputDialog.getText(self, "New Broker", "Enter Email:")
            if not ok or not email: return
            phone, ok = QInputDialog.getText(self, "New Broker", "Enter Phone:")
            if not ok or not phone: return
            try:
                conn = pymysql.connect(host='localhost', user='root', password='Harsh#2004', database='DalalBros')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Broker (Broker_id, Name, Email, Phone) VALUES (%s, %s, %s, %s);", (broker_id, name, email, phone))
                conn.commit()
                cursor.close()
                conn.close()
                QMessageBox.information(self, "Success", "Broker added!")
                self.load_broker_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not add broker:\n{e}")

    def update_broker(self):
        broker_id, ok = QInputDialog.getInt(self, "Update Broker", "Enter Broker ID to update:")
        if not ok: return
        license_no, ok = QInputDialog.getText(self, "Update Broker", "Enter new License Number:")
        if not ok or not license_no: return
        name, ok = QInputDialog.getText(self, "Update Broker", "Enter new Name:")
        if not ok or not name: return
        t_id, ok = QInputDialog.getInt(self, "Update Broker", "Enter new T_id (Trader ID, optional):")
        if not ok:
            t_id = None

        try:
            conn = pymysql.connect(host='localhost', user='root', password='Harsh#2004', database='DalalBros')
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Broker SET License_no=%s, Name=%s, T_id=%s WHERE Broker_id=%s;",
                (license_no, name, t_id, broker_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", f"Broker {broker_id} updated!")
            self.load_broker_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not update broker:\n{e}")

            broker_id, ok = QInputDialog.getInt(self, "Update Broker", "Enter Broker ID to update:")
            if not ok: return
            name, ok = QInputDialog.getText(self, "Update Broker", "Enter new Name:")
            if not ok or not name: return
            email, ok = QInputDialog.getText(self, "Update Broker", "Enter new Email:")
            if not ok or not email: return
            phone, ok = QInputDialog.getText(self, "Update Broker", "Enter new Phone:")
            if not ok or not phone: return
            try:
                conn = pymysql.connect(host='localhost', user='root', password='Harsh#2004', database='DalalBros')
                cursor = conn.cursor()
                cursor.execute("UPDATE Broker SET Name=%s, Email=%s, Phone=%s WHERE Broker_id=%s;", (name, email, phone, broker_id))
                conn.commit()
                cursor.close()
                conn.close()
                QMessageBox.information(self, "Success", f"Broker {broker_id} updated!")
                self.load_broker_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not update broker:\n{e}")

    def delete_broker(self):
        broker_id, ok = QInputDialog.getInt(self, "Delete Broker", "Enter Broker ID to delete:")
        if not ok: return

        reply = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete Broker {broker_id}?", QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes: return

        try:
            conn = pymysql.connect(host='localhost', user='root', password='Harsh#2004', database='DalalBros')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Broker WHERE Broker_id=%s;", (broker_id,))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", f"Broker {broker_id} deleted!")
            self.load_broker_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not delete broker:\n{e}")

            broker_id, ok = QInputDialog.getInt(self, "Delete Broker", "Enter Broker ID to delete:")
            if not ok: return
            reply = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete Broker {broker_id}?", QMessageBox.Yes | QMessageBox.No)
            if reply != QMessageBox.Yes: return
            try:
                conn = pymysql.connect(host='localhost', user='root', password='Harsh#2004', database='DalalBros')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Broker WHERE Broker_id=%s;", (broker_id,))
                conn.commit()
                cursor.close()
                conn.close()
                QMessageBox.information(self, "Success", f"Broker {broker_id} deleted!")
                self.load_broker_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete broker:\n{e}")

    #Transaction Tab

    def make_transaction_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.transaction_table = QTableWidget()
        layout.addWidget(self.transaction_table)

        add_btn = QPushButton("Add Transaction")
        add_btn.clicked.connect(self.add_transaction)
        layout.addWidget(add_btn)

        delete_btn = QPushButton("Delete Transaction")
        delete_btn.clicked.connect(self.delete_transaction)
        layout.addWidget(delete_btn)

        update_btn = QPushButton("Update Transaction")
        update_btn.clicked.connect(self.update_transaction)
        layout.addWidget(update_btn)

        widget.setLayout(layout)
        self.load_transaction_table()
        return widget
    
    def load_transaction_table(self):
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Transaction;")
            rows = cursor.fetchall()
            self.transaction_table.setRowCount(0)
            self.transaction_table.setColumnCount(5)
            self.transaction_table.setHorizontalHeaderLabels(['T_id', 'TradeType', 'Quantity', 'Price', 'Timestamp'])
            for r, row in enumerate(rows):
                self.transaction_table.insertRow(r)
                for c, value in enumerate(row):
                    self.transaction_table.setItem(r, c, QTableWidgetItem(str(value) if value is not None else ''))
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load transaction data:\n{e}")

            try:
                conn = pymysql.connect(host='localhost', user='root', password='Harsh#2004', database='DalalBros')
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Transaction;")
                rows = cursor.fetchall()
                self.transaction_table.setRowCount(0)
                self.transaction_table.setColumnCount(5)
                self.transaction_table.setHorizontalHeaderLabels(['T_id', 'TradeType', 'Quantity', 'Price', 'Timestamp'])
                for r, row in enumerate(rows):
                    self.transaction_table.insertRow(r)
                    for c, value in enumerate(row):
                        self.transaction_table.setItem(r, c, QTableWidgetItem(str(value) if value is not None else ''))
                cursor.close()
                conn.close()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not load transaction data:\n{e}")

    def add_transaction(self):
        T_id, ok = QInputDialog.getInt(self, "New Transaction", "Enter Transaction ID:")
        if not ok: return
        trade_type, ok = QInputDialog.getText(self, "New Transaction", "Enter Trade Type:")
        if not ok or not trade_type: return
        quantity, ok = QInputDialog.getInt(self, "New Transaction", "Enter Quantity:")
        if not ok: return
        price, ok = QInputDialog.getDouble(self, "New Transaction", "Enter Price:")
        if not ok: return
        timestamp, ok = QInputDialog.getText(self, "New Transaction", "Enter Timestamp (e.g., YYYY-MM-DD HH:MM:SS):")
        if not ok or not timestamp: return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Transaction (T_id, TradeType, Quantity, Price, Timestamp) VALUES (%s, %s, %s, %s, %s);",
                (T_id, trade_type, quantity, price, timestamp)
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", "Transaction added!")
            self.load_transaction_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not add transaction:\n{e}")

    def update_transaction(self):
        T_id, ok = QInputDialog.getInt(self, "Update Transaction", "Enter Transaction ID to update:")
        if not ok: return
        trade_type, ok = QInputDialog.getText(self, "Update Transaction", "Enter new Trade Type:")
        if not ok or not trade_type: return
        quantity, ok = QInputDialog.getInt(self, "Update Transaction", "Enter new Quantity:")
        if not ok: return
        price, ok = QInputDialog.getDouble(self, "Update Transaction", "Enter new Price:")
        if not ok: return
        timestamp, ok = QInputDialog.getText(self, "Update Transaction", "Enter new Timestamp:")
        if not ok or not timestamp: return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Transaction SET TradeType=%s, Quantity=%s, Price=%s, Timestamp=%s WHERE T_id=%s;",
                (trade_type, quantity, price, timestamp, T_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", f"Transaction {T_id} updated!")
            self.load_transaction_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not update transaction:\n{e}")

    def delete_transaction(self):
        T_id, ok = QInputDialog.getInt(self, "Delete Transaction", "Enter Transaction ID to delete:")
        if not ok: return

        reply = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete Transaction {T_id}?", QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes: return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Transaction WHERE T_id=%s;", (T_id,))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", f"Transaction {T_id} deleted!")
            self.load_transaction_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not delete transaction:\n{e}")

    #Phone Tab

    def make_phone_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.phone_table = QTableWidget()
        layout.addWidget(self.phone_table)

        add_btn = QPushButton("Add Phone")
        add_btn.clicked.connect(self.add_phone)
        layout.addWidget(add_btn)

        delete_btn = QPushButton("Delete Phone")
        delete_btn.clicked.connect(self.delete_phone)
        layout.addWidget(delete_btn)

        update_btn = QPushButton("Update Phone")
        update_btn.clicked.connect(self.update_phone)
        layout.addWidget(update_btn)

        widget.setLayout(layout)
        self.load_phone_table()
        return widget

    def load_phone_table(self):
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Phone;")
            rows = cursor.fetchall()
            self.phone_table.setRowCount(0)
            self.phone_table.setColumnCount(2)
            self.phone_table.setHorizontalHeaderLabels(['Iid', 'Phone_number'])
            for r, row in enumerate(rows):
                self.phone_table.insertRow(r)
                for c, value in enumerate(row):
                    self.phone_table.setItem(r, c, QTableWidgetItem(str(value) if value is not None else ''))
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load phone data:\n{e}")


    def add_phone(self):
        iid, ok = QInputDialog.getInt(self, "New Phone", "Enter Iid:")
        if not ok: return
        phone_number, ok = QInputDialog.getText(self, "New Phone", "Enter Phone Number:")
        if not ok or not phone_number: return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Phone (I_id, Phone_number) VALUES (%s, %s);",
                (iid, phone_number)
            )

            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", "Phone added!")
            self.load_phone_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not add phone:\n{e}")


    def update_phone(self):
        iid, ok = QInputDialog.getInt(self, "Update Phone", "Enter Iid to update:")
        if not ok: return
        phone_number, ok = QInputDialog.getText(self, "Update Phone", "Enter new Phone Number:")
        if not ok or not phone_number: return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Phone SET Phone_number=%s WHERE Iid=%s;",
                (phone_number, iid)
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", f"Phone entry {iid} updated!")
            self.load_phone_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not update phone entry:\n{e}")

    def delete_phone(self):
        iid, ok = QInputDialog.getInt(self, "Delete Phone", "Enter Iid to delete:")
        if not ok: return

        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete Phone entry {iid}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes: return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Phone WHERE Iid=%s;", (iid,))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", f"Phone entry {iid} deleted!")
            self.load_phone_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not delete phone entry:\n{e}")

    #RegisteredWith Tab

    def make_broker_investor_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.broker_investor_table = QTableWidget()
        layout.addWidget(self.broker_investor_table)

        add_btn = QPushButton("Add Relation")
        add_btn.clicked.connect(self.add_broker_investor)
        layout.addWidget(add_btn)

        delete_btn = QPushButton("Delete Relation")
        delete_btn.clicked.connect(self.delete_broker_investor)
        layout.addWidget(delete_btn)

        update_btn = QPushButton("Update Relation")
        update_btn.clicked.connect(self.update_broker_investor)
        layout.addWidget(update_btn)

        widget.setLayout(layout)
        self.load_broker_investor_table()
        return widget

    def load_broker_investor_table(self):
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM RegisteredWith;")
            rows = cursor.fetchall()
            self.broker_investor_table.setRowCount(0)
            self.broker_investor_table.setColumnCount(2)
            self.broker_investor_table.setHorizontalHeaderLabels(['B_id', 'I_id'])
            for r, row in enumerate(rows):
                self.broker_investor_table.insertRow(r)
                for c, value in enumerate(row):
                    self.broker_investor_table.setItem(r, c, QTableWidgetItem(str(value) if value is not None else ''))
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load Broker-Investor data:\n{e}")

    def add_broker_investor(self):
        b_id, ok = QInputDialog.getInt(self, "New Relation", "Enter Broker ID (B_id):")
        if not ok: return
        i_id, ok = QInputDialog.getInt(self, "New Relation", "Enter Investor ID (I_id):")
        if not ok: return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO RegisteredWith (B_id, I_id) VALUES (%s, %s);",
                (b_id, i_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", "Relation added!")
            self.load_broker_investor_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not add relation:\n{e}")

    def update_broker_investor(self):
        b_id, ok = QInputDialog.getInt(self, "Update Relation", "Enter current Broker ID (B_id):")
        if not ok: return
        i_id, ok = QInputDialog.getInt(self, "Update Relation", "Enter current Investor ID (I_id):")
        if not ok: return

        new_b_id, ok = QInputDialog.getInt(self, "Update Relation", "Enter new Broker ID:")
        if not ok: return
        new_i_id, ok = QInputDialog.getInt(self, "Update Relation", "Enter new Investor ID:")
        if not ok: return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE RegisteredWith SET B_id=%s, I_id=%s WHERE B_id=%s AND I_id=%s;",
                (new_b_id, new_i_id, b_id, i_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", "Relation updated!")
            self.load_broker_investor_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not update relation:\n{e}")

    def delete_broker_investor(self):
        b_id, ok = QInputDialog.getInt(self, "Delete Relation", "Enter Broker ID (B_id):")
        if not ok: return
        i_id, ok = QInputDialog.getInt(self, "Delete Relation", "Enter Investor ID (I_id):")
        if not ok: return

        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete this Broker-Investor relation?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes: return

        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM RegisteredWith WHERE B_id=%s AND I_id=%s;",
                (b_id, i_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", "Relation deleted!")
            self.load_broker_investor_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not delete relation:\n{e}")


    #Function Tab


    def make_function_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.pid_input = QLineEdit()
        self.pid_input.setPlaceholderText("Enter Portfolio ID (P_id)")

        calc_btn = QPushButton("Show Portfolio Holdings for P_id")
        calc_btn.clicked.connect(self.show_portfolio_holdings)
        
        self.holdings_label = QLabel("Result will be shown here.")

        # Table and button for all portfolios
        show_all_btn = QPushButton("Show ALL Portfolio Holdings")
        show_all_btn.clicked.connect(self.show_all_portfolio_holdings)
        self.all_holdings_table = QTableWidget()
        self.all_holdings_table.setColumnCount(2)
        self.all_holdings_table.setHorizontalHeaderLabels(['P_id', 'TotalHoldings'])

        layout.addWidget(self.pid_input)
        layout.addWidget(calc_btn)
        layout.addWidget(self.holdings_label)
        layout.addWidget(show_all_btn)
        layout.addWidget(self.all_holdings_table)

        widget.setLayout(layout)
        return widget
    
    def show_portfolio_holdings(self):
        try:
            pid_text = self.pid_input.text()
            if not pid_text.isdigit():
                self.holdings_label.setText("Please enter a valid Portfolio ID!")
                return
            pid = int(pid_text)

            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT PortfolioTotalHoldings(%s);", (pid,))
            result = cursor.fetchone()
            total = result[0] if result else 0
            self.holdings_label.setText(f"P_id: {pid}   Total Holdings: {total}")
            cursor.close()
            conn.close()
        except Exception as e:
            self.holdings_label.setText(f"Error: {e}")

    def show_all_portfolio_holdings(self):
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Harsh#2004',
                database='DalalBros'
            )
            cursor = conn.cursor()
            # Query all P_id and their portfolio holdings using your SQL function
            cursor.execute("SELECT P_id, PortfolioTotalHoldings(P_id) FROM Portfolio;")
            rows = cursor.fetchall()
            self.all_holdings_table.setRowCount(0)
            for r, row in enumerate(rows):
                self.all_holdings_table.insertRow(r)
                self.all_holdings_table.setItem(r, 0, QTableWidgetItem(str(row[0])))
                self.all_holdings_table.setItem(r, 1, QTableWidgetItem(str(row[1])))
            cursor.close()
            conn.close()
        except Exception as e:
            self.holdings_label.setText(f"Error (all): {e}")


    




    


    

# App launch
app = QApplication(sys.argv)
main_win = DalalBrosApp()
main_win.show()
sys.exit(app.exec_())
