# Omar Ramadan          AUB ID: 202204622

# Lab 2: School Management System Assignment
# Part 2: GUI Development with Tkinter

"""
School Management System GUI (Tkinter)

This module contains a Tkinter-based GUI for managing students, instructors,
and courses in a school. It allows adding, editing, and deleting records,
assigning instructors to courses, registering students for courses, and
searching records. It also supports saving and loading the data to/from
a JSON file.

Classes:
    None

Functions:
    get_new_student_id(): Generates a unique student ID.
    get_new_instructor_id(): Generates a unique instructor ID.
    get_new_course_id(): Generates a unique course ID.
    save_data(): Saves the current state of students, instructors, courses, 
                 registrations, and assignments to a JSON file.
    load_data(): Loads the state of students, instructors, courses, 
                 registrations, and assignments from a JSON file.
    update_treeview(): Updates the treeview display with the current data.
    update_dropdown_menus(): Updates the dropdown menus for students, 
                             instructors, and courses.
    add_student(): Adds a new student based on user input.
    add_instructor(): Adds a new instructor based on user input.
    add_course(): Adds a new course based on user input.
    register_student_for_course(): Registers a selected student for a 
                                   selected course.
    assign_instructor_to_course(): Assigns a selected instructor to a 
                                   selected course.
    search_records(search_by, search_term): Searches for students, 
                                            instructors, or courses 
                                            by name, ID, or type.
    edit_record(): Edits a selected record (student, instructor, or course).
    update_record(): Updates a record with the user's modifications.
    delete_record(): Deletes a selected record from the system.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import re

# Global variables to manage unique IDs for students, instructors, and courses
max_student_id = 0
max_instructor_id = 0
max_course_id = 0
current_edit_id = 0 # Tracks ID of the record being edited

def get_new_student_id():
    """
    Generates a unique student ID in the format 'Sxxx', where 'xxx' is a 
    zero-padded number.
    
    :return: New unique student ID.
    :rtype: str
    """
    global max_student_id
    max_student_id += 1
    return f"S{max_student_id:03}"

def get_new_instructor_id():
    """
    Generates a unique instructor ID in the format 'Ixxx', where 'xxx' is a 
    zero-padded number.
    
    :return: New unique instructor ID.
    :rtype: str
    """
    global max_instructor_id
    max_instructor_id += 1
    return f"I{max_instructor_id:03}"

def get_new_course_id():
    """
    Generates a unique course ID in the format 'Cxxx', where 'xxx' is a 
    zero-padded number.
    
    :return: New unique course ID.
    :rtype: str
    """
    global max_course_id
    max_course_id += 1
    return f"C{max_course_id:03}"

def save_data():
    """
    Saves the current state of the system, including students, instructors, 
    courses, registrations, and assignments, to a JSON file.
    """
    data = { 'students': students, 'instructors': instructors, 'courses': courses, 'registrations': registrations, 'assignments': assignments }
    with open('school_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    messagebox.showinfo("Success", "Data saved successfully.")

def load_data():
    """
    Loads the state of the system from a JSON file, updating the global 
    students, instructors, courses, registrations, and assignments variables.
    """
    global students, instructors, courses, registrations, assignments
    global max_student_id, max_instructor_id, max_course_id
    try:
        with open('school_data.json', 'r') as f:
            data = json.load(f)
            students = data.get('students', [])
            instructors = data.get('instructors', [])
            courses = data.get('courses', [])
            registrations = data.get('registrations', {})
            assignments = data.get('assignments', {})

            # Update max ids defined globally
            max_student_id = max((int(s['student_id'][1:]) for s in students), default=0)
            max_instructor_id = max((int(i['instructor_id'][1:]) for i in instructors), default=0)
            max_course_id = max((int(c['course_id'][1:]) for c in courses), default=0)


            update_treeview()
            update_dropdown_menus()
            messagebox.showinfo("Success", "Data loaded successfully.")
    except FileNotFoundError:
        messagebox.showerror("Error", "Data file not found.")

# Entries will be stored in dictionary-format located inside arrays
students = []
instructors = []
courses = []
registrations = {}  # Dictionary to store course registrations
assignments = {}    # Dictionary to store instructor assignments

# Called at each entry (Course, Student, Instructor) created
def update_treeview():
    """
    Updates the treeview display with the current students, instructors, 
    and courses.
    """
    for row in tree.get_children():  # Clear existing entries
        tree.delete(row)
    for student in students:
        registered_courses = [c['course_id'] for c in courses if c['course_id'] in student.get('registered_courses_ids', [])]
        additional_info = f"Registered Courses: {', '.join(registered_courses) if registered_courses else 'None'}"
        tree.insert('', 'end', values=(student['student_id'], student['name'], 'Student', additional_info))
    for instructor in instructors:
        assigned_courses = [c['course_id'] for c in courses if c['course_id'] in instructor.get('assigned_courses_ids', [])]
        additional_info = f"Assigned Courses: {', '.join(assigned_courses) if assigned_courses else 'None'}"
        tree.insert('', 'end', values=(instructor['instructor_id'], instructor['name'], 'Instructor', additional_info))
    for course in courses:
        assigned_instructor = next((i for i in instructors if i['instructor_id'] == course['instructor_id']), None)
        registered_students = [s for s in students if course['course_id'] in s.get('registered_courses_ids', [])]  # Corrected this
        instructor_info = (f"Assigned Instructor: {assigned_instructor['instructor_id']} ({assigned_instructor['name']})"
                           if assigned_instructor else "Assigned Instructor: None")
        student_info = ', '.join([f"{s['student_id']} ({s['name']})" for s in registered_students]) if registered_students else "None"
        additional_info = f"{instructor_info}; Registered Students: {student_info}"
        tree.insert('', 'end', values=(course['course_id'], course['course_name'], 'Course', additional_info))

def update_dropdown_menus():
    """
    Updates the dropdown menus with the names of students, instructors, and 
    courses.
    """
    student_dropdownmenu["values"] = [s['name'] for s in students]
    instructor_dropdownmenu["values"] = [i['name'] for i in instructors]
    course_dropdownmenu["values"] = [c['course_name'] for c in courses]
    instructor_dropdownmenu2["values"] = [i['name'] for i in instructors]
    course_dropdownmenu2["values"] = [c['course_name'] for c in courses]


def add_student():
    """
    Adds a new student to the system. The student's name, age, and email 
    are provided by the user through entry fields in the GUI. A unique 
    student ID is generated automatically.
    
    :raises messagebox.showerror: If any required fields are missing or 
                                  if the email format is invalid.
    """
    name = student_name_entry.get()
    age = student_age_entry.get()
    email = student_email_entry.get()
    student_id = get_new_student_id()
    if not name or not email:
        messagebox.showerror("Error", "All fields are required.")
        return
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is None:
         messagebox.showerror("Error", "Invalid email format.")
         return
    if not age.isdigit():
        messagebox.showerror("Error", "Age must be a non-negative integer.")
        return

    students.append({'name': name, 'age': age, 'email': email, 'student_id': student_id})
    update_dropdown_menus()
    update_treeview()
    student_name_entry.delete(0, tk.END)
    student_age_entry.delete(0, tk.END)
    student_email_entry.delete(0, tk.END)

def add_instructor():
    """
    Adds a new instructor to the system. The instructor's name, age, and 
    email are provided by the user through entry fields in the GUI. A 
    unique instructor ID is generated automatically.
    
    :raises messagebox.showerror: If any required fields are missing or 
                                  if the email format is invalid.
    """
    name = instructor_name_entry.get()
    age = instructor_age_entry.get()
    email = instructor_email_entry.get()
    instructor_id = get_new_instructor_id()
    if not name or not email or not instructor_id:
        messagebox.showerror("Error", "All fields are required.")
        return
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is None:
         messagebox.showerror("Error", "Invalid email format.")
         return
    if not age.isdigit():
        messagebox.showerror("Error", "Age must be a non-negative integer.")
        return
    
    instructors.append({'name': name, 'age': age, 'email': email, 'instructor_id': instructor_id})
    instructor_dropdownmenu["values"] = [i['name'] for i in instructors]
    instructor_dropdownmenu2["values"] = [i['name'] for i in instructors]
    update_treeview()
    instructor_name_entry.delete(0, tk.END)
    instructor_age_entry.delete(0, tk.END)
    instructor_email_entry.delete(0, tk.END)

def add_course():
    """
    Adds a new course to the system. The course's name and instructor are 
    provided by the user through entry fields in the GUI. A unique course 
    ID is generated automatically.
    
    :raises messagebox.showerror: If the course name or instructor is 
                                  missing or invalid.
    """
    course_id = get_new_course_id()
    course_name = course_name_entry.get()
    instructor_name = instructor_dropdownmenu.get() 
    if not course_name:
        messagebox.showerror("Error", "Course name is required.")
        return
    instructor_id = next((i['instructor_id'] for i in instructors if i['name'] == instructor_name), None)
    if not instructor_id:
        messagebox.showerror("Error", "Please select a valid instructor.")
        return
    courses.append({'course_id': course_id, 'course_name': course_name, 'instructor_id': instructor_id})
    assignments[course_id] = instructor_name
    course_dropdownmenu["values"] = [c['course_name'] for c in courses]
    course_dropdownmenu2["values"] = [c['course_name'] for c in courses]
    update_treeview()
    course_name_entry.delete(0, tk.END)
    instructor_dropdownmenu.set('')

def register_student_for_course():
    """
    Registers a selected student for a selected course. Both the student 
    and course are chosen from dropdown menus in the GUI.
    
    :raises messagebox.showerror: If the student or course is missing or 
                                  invalid.
    :raises messagebox.showinfo: If the student is already registered for 
                                 the selected course.
    """
    student_name = student_dropdownmenu.get()
    course_name = course_dropdownmenu.get()
    if not student_name or not course_name:
        messagebox.showerror("Error", "Both Student and Course are required.")
        return
    student = next((s for s in students if s['name'] == student_name), None)
    course = next((c for c in courses if c['course_name'] == course_name), None)
    if not student or not course:
        messagebox.showerror("Error", "Student or Course not found.")
        return
    course_id = course['course_id']
    if 'registered_courses_ids' not in student:
        student['registered_courses_ids'] = []
    if course_id not in student['registered_courses_ids']:
        student['registered_courses_ids'].append(course_id)
        if course_id not in registrations:
            registrations[course_id] = []
        registrations[course_id].append(student['student_id'])
        messagebox.showinfo("Success", f"{student_name} has been registered for {course_name}.")
    else:
        messagebox.showinfo("Info", f"{student_name} is already registered for {course_name}.")
    update_treeview()

def assign_instructor_to_course():
    """
    Assigns a selected instructor to a selected course. Both the instructor 
    and course are chosen from dropdown menus in the GUI.
    
    :raises messagebox.showerror: If the instructor or course is missing or invalid.
    """
    instructor_name = instructor_dropdownmenu2.get()
    course_name = course_dropdownmenu2.get()
    if not instructor_name or not course_name:
        messagebox.showerror("Error", "Both Instructor and Course are required.")
        return
    instructor = next((i for i in instructors if i['name'] == instructor_name), None)
    course = next((c for c in courses if c['course_name'] == course_name), None)
    if not instructor or not course:
        messagebox.showerror("Error", "Instructor or Course not found.")
        return
    course['instructor_id'] = instructor['instructor_id']
    assignments[course['course_id']] = instructor_name 
    messagebox.showinfo("Success", f"{instructor_name} has been assigned to {course_name}.")
    update_treeview()

def search_records(search_by, search_term):
    """
    Searches for students, instructors, or courses by name, ID, or type.
    
    :param search_by: The field to search by ('Name', 'ID', or 'Type').
    :type search_by: str
    :param search_term: The search term to match against.
    :type search_term: str
    """
    search_term = search_term.lower()
    filtered_students, filtered_instructors, filtered_courses = [], [], []
    if search_by == 'Name':
        filtered_students = [s for s in students if search_term in s['name'].lower()]
        filtered_instructors = [i for i in instructors if search_term in i['name'].lower()]
        filtered_courses = [c for c in courses if search_term in c['course_name'].lower()]
    elif search_by == 'ID':
        filtered_students = [s for s in students if search_term in s['student_id'].lower()]
        filtered_instructors = [i for i in instructors if search_term in i['instructor_id'].lower()]
        filtered_courses = [c for c in courses if search_term in c['course_id'].lower()]
    elif search_by == 'Type':
        if search_term == 'student':
            filtered_students = students
        elif search_term == 'instructor':
            filtered_instructors = instructors
        elif search_term == 'course':
            filtered_courses = courses
        else:
            messagebox.showerror("Error", "Invalid type. Please enter 'Student', 'Instructor', or 'Course'.")
            return
        
    for i in tree.get_children():
        tree.delete(i)
    for student in filtered_students:
        additional_info = f"Email: {student['email']}"
        tree.insert('', 'end', values=(student['student_id'], student['name'], 'Student', additional_info))
    for instructor in filtered_instructors:
        assigned_courses = [course['course_name'] for course in courses if course['instructor_id'] == instructor['instructor_id']]
        additional_info = f"Email: {instructor['email']}, Assigned Courses: {', '.join(assigned_courses) if assigned_courses else 'None'}"
        tree.insert('', 'end', values=(instructor['instructor_id'], instructor['name'], 'Instructor', additional_info))
    for course in filtered_courses:
        registered_students = [s['name'] for s in students if course['course_id'] in s.get('registered_courses_ids', [])]
        additional_info = f"Assigned Instructor: {assignments.get(course['course_id'], 'None')}; Registered Students: {', '.join(registered_students) if registered_students else 'None'}"
        tree.insert('', 'end', values=(course['course_id'], course['course_name'], 'Course', additional_info))

# Step 3: Implement Advanced Features

# 1. Edit and Delete Records
def edit_record():
    """
    Allows the user to edit a selected record (student, instructor, or 
    course). The selected record's fields are loaded into the relevant 
    entry fields for editing.
    
    :raises messagebox.showerror: If no record is selected.
    """
    global current_edit_id
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No record selected.")
        return
    item_values = tree.item(selected_item[0], 'values')
    record_id = item_values[0]
    record_type = item_values[2]
    current_edit_id = record_id  # Store the ID of the record being edited
    if record_type == 'Student':
        record = next((s for s in students if s['student_id'] == record_id), None)
        if record:
            student_name_entry.delete(0, tk.END)
            student_name_entry.insert(0, record['name'])
            student_age_entry.delete(0, tk.END)
            student_age_entry.insert(0, record.get('age', ''))
            student_email_entry.delete(0, tk.END)
            student_email_entry.insert(0, record['email'])
    elif record_type == 'Instructor':
        record = next((i for i in instructors if i['instructor_id'] == record_id), None)
        if record:
            instructor_name_entry.delete(0, tk.END)
            instructor_name_entry.insert(0, record['name'])
            instructor_age_entry.delete(0, tk.END)
            instructor_age_entry.insert(0, record.get('age', ''))
            instructor_email_entry.delete(0, tk.END)
            instructor_email_entry.insert(0, record['email'])
    elif record_type == 'Course':
        record = next((c for c in courses if c['course_id'] == record_id), None)
        if record:
            course_name_entry.delete(0, tk.END)
            course_name_entry.insert(0, record['course_name'])
            instructor_dropdownmenu.set(record.get('instructor_id', ''))

def update_record():
    """
    Updates the currently selected record (student, instructor, or course) 
    based on the user's modifications to the entry fields.
    
    :raises messagebox.showerror: If no record is selected for editing.
    """
    global current_edit_id
    if not current_edit_id:
        messagebox.showerror("Error", "No record selected for editing.")
        return
    # Update the corresponding record
    if any(s['student_id'] == current_edit_id for s in students):
        for s in students:
            if s['student_id'] == current_edit_id:
                s.update({'name': student_name_entry.get(), 'age': student_age_entry.get(), 'email': student_email_entry.get()})
    elif any(i['instructor_id'] == current_edit_id for i in instructors):
        for i in instructors:
            if i['instructor_id'] == current_edit_id:
                i.update({'name': instructor_name_entry.get(), 'age': instructor_age_entry.get(), 'email': instructor_email_entry.get()})
    elif any(c['course_id'] == current_edit_id for c in courses):
        for c in courses:
            if c['course_id'] == current_edit_id:
                c.update({'course_name': course_name_entry.get(), 'instructor_id': instructor_dropdownmenu.get()})
    current_edit_id = None
    update_treeview()
    messagebox.showinfo("Info", "Record updated successfully.")

def delete_record():
    """
    Deletes the currently selected record (student, instructor, or course) 
    from the system.
    
    :raises messagebox.showerror: If no record is selected.
    """
    global assignments, registrations, courses, students, instructors
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No record selected.")
        return
    item_values = tree.item(selected_item[0], 'values')
    record_id = item_values[0]
    record_type = item_values[2]
    if record_type == 'Student':
        students[:] = [s for s in students if s['student_id'] != record_id]
        for course_id in registrations:
            registrations[course_id] = [s_id for s_id in registrations[course_id] if s_id != record_id]
    elif record_type == 'Instructor':
        instructors[:] = [i for i in instructors if i['instructor_id'] != record_id]
        assignments = {k: v for k, v in assignments.items() if v != record_id}
    elif record_type == 'Course':
        courses[:] = [c for c in courses if c['course_id'] != record_id]
        registrations.pop(record_id, None)
        assignments.pop(record_id, None)
    update_treeview()
    messagebox.showinfo("Info", "Record deleted successfully.")

# Step 1: Create a Tkinter Window:

# 1. Basic Window Setup:

window = tk.Tk()
window.title("School Management System")
window.geometry("1500x750")

# Grid Layout to diplay all fields/TreeView on Basic Window Setup:
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=2)  # Make sure the TreeView takes more space
window.rowconfigure(0, weight=1) 

# Step 2: Add GUI Components:
form_frame = tk.Frame(window)
form_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# 2. Student, Instructor, and Course Forms:
# Frames for each form:
student_frame = tk.LabelFrame(form_frame, text="Student Form")
student_frame.pack(fill="x", padx=10, pady=5)

instructor_frame = tk.LabelFrame(form_frame, text="Instructor Form")
instructor_frame.pack(fill="x", padx=10, pady=5)

course_frame = tk.LabelFrame(form_frame, text="Course Form")
course_frame.pack(fill="x", padx=10, pady=5)

# Entry Fields for each form (Object Type)

# Student
tk.Label(student_frame, text="Student Name:").grid(row=0, column=0, padx=5, pady=2)
student_name_entry = tk.Entry(student_frame)
student_name_entry.grid(row=0, column=1, padx=5, pady=2)

tk.Label(student_frame, text="Age:").grid(row=1, column=0, padx=5, pady=2)
student_age_entry = tk.Entry(student_frame)
student_age_entry.grid(row=1, column=1, padx=5, pady=2)

tk.Label(student_frame, text="Email:").grid(row=2, column=0, padx=5, pady=2)
student_email_entry = tk.Entry(student_frame)
student_email_entry.grid(row=2, column=1, padx=5, pady=2)

add_student_btn = tk.Button(student_frame, text="Add Student:", command=add_student)
add_student_btn.grid(row=4, column=0, columnspan=2, pady=2)

# Instructor
tk.Label(instructor_frame, text="Instructor Name:").grid(row=0, column=0, padx=5, pady=2)
instructor_name_entry = tk.Entry(instructor_frame)
instructor_name_entry.grid(row=0, column=1, padx=5, pady=2)

tk.Label(instructor_frame, text="Age:").grid(row=1, column=0, padx=5, pady=2)
instructor_age_entry = tk.Entry(instructor_frame)
instructor_age_entry.grid(row=1, column=1, padx=5, pady=2)

tk.Label(instructor_frame, text="Email:").grid(row=2, column=0, padx=5, pady=2)
instructor_email_entry = tk.Entry(instructor_frame)
instructor_email_entry.grid(row=2, column=1, padx=5, pady=2)

add_instructor_btn = tk.Button(instructor_frame, text="Add Instructor:", command=add_instructor)
add_instructor_btn.grid(row=4, column=0, columnspan=2, pady=2)

tk.Label(course_frame, text="Course Name:").grid(row=1, column=0, padx=5, pady=2)
course_name_entry = tk.Entry(course_frame)
course_name_entry.grid(row=1, column=1, padx=5, pady=2)

tk.Label(course_frame, text="Instructor:").grid(row=2, column=0, padx=5, pady=2)
instructor_dropdownmenu = ttk.Combobox(course_frame)
instructor_dropdownmenu.grid(row=2, column=1, padx=5, pady=2)

add_course_btn = tk.Button(course_frame, text="Add Course:", command=add_course)
add_course_btn.grid(row=3, column=0, columnspan=2, pady=2)

# 3. Student Registration for Courses:
registration_frame = tk.LabelFrame(form_frame, text="Student Registration for Courses")
registration_frame.pack(fill="x", padx=10, pady=2)

tk.Label(registration_frame, text="Select Student:").grid(row=0, column=0, padx=5, pady=2)
student_dropdownmenu = ttk.Combobox(registration_frame)
student_dropdownmenu.grid(row=0, column=1, padx=5, pady=2)

tk.Label(registration_frame, text="Select Course:").grid(row=1, column=0, padx=5, pady=2)
course_dropdownmenu = ttk.Combobox(registration_frame)
course_dropdownmenu.grid(row=1, column=1, padx=5, pady=2)

register_btn = tk.Button(registration_frame, text="Register", command=register_student_for_course)
register_btn.grid(row=2, column=0, columnspan=2, pady=2)

# 4. Instructor Assignment to Courses:
assignment_frame = tk.LabelFrame(form_frame, text="Instructor Assignment for Courses")
assignment_frame.pack(fill="x", padx=10, pady=2)

tk.Label(assignment_frame, text="Select Instructor:").grid(row=0, column=0, padx=5, pady=2)
instructor_dropdownmenu2 = ttk.Combobox(assignment_frame)
instructor_dropdownmenu2.grid(row=0, column=1, padx=5, pady=2)

tk.Label(assignment_frame, text="Select Course:").grid(row=1, column=0, padx=5, pady=2)
course_dropdownmenu2 = ttk.Combobox(assignment_frame)
course_dropdownmenu2.grid(row=1, column=1, padx=5, pady=2)

assignment_btn = tk.Button(assignment_frame, text="Assign", command=assign_instructor_to_course)
assignment_btn.grid(row=2, column=0, columnspan=2, pady=2)

# 5. Display All Records:
tree_frame = tk.Frame(window)
tree_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
columns = ("ID", "Name", "Type", "Additional Info")
tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Type", text="Type")
tree.heading("Additional Info", text="Additional Info")
tree.column("#0", width=0, stretch=tk.NO)  # Hides the first column (tree ID)
tree.column("ID", width=100, stretch=tk.NO)
tree.column("Name", width=200, stretch=tk.NO)
tree.column("Type", width=100, stretch=tk.NO)
tree.column("Additional Info", width=400, stretch=tk.YES)
tree.pack(fill="both", expand=True)

# 6. Search Functionality
search_frame = tk.LabelFrame(window, text="Search")
search_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

search_option = ttk.Combobox(search_frame, values=['Name', 'ID', 'Type']) # Search option dropdown
search_option.set('Name')  # Default option
search_option.grid(row=0, column=0, padx=5, pady=5)

search_entry = tk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=5, pady=5)

search_button = tk.Button(search_frame, text="Search", command=lambda: search_records(search_option.get(), search_entry.get()))
search_button.grid(row=0, column=2, padx=5, pady=5)

# Edit and Delete Buttons
edit_btn = tk.Button(tree_frame, text="Edit", command=edit_record)
edit_btn.pack(side="left", padx=5, pady=5)

update_btn = tk.Button(tree_frame, text="Update Record", command=update_record)
update_btn.pack(side="left", padx=5, pady=5)

delete_btn = tk.Button(tree_frame, text="Delete", command=delete_record)
delete_btn.pack(side="left", padx=5, pady=5)

# Step 3: Implement Advanced Features

# 2. Save and Load Data
save_btn = tk.Button(window, text="Save Data", command=save_data)
save_btn.grid(row=2, column=0, padx=10, pady=10)

load_btn = tk.Button(window, text="Load Data", command=load_data)
load_btn.grid(row=2, column=1, padx=10, pady=10)

window.mainloop()