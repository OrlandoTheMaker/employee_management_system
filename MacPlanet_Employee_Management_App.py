import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('attendance.db')
c = conn.cursor()

# Create the employee table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS employees
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')

# Create the attendance table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS attendance
             (id INTEGER PRIMARY KEY AUTOINCREMENT, employee_id INTEGER,
             status TEXT, date TEXT,
             FOREIGN KEY(employee_id) REFERENCES employees(id))''')

# Create the main tkinter application window
root = tk.Tk()
root.title("MacPlanet Employee Attendance")
root.config(bg="black")

# Function to add a new employee to the database
def add_employee():
    name = employee_entry.get().strip()
    if name:
        c.execute("INSERT INTO employees (name) VALUES (?)", (name,))
        conn.commit()
        messagebox.showinfo("Success", "Employee added successfully!")
        employee_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a valid employee name.")

# Function to record attendance for an employee
def record_attendance():
    employee_name = employee_entry.get().strip()
    status = status_var.get()
    if employee_name:
        c.execute("SELECT id FROM employees WHERE name = ?", (employee_name,))
        result = c.fetchone()
        if result:
            employee_id = result[0]
            c.execute("INSERT INTO attendance (employee_id, status, date) VALUES (?, ?, DATE('now'))", (employee_id, status))
            conn.commit()
            messagebox.showinfo("Success", "Attendance recorded successfully!")
            employee_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Employee does not exist.")
    else:
        messagebox.showwarning("Warning", "Please enter a valid employee name.")

# Function to generate an attendance report
def generate_report():
    c.execute("SELECT employees.name, attendance.status, attendance.date FROM employees INNER JOIN attendance ON employees.id = attendance.employee_id")
    results = c.fetchall()
    report = ""
    for row in results:
        report += f"Employee: {row[0]}, Status: {row[1]}, Date: {row[2]}\n"
    if report:
        messagebox.showinfo("Attendance Report", report)
    else:
        messagebox.showinfo("Attendance Report", "No attendance records found.")

# Create the employee entry label and entry field
employee_label = tk.Label(root, text="Employee Name:")
employee_label.pack()
employee_entry = tk.Entry(root)
employee_entry.pack()

# Create the attendance status radio buttons
status_label = tk.Label(root, text="Attendance Status:")
status_label.place(x=625, y=125)

status_var = tk.StringVar(value="Present")
present_radio = tk.Radiobutton(root, text="Present", variable=status_var, value="Present")
present_radio.place(x=900, y=275)

absent_radio = tk.Radiobutton(root, text="Absent", variable=status_var, value="Absent")
absent_radio.place(x=900, y=175)

late_radio = tk.Radiobutton(root, text="Late", variable=status_var, value="Late")
late_radio.place(x=900, y=225)




# Create the buttons for adding employees, recording attendance, and generating reports
add_button = tk.Button(root, text="Add Employee", command=add_employee)
add_button.config(bg='green')
add_button.place(x=325, y=275)

record_button = tk.Button(root, text="Record Attendance", command=record_attendance)
record_button.config(bg='red')
record_button.place(x=325, y=175)

report_button = tk.Button(root, text="Generate Report", command=generate_report)
report_button.config(bg='yellow')
report_button.place(x=325, y=225)

# Start the tkinter event loop
root.mainloop()

# Close the database connection when the application
