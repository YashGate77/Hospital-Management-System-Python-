import os
from tkinter import *
from tkinter import messagebox
import sqlite3

class HospitalManagementSystem(Tk):
    def __init__(self):
        super().__init__()
        # Main page decoration
        self.title("Hospital Management System")
        self.geometry("600x400")
        self.config(bg="#f0f0f0")
        self.set_interface()
        self.reset_database()

    def reset_database(self):
        # Remove the existing database file if it exists
        # if os.path.exists('hospital.db'):
        #     os.remove('hospital.db')

        # Create the database and tables
        self.create_tables()

    def create_tables(self):
        # Creating database tables
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS doctors (
                          id TEXT PRIMARY KEY,
                          name TEXT,
                          age INTEGER,
                          experience INTEGER,
                          specialty TEXT,
                          password TEXT,
                          gender TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                          id TEXT PRIMARY KEY,
                          name TEXT,
                          age INTEGER,
                          disease TEXT,
                          password TEXT,
                          gender TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            patient_id INTEGER NOT NULL,
                            doctor_id INTEGER NOT NULL,
                            date TEXT NOT NULL,
                            time TEXT NOT NULL,
                            status TEXT NOT NULL,
                            FOREIGN KEY (patient_id) REFERENCES patients (id),
                            FOREIGN KEY (doctor_id) REFERENCES doctors (id))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS doctor_availability (
                            doctor_id INTEGER NOT NULL,
                            
                            time_start TEXT NOT NULL,
                            time_end TEXT NOT NULL,
                            date TEXT,
                            status TEXT,
                            FOREIGN KEY (doctor_id) REFERENCES doctors (id))''')
   
        conn.commit()
        conn.close()

    def set_interface(self):
        title_frame = Frame(self, bg="#4CAF50", bd=5)
        title_frame.place(relx=0.5, rely=0.1, anchor="center")
        hospital_name_label = Label(title_frame, text="Welcome To\n Shayan Hospital", font=("Helvetica", 20, "bold"), bg="#4CAF50", fg="white")
        hospital_name_label.pack(padx=10, pady=10)

        button_frame = Frame(self, bg="#f0f0f0")
        button_frame.place(relx=0.5, rely=0.5, anchor="center")
        button_style = {"font": ("Helvetica", 16), "bg": "#4CAF50", "fg": "white", "bd": 3, "relief": "raised", "width": 15, "height": 2}

        patient_button = Button(button_frame, text="Patient", command=self.patient_button_click, **button_style)
        patient_button.grid(row=0, column=0, padx=10, pady=10)

        doctor_button = Button(button_frame, text="Doctor", command=self.doctor_button_click, **button_style)
        doctor_button.grid(row=0, column=1, padx=10, pady=10)

        admin_button = Button(button_frame, text="Admin", command=self.admin_button_click, **button_style)
        admin_button.grid(row=0, column=2, padx=10, pady=10)

    def patient_button_click(self):
        messagebox.showinfo("Patient", "Patient section")
        patient_window = Patient()
        patient_window.mainloop()

    def doctor_button_click(self):
        doctor_window = Doctor()
        doctor_window.mainloop()

    def admin_button_click(self):
        admin_window = Admin()
        admin_window.mainloop()
        
class Patient(Tk):
    def __init__(self):
        super().__init__()
        # Doctor page interfaces
        self.title("Patient Side")
        self.geometry("540x560")
        self.set_interface()

    def set_interface(self):
        button_frame = Frame(self, bg="#f0f0f0")
        button_frame.place(relx=0.5, rely=0.5, anchor="center")
        button_style = {"font": ("Helvetica", 16), "bg": "#4CAF50", "fg": "white", "bd": 3, "relief": "raised", "width": 15, "height": 2}

        Button(button_frame, text="Login", command=self.patient_login, **button_style).grid(row=0, column=0, padx=10, pady=10)
        Button(button_frame, text="New Register", command=self.patient_register, **button_style).grid(row=0, column=1, padx=10, pady=10)

    def patient_register(self):
        # Create a new frame for registration
        register_frame = Frame(self, bg="#f0f0f0")
        register_frame.pack(padx=10, pady=10)

        # Create labels and entries for registration
        fields = ["ID", "Name", "Age", "Gender", "Disease", "Password", "Re-enter Password"]
        self.entries = {}
        for i, field in enumerate(fields):
            Label(register_frame, text=f"{field}:").grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(register_frame, show="*" if "Password" in field else "")
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry

        # Create a button to register
        Button(register_frame, text="Register", command=self.register).grid(row=len(fields), column=0, columnspan=2, pady=10)

    def register(self):
        patient_data = {field: entry.get() for field, entry in self.entries.items()}
        if patient_data["Password"] != patient_data["Re-enter Password"]:
            messagebox.showerror("Error", "Password Mismatch")
            return

        try:
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO patients (id, name, age, gender, disease, password) VALUES (?, ?, ?, ?, ?, ?)",
                           (patient_data["ID"], patient_data["Name"], patient_data["Age"], patient_data["Gender"],
                            patient_data["Disease"], patient_data["Password"]))
            conn.commit()
            conn.close()
            messagebox.showinfo("Registration Success", "Patient registered successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def patient_login(self):
        # Create a new frame for login
        login_frame = Frame(self, bg="#f0f0f0")
        login_frame.pack(padx=10, pady=10)

        # Create labels and entries for login
        Label(login_frame, text="ID:").grid(row=0, column=0, padx=10, pady=5)
        self.id_entry = Entry(login_frame)
        self.id_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(login_frame, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = Entry(login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Create a button to log in
        Button(login_frame, text="Log in", command=self.check_login).grid(row=2, column=0, columnspan=2, pady=10)

    def check_login(self):
        patient_id = self.id_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE id=? AND password=?", (patient_id, password))
        patient = cursor.fetchone()
        conn.close()

        if patient:
            messagebox.showinfo("Success", "Login successful")
            self.show_patient_dashboard()
        else:
            messagebox.showerror("Error", "Invalid patient ID or password")

    def show_patient_dashboard(self):
        self.title("Patient Dashboard")
        self.geometry("400x400")
        self.patient_frame = Frame(self, bg="#f0f0f0").pack(padx=10, pady=1)

        button_frame = Frame(self, bg="#f0f0f0")
        button_frame.place(relx=0.5, rely=0.5, anchor="center")
        button_style = {"font": ("Helvetica", 16), "bg": "#4CAF50", "fg": "white", "bd": 3, "relief": "raised", "width": 25, "height": 2}

        Button(button_frame, text="Show AND Book Doctors", command=self.view_doctors, **button_style).grid(row=2,column=1,padx=30,pady=10)
        # Button(button_frame, text="Book Appoinment", command=self.book_appointments, **button_style).grid(row=0, column=1, padx=10, pady=10)

    def view_doctors(self):
       self.title("Show Doctors")
       self.geometry("800x600")
       main_frame = Frame(self, bg="#f0f0f0")
       main_frame.pack(padx=10, pady=10)
        # Create a table to display doctor details
       table_frame = Frame(main_frame)
       table_frame.pack()
        # Create headers
       headers = ["Doctor ID", "Name", "Age", "Experience", "Specialty", "Gender"]
       for i, header in enumerate(headers):
           Label(table_frame, text=header, font=("Arial", 12)).grid(row=0, column=i, padx=5, pady=5)
        # Retrieve doctor details from the database
       conn = sqlite3.connect('hospital.db')
       cursor = conn.cursor()
       cursor.execute("SELECT id, name, age, experience, specialty, gender FROM doctors")
       doctors = cursor.fetchall()
       conn.close()
        # Display doctor details in the table
       doctors_except_third = [doctor for i, doctor in enumerate(doctors) if i != 2]
       for i, doctor in enumerate(doctors_except_third, start=1):
           for j, value in enumerate(doctor):
                Label(table_frame, text=str(value), font=("Arial", 12)).grid(row=i, column=j, padx=5, pady=5)
                # Add a button to book an appointment
           book_button = Button(table_frame, text="Book Appointment", command=lambda doctor_id=doctor[0]: self.book_appointment(doctor_id))
           book_button.grid(row=i, column=len(headers)+1, padx=5, pady=5)
    def book_appointment(self, doctor_id):
      # Create a new window to book an appointment
        book_window = Toplevel(self)
        book_window.title("Book Appointment")
        book_window.geometry("300x200")
      # Create labels and entries for appointment details
        Label(book_window, text="Date (dd-mm-yyyy):").grid(row=0, column=0, padx=10, pady=5)
        date_entry = Entry(book_window)
        date_entry.grid(row=0, column=1, padx=10, pady=5)
        Label(book_window, text="Time:").grid(row=1, column=0, padx=10, pady=5)
        time_entry = Entry(book_window)
        time_entry.grid(row=1, column=1, padx=10, pady=5)
      # Create a button to save the appointment
        save_button = Button(book_window, text="Save Appointment", command=lambda: self.save_appointment(doctor_id, date_entry.get(), time_entry.get()))
        save_button.grid(row=2, column=0, columnspan=2, pady=10)
    def save_appointment(self, doctor_id, date, time):
      # Save the appointment to the database
       patient_id=self.id_entry.get()
       try:
          conn = sqlite3.connect('hospital.db')
          cursor = conn.cursor()
          cursor.execute("INSERT INTO appointments (patient_id, doctor_id, date, time, status) VALUES (?, ?, ?, ?, ?)",
                       (patient_id, doctor_id, date, time, "pending"))
          conn.commit()
          conn.close()
          messagebox.showinfo("Success", "Appointment booked successfully!")
       except sqlite3.Error as e:
           messagebox.showerror("Database Error", str(e))
                 
class Doctor(Tk):
    def __init__(self):
        super().__init__()
        # Doctor page interfaces
        self.title("Doctor Side")
        self.geometry("540x560")
        self.set_interface()

    def set_interface(self):
        button_frame = Frame(self, bg="#f0f0f0")
        button_frame.place(relx=0.5, rely=0.5, anchor="center")
        button_style = {"font": ("Helvetica", 16), "bg": "#4CAF50", "fg": "white", "bd": 3, "relief": "raised", "width": 15, "height": 2}

        Button(button_frame, text="Login", command=self.doc_login, **button_style).grid(row=0, column=0, padx=10, pady=10)
        Button(button_frame, text="New Register", command=self.doc_register, **button_style).grid(row=0, column=1, padx=10, pady=10)

    def doc_register(self):
        # Create a new frame for registration
        register_frame = Frame(self, bg="#f0f0f0")
        register_frame.pack(padx=10, pady=10)

        # Create labels and entries for registration
        fields = ["ID", "Name", "Age","Gender", "Experience", "Specialty", "Password", "Re-enter Password"]
        self.entries = {}
        for i, field in enumerate(fields):
            Label(register_frame, text=f"{field}:").grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(register_frame, show="*" if "Password" in field else "")
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry

        # Create a button to register
        Button(register_frame, text="Register", command=self.register).grid(row=len(fields), column=0, columnspan=2, pady=10)

    def register(self):
       doctor_data = {field: entry.get() for field, entry in self.entries.items()}
       if doctor_data["Password"] != doctor_data["Re-enter Password"]:
        messagebox.showerror("Error", "Password Mismatch")
        return

       try:
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO doctors (id, name, age,gender, experience, specialty, password) VALUES (?, ?,?, ?, ?, ?, ?)",
                       (doctor_data["ID"], doctor_data["Name"], doctor_data["Age"],doctor_data["Gender"],
                        doctor_data["Experience"], doctor_data["Specialty"], doctor_data["Password"]))
        conn.commit()
        conn.close()
        messagebox.showinfo("Registration Success", "Doctor registered successfully!")
       except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
    def doc_login(self):
        # Create a new frame for login
        login_frame = Frame(self, bg="#f0f0f0")
        login_frame.pack(padx=10, pady=10)

        # Create labels and entries for login
        Label(login_frame, text="ID:").grid(row=0, column=0, padx=10, pady=5)
        self.id_entry = Entry(login_frame)
        self.id_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(login_frame, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = Entry(login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Create a button to log in
        Button(login_frame, text="Log in", command=self.check_login).grid(row=2, column=0, columnspan=2, pady=10)

    def check_login(self):
        doctor_id = self.id_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors WHERE id=? AND password=?", (doctor_id, password))
        doctor = cursor.fetchone()
        conn.close()

        if doctor:
            messagebox.showinfo("Success", "Login successful")
            # self.destroy()
           # self.withdraw()
            # Create a new instance of the DoctorDashboard class
            # This would be another class defined similarly to this one
            # For now, just showing a message
            messagebox.showinfo("Dashboard", "Welcome to the Doctor Dashboard!")
            self.doct_interface()
        else:
            messagebox.showerror("Error", "Invalid doctor ID or password")
    def doct_interface(self):
        self.title("Doctor Dashboard")
        self.geometry("400x450")
        button_frame = Frame(self, bg="#f0f0f0")
        button_frame.place(relx=0.5, rely=0.5, anchor="center")
        button_style = {"font": ("Helvetica", 16), "bg": "#4CAF50", "fg": "white", "bd": 3, "relief": "raised", "width": 15, "height": 2}
        Button(button_frame, text="Set Schedule", command=self.set_schedule, **button_style).grid(row=2, column=0, padx=10, pady=10)
        Button(button_frame, text="View Appoinment", command=self.show_appoinment, **button_style).grid(row=2, column=4, padx=10, pady=10)
    def show_appoinment(self):
        appointment_frame = Frame(self, bg="#f0f0f0")
        appointment_frame.pack(padx=10, pady=10)
        doctor_id=self.id_entry.get()
        Label(appointment_frame, text="Appointments:").pack(pady=10)

        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute("SELECT patient_id, date, time, status FROM appointments WHERE doctor_id=?", (doctor_id,))
        appointments = cursor.fetchall()
        conn.close()

        for appointment in appointments:
            Label(appointment_frame, text=f"Patient ID: {appointment[0]}, Date: {appointment[1]}, Time: {appointment[2]}, Status: {appointment[3]}").pack(pady=5)

   
    def set_schedule(self):
        # Create a new frame for setting schedule
        schedule_frame = Frame(self, bg="#f0f0f0")
        schedule_frame.pack(padx=10, pady=10)

        # Create labels and entries for schedule
        Label(schedule_frame, text="Date (dd-mm-yyyy):").grid(row=0, column=0, padx=10, pady=5)
        self.date_entry = Entry(schedule_frame)
        self.date_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(schedule_frame, text="Time Start:").grid(row=1, column=0, padx=10, pady=5)
        self.time_st_entry = Entry(schedule_frame)
        self.time_st_entry.grid(row=1, column=1, padx=10, pady=5)
        Label(schedule_frame, text="(hh:mm am/pm - hh:mm am/pm)").grid(row=1, column=2, padx=10, pady=5)
         
        Label(schedule_frame, text="Time End:").grid(row=2, column=0, padx=10, pady=5)
        self.time_end_entry = Entry(schedule_frame)
        self.time_end_entry.grid(row=2, column=1, padx=10, pady=5)
        Label(schedule_frame, text="(hh:mm am/pm - hh:mm am/pm)").grid(row=1, column=2, padx=10, pady=5)

        Label(schedule_frame, text="Status:").grid(row=3, column=0, padx=10, pady=5)
        self.status_var = StringVar()
        self.status_var.set("Available")
        OptionMenu(schedule_frame, self.status_var, "Available", "Busy").grid(row=3, column=1, padx=10, pady=5)

        # Get the doctor ID from the database using the doctor's login credentials
        doctor_id = self.get_doctor_id()

        # Create a button to save the schedule
        Button(schedule_frame, text="Save Schedule", command=lambda: self.save_schedule(doctor_id)).grid(row=3, column=0, columnspan=2, pady=10)

    def save_schedule(self, doctor_id):
        # Save the schedule to the database
        date = self.date_entry.get()
        time_st = self.time_st_entry.get()
        time_end = self.time_end_entry.get()
        status = self.status_var.get()

        try:
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO doctor_availability (doctor_id, date, time_start, time_end, status) VALUES (?,?,?,?,?)",
               (doctor_id, date, time_st, time_end, status))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Schedule saved successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
    def get_doctor_id(self):
    # Retrieve the doctor ID from the database using the doctor's login credentials
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM doctors WHERE id=? AND password=?", (self.id_entry.get(), self.password_entry.get()))
        doctor_id = cursor.fetchone()[0]
        conn.close()
        return doctor_id
class Admin(Tk):
    def __init__(self):
        super().__init__()
        self.title("Admin")
        self.geometry("640x660")
        self.set_interface()

    def set_interface(self):
        button_frame = Frame(self, bg="#f0f0f0")
        button_frame.place(relx=0.5, rely=0.5, anchor="center")
        button_style = {"font": ("Helvetica", 16), "bg": "#4CAF50", "fg": "white", "bd": 3, "relief": "raised", "width": 15, "height": 2}

        Button(button_frame, text="Show", command=self.show_admin, **button_style).grid(row=0, column=0, padx=10, pady=10)
        Button(button_frame, text="Edit", command=self.edit_data, **button_style).grid(row=0, column=1, padx=10, pady=10)
        Button(button_frame, text="Delete", command=self.delete_data, **button_style).grid(row=0, column=2, padx=10, pady=10)
        Button(button_frame, text="View Appointments", command=self.view_appointments, **button_style).grid(row=1, column=0,  padx=10, pady=10)
        Button(button_frame, text="View All Schedules", command=self.view_all_schedules, **button_style).grid(row=1, column=1, padx=10, pady=10)
    def view_appointments(self):
        self.view_appointments_window = Toplevel(self)
        self.view_appointments_window.title("View Appointments")
        self.view_appointments_window.geometry("600x400")

        # Create a frame to display the appointments information
        appointments_frame = Frame(self.view_appointments_window)
        appointments_frame.pack(fill="both", expand=True)

        # Retrieve appointments data from the database
        appointments_data = self.get_appointments_data()

        # Display appointments data in a scrollable text widget
        appointments_text = Text(appointments_frame, wrap="word")
        appointments_text.pack(fill="both", expand=True)

        # Insert appointments data into the text widget
        for patient_id, doctor_id, date, time, status in appointments_data:
            appointments_text.insert(END, f"Patient ID: {patient_id}\nDoctor ID: {doctor_id}\nDate: {date}\nTime: {time}\nStatus: {status}\n\n")

    def get_appointments_data(self):
        try:
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            cursor.execute("SELECT patient_id, doctor_id, date, time, status FROM appointments")
            appointments_data = cursor.fetchall()
            conn.close()
            return appointments_data
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
       
    def view_all_schedules(self):
        self.title("ALL Schedules")
        self.geometry("800x800")
        self.config(bg="#f0f0f0")
        
    # Create a new frame for viewing all schedules
        schedule_frame = Frame(self, bg="#f0f0f0")
        schedule_frame.pack(padx=20, pady=20)
        # Create a label to display the title
        Label(schedule_frame, text="All Doctor Schedules", font=("Arial", 16)).pack(pady=10)
        # Connect to the database
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        # Retrieve all schedules from the database
        cursor.execute("SELECT doctor_id, time_start, time_end, date, status FROM doctor_availability")
        schedules = cursor.fetchall()
        # Display the schedules in a table
        table_frame = Frame(schedule_frame)
        table_frame.pack()
        # Create headers
        headers = ["Doctor ID", "Time Start", "Time End", "Date", "Status"]
        for i, header in enumerate(headers):
           Label(table_frame, text=header, font=("Arial", 12)).grid(row=0, column=i, padx=5, pady=5)
        # Create rows
        for i, schedule in enumerate(schedules, start=1):
           for j, value in enumerate(schedule):
                Label(table_frame, text=str(value), font=("Arial", 12)).grid(row=i, column=j, padx=5, pady=5)
        # Create a scrollbar
        scrollbar = Scrollbar(schedule_frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        # Create a Text widget to display the schedules
        text_widget = Text(schedule_frame, yscrollcommand=scrollbar.set)
        text_widget.pack(fill="both", expand=True)
        # Insert the schedules into the Text widget
        for schedule in schedules:
           text_widget.insert(END, str(schedule) + "\n")
        # Configure the scrollbar
        scrollbar.config(command=text_widget.yview)
        conn.close()
    def show_admin(self):
        # Admin data details of registered doctors and patients
        admin_frame = Frame(self, bg="#f0f0f0")
        admin_frame.pack(padx=10, pady=10)

        Label(admin_frame, text="Registered Doctors:").pack()
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors")
        doctors = cursor.fetchall()
        for doctor in doctors:
            Label(admin_frame, text=str(doctor)).pack()

        Label(admin_frame, text="Registered Patients:").pack()
        cursor.execute("SELECT * FROM patients")
        patients = cursor.fetchall()
        for patient in patients:
            Label(admin_frame, text=str(patient)).pack()
            # Label(admin_frame,text=str(appoinment))
        conn.close()

    def edit_data(self):
        # Edit registered data
        self.edit_window = Toplevel(self)
        self.edit_window.title("Edit Data")
        self.edit_window.geometry("400x400")
        self.edit_frame = Frame(self.edit_window, bg="#f0f0f0")
        self.edit_frame.pack(padx=10, pady=10)

        Label(self.edit_frame, text="Table:").grid(row=0, column=0, padx=10, pady=5)
        self.table_var = StringVar()
        self.table_var.set("doctors")
        OptionMenu(self.edit_frame, self.table_var, "doctors", "patients").grid(row=0, column=1, padx=10, pady=5)

        Label(self.edit_frame, text="ID:").grid(row=1, column=0, padx=10, pady=5)
        self.id_entry = Entry(self.edit_frame)
        self.id_entry.grid(row=1, column=1, padx=10, pady=5)

        self.update_entries = {}
        Label(self.edit_frame, text="Fields to update:").grid(row=2, column=0, padx=10, pady=5)
        for i, field in enumerate(["Name", "Age", "Experience", "Specialty", "Disease", "Password"], start=3):
            Label(self.edit_frame, text=f"{field}:").grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(self.edit_frame)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.update_entries[field] = entry

        Button(self.edit_frame, text="Update", command=self.update_data).grid(row=9, column=0, columnspan=2, pady=10)
        Label(self.edit_frame, text="Appointments:").grid(row=10, column=0, padx=10, pady=5)
        self.appointment_id_entry = Entry(self.edit_frame)
        self.appointment_id_entry.grid(row=10, column=1, padx=10, pady=5)

        Button(self.edit_frame, text="Update Appointment", command=self.update_appointment).grid(row=11, column=0, columnspan=2, pady=10)

    def update_appointment(self):
        appointment_id = self.appointment_id_entry.get()
        updates = {}

        for field, entry in self.update_entries.items():
            if entry.get():
                updates[field.lower()] = entry.get()

        set_clause = ", ".join([f"{field}=?" for field in updates.keys()])
        values = list(updates.values()) + [appointment_id]

        try:
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            cursor.execute(f"UPDATE appointments SET {set_clause} WHERE id=?", values)
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Appointment updated successfully!")
            self.edit_window.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
    def update_data(self):
        table = self.table_var.get()
        id_value = self.id_entry.get()
        updates = {field.lower(): entry.get() for field, entry in self.update_entries.items() if entry.get()}

        set_clause = ", ".join([f"{field}=?" for field in updates.keys()])
        values = list(updates.values()) + [id_value]

        try:
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {table} SET {set_clause} WHERE id=?", values)
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"{table.capitalize()} data updated successfully!")
            self.edit_window.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def delete_data(self):
        self.delete_window = Toplevel(self)
        self.delete_window.title("Delete Data")
        self.delete_window.geometry("400x200")
        self.delete_frame = Frame(self.delete_window, bg="#f0f0f0")
        self.delete_frame.pack(padx=10, pady=10)

        Label(self.delete_frame, text="Table:").grid(row=0, column=0, padx=10, pady=5)
        self.del_table_var = StringVar()
        self.del_table_var.set("doctors")
        OptionMenu(self.delete_frame, self.del_table_var, "doctors", "patients").grid(row=0, column=1, padx=10, pady=5)

        Label(self.delete_frame, text="ID:").grid(row=1, column=0, padx=10, pady=5)
        self.del_id_entry = Entry(self.delete_frame)
        self.del_id_entry.grid(row=1, column=1, padx=10, pady=5)

        Button(self.delete_frame, text="Delete", command=self.perform_delete).grid(row=2, column=0, columnspan=2, pady=10)

    def perform_delete(self):
        table = self.del_table_var.get()
        id_value = self.del_id_entry.get()

        try:
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table} WHERE id=?", (id_value,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"{table.capitalize()} data deleted successfully!")
            self.delete_window.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

if __name__ == "__main__":
    app = HospitalManagementSystem()
    app.mainloop()
