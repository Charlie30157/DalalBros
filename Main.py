from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QInputDialog
)
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

    from PyQt5.QtWidgets import QInputDialog, QMessageBox

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
    


# App launch
app = QApplication(sys.argv)
main_win = DalalBrosApp()
main_win.show()
sys.exit(app.exec_())
