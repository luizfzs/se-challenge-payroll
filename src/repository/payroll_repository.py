import sqlite3


class PayrollRepository:
    def __init__(self):
        self.conn = sqlite3.connect("se-challenge.db", check_same_thread=False)
        self._init_database()

    def _init_database(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS time_report 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, time_report_name TEXT UNIQUE)''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS employee_time_report
                (time_report_id INTEGER, date TEXT, hours_worked INTEGER, employee_id INTEGER, job_group TEXT)''')

    def get_employee_payroll_entries(self):
        cursor = self.conn.execute("SELECT * FROM employee_time_report")
        return list(cursor)

    def get_time_report_by_name(self, time_report_name):
        cursor = self.conn.execute("SELECT * FROM time_report WHERE time_report_name = ? LIMIT 1", (time_report_name,))

        rows = list(cursor)

        return rows[0] if rows else None

    def add_time_report(self, time_report_name):
        cursor = self.conn.execute("INSERT INTO time_report (time_report_name) VALUES (?)", (time_report_name,))
        self.conn.commit()
        return cursor.lastrowid

    def add_time_report_info(self, time_report_id, time_report_entries):
        for entry in time_report_entries:
            cursor = self.conn.execute(
                "INSERT INTO employee_time_report (time_report_id, date, hours_worked, employee_id, job_group) "
                "VALUES (?,?,?,?,?)", (time_report_id, entry[0], entry[1], entry[2], entry[3])
            )

        self.conn.commit()
