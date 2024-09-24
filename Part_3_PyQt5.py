"""
Lama Hasbini
EECE 435L - Lab 2
Part 3: GUI Development with PyQt5
"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTableWidgetItem, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
import re
import json
import csv

class Person:
    """
    The Person class represents a person with a name, age, and email.

    :param name: The name of the person.
    :type name: str
    :param age: The age of the person. It must be a non-negative integer.
    :type age: int
    :param email: The email address of the person. It must follow a valid email format.
    :type email: str
    :ivar name: This is where the person's name is stored.
    :vartype name: str
    :ivar age: This is where the person's age is stored after validation.
    :vartype age: int
    :ivar _email: This is where the person's email is stored after validation.
    :vartype _email: str
    """
    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = self.validate_age(age)
        self._email = email if self.validate_email(email) else None

    def introduce(self):
        """
        Prints the introduction of the person, including their name and age.
        """
        print(f"Hello, I'm {self.name}. I'm {self.age} years old.")
    
    def validate_age(self, age):
        """
        Validates that the age is non-negative.

        :param age: The age to validate.
        :type age: int
        :raises ValueError: If the age is negative.
        :return: The validated age.
        :rtype: int
        """
        if age >= 0:
            return age
        else:
            raise ValueError("Age must be non-negative")
        
    def validate_email(self, email):
        """
        Validates that the email is in the correct format.

        :param email: The email to validate.
        :type email: str
        :raises ValueError: If the email is in an invalid format.
        :return: The validated email.
        :rtype: str
        """
        if re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return email
        else:
            raise ValueError("Invalid email format")
    
    def to_json(self):
        """
        Converts the person object into a JSON serializable dictionary.

        :return: A dictionary containing the person's details.
        :rtype: dict
        """
        return {'name': self.name, 'age': self.age, 'email': self._email}

class Student(Person):
    """
    The Student class inherits from Person and adds student-specific details such as student ID and registered courses.

    :param name: The name of the student.
    :type name: str
    :param age: The age of the student. It must be a non-negative integer.
    :type age: int
    :param email: The email address of the student. It must follow a valid email format.
    :type email: str
    :param student_id: The unique ID of the student.
    :type student_id: str
    :param registered_courses: A list of courses the student is registered in (optional).
    :type registered_courses: list
    :ivar student_id: Stores the unique student ID.
    :vartype student_id: str
    :ivar registered_courses: Stores the courses the student is registered in.
    :vartype registered_courses: list
    """
    def __init__(self, name: str, age: int, email: str, student_id: str, registered_courses=None):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = registered_courses if registered_courses else []

    def register_course(self, course):
        """
        Registers a student for a course.

        :param course: The course to register the student in.
        :type course: Course
        """
        if isinstance(course, Course) and course not in self.registered_courses:
            self.registered_courses.append(course)
            course.add_student(self)

    def to_json(self):
        """
        Converts the student object into a JSON serializable dictionary, including student-specific details.

        :return: A dictionary containing the student's details.
        :rtype: dict
        """
        data = super().to_json()
        data['student_id'] = self.student_id
        data['registered_courses'] = {course.course_name: course.course_id for course in self.registered_courses}
        return data

class Instructor(Person):
    """
    The Instructor class inherits from Person and adds instructor-specific details such as instructor ID and assigned courses.

    :param name: The name of the instructor.
    :type name: str
    :param age: The age of the instructor. It must be a non-negative integer.
    :type age: int
    :param email: The email address of the instructor. It must follow a valid email format.
    :type email: str
    :param instructor_id: The unique ID of the instructor.
    :type instructor_id: str
    :param assigned_courses: A list of courses the instructor is assigned to teach (optional).
    :type assigned_courses: list
    :ivar instructor_id: Stores the unique instructor ID.
    :vartype instructor_id: str
    :ivar assigned_courses: Stores the courses the instructor is assigned to teach.
    :vartype assigned_courses: list
    """
    def __init__(self, name: str, age: int, email: str, instructor_id: str, assigned_courses=None):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = assigned_courses if assigned_courses else []

    def assign_course(self, course):
        """
        Assigns a course to the instructor.

        :param course: The course to assign the instructor to.
        :type course: Course
        """
        if isinstance(course, Course) and course not in self.assigned_courses:
            self.assigned_courses.append(course)
            course.instructor = self

    def to_json(self):
        """
        Converts the instructor object into a JSON serializable dictionary, including instructor-specific details.

        :return: A dictionary containing the instructor's details.
        :rtype: dict
        """
        data = super().to_json()
        data['instructor_id'] = self.instructor_id
        data['assigned_courses'] = {course.course_name: course.course_id for course in self.assigned_courses}
        return data

class Course:
    """
    The Course class represents a course with an ID, name, and optionally an instructor and enrolled students.

    :param course_id: The unique ID of the course.
    :type course_id: str
    :param course_name: The name of the course.
    :type course_name: str
    :param instructor: The instructor assigned to the course (optional).
    :type instructor: Instructor
    :param enrolled_students: A list of students enrolled in the course (optional).
    :type enrolled_students: list
    :ivar course_id: Stores the unique course ID.
    :vartype course_id: str
    :ivar course_name: Stores the name of the course.
    :vartype course_name: str
    :ivar instructor: Stores the instructor assigned to the course, if any.
    :vartype instructor: Instructor
    :ivar enrolled_students: Stores the students enrolled in the course.
    :vartype enrolled_students: list
    """
    def __init__(self, course_id: str, course_name: str, instructor: 'Instructor' = None, enrolled_students=None):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = enrolled_students if enrolled_students else []

    def add_student(self, student):
        """
        Enrolls a student in the course.

        :param student: The student to enroll.
        :type student: Student
        """
        if isinstance(student, Student) and student not in self.enrolled_students:
            self.enrolled_students.append(student)

    def to_json(self):
        """
        Converts the course object into a JSON serializable dictionary.

        :return: A dictionary containing the course's details.
        :rtype: dict
        """
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'instructor': self.instructor.instructor_id if self.instructor else None,
            'enrolled_students': {student.name: student.student_id for student in self.enrolled_students}
        }

# 1. Create a main window titled "School Management System"
class SchoolManagementSystem(QtWidgets.QWidget):
    """
    The SchoolManagementSystem class manages the overall functionality for handling
    students, instructors, and courses within the school.

    :param students: A list of students in the school (optional).
    :type students: list
    :param instructors: A list of instructors in the school (optional).
    :type instructors: list
    :param courses: A list of courses offered in the school (optional).
    :type courses: list
    :ivar students: Stores the registered students in the system.
    :vartype students: list
    :ivar instructors: Stores the registered instructors in the system.
    :vartype instructors: list
    :ivar courses: Stores the courses offered in the system.
    :vartype courses: list
    """
    def __init__(self):
        """
        Initializes the SchoolManagementSystem instance, setting up the layout, 
        and initializing the UI components.
        """
        super().__init__()  
        self.students = []  
        self.instructors = []  
        self.courses = []  
        self.init_ui()  
    def init_ui(self):
        """
        Initializes the user interface by setting up the layout and creating tabs 
        for students, instructors, courses, and additional UI components.
        """
        layout = QtWidgets.QVBoxLayout()  
        self.setLayout(layout)  

        self.tab_widget = QtWidgets.QTabWidget()  
        layout.addWidget(self.tab_widget)  

        self.create_student_tab()  
        self.create_instructor_tab()  
        self.create_course_tab()  
        self.create_display_table()  
        self.create_buttons()  
        self.create_search_bar() 

    # 2. Create forms with labels, line edits, and buttons to add Student, Instructor, andCourseobjects.
    def create_student_tab(self):
        """
        Creates the tab for managing students, including input fields for student details 
        and buttons for registering students and adding them to the system.
        """
        student_tab = QtWidgets.QWidget()
        student_layout = QtWidgets.QFormLayout()

        self.student_name_input = QtWidgets.QLineEdit()
        self.student_age_input = QtWidgets.QSpinBox()
        self.student_email_input = QtWidgets.QLineEdit()
        self.student_id_input = QtWidgets.QLineEdit()

        student_layout.addRow("Student Name", self.student_name_input)
        student_layout.addRow("Age", self.student_age_input)
        student_layout.addRow("Email", self.student_email_input)
        student_layout.addRow("Student ID", self.student_id_input)

        self.student_course_combobox = QComboBox()
        student_layout.addRow("Select Course to Register", self.student_course_combobox)

        register_student_button = QtWidgets.QPushButton("Register for Course")
        register_student_button.clicked.connect(self.register_student_for_course)
        student_layout.addRow(register_student_button)

        add_student_button = QtWidgets.QPushButton("Add Student")
        add_student_button.clicked.connect(self.add_student)
        student_layout.addRow(add_student_button)

        student_tab.setLayout(student_layout)
        self.tab_widget.addTab(student_tab, "Students")
    def create_instructor_tab(self):
        """
        Creates the tab for managing instructors, including input fields for instructor details 
        and buttons for assigning instructors and adding them to the system.
        """
        instructor_tab = QtWidgets.QWidget()
        instructor_layout = QtWidgets.QFormLayout()

        self.instructor_name_input = QtWidgets.QLineEdit()
        self.instructor_age_input = QtWidgets.QSpinBox()
        self.instructor_email_input = QtWidgets.QLineEdit()
        self.instructor_id_input = QtWidgets.QLineEdit()

        instructor_layout.addRow("Instructor Name", self.instructor_name_input)
        instructor_layout.addRow("Age", self.instructor_age_input)
        instructor_layout.addRow("Email", self.instructor_email_input)
        instructor_layout.addRow("Instructor ID", self.instructor_id_input)

        self.instructor_course_combobox = QComboBox()
        instructor_layout.addRow("Select Course to Assign", self.instructor_course_combobox)

        assign_instructor_button = QtWidgets.QPushButton("Assign to Course")
        assign_instructor_button.clicked.connect(self.assign_instructor_to_course)
        instructor_layout.addRow(assign_instructor_button)

        add_instructor_button = QtWidgets.QPushButton("Add Instructor")
        add_instructor_button.clicked.connect(self.add_instructor)
        instructor_layout.addRow(add_instructor_button)

        instructor_tab.setLayout(instructor_layout)
        self.tab_widget.addTab(instructor_tab, "Instructors")
    def create_course_tab(self):
        """
        Creates the tab for managing courses, including input fields for course details 
        and buttons for adding courses to the system.
        """
        course_tab = QtWidgets.QWidget()
        course_layout = QtWidgets.QFormLayout()

        self.course_name_input = QtWidgets.QLineEdit()
        self.course_id_input = QtWidgets.QLineEdit()

        course_layout.addRow("Course Name", self.course_name_input)
        course_layout.addRow("Course ID", self.course_id_input)

        add_course_button = QtWidgets.QPushButton("Add Course")
        add_course_button.clicked.connect(self.add_course)
        course_layout.addRow(add_course_button)

        course_tab.setLayout(course_layout)
        self.tab_widget.addTab(course_tab, "Courses")
    
    # Step 3: 4. Validate input fields to ensure they conform to expected formats.
    def validate_name(self, name):
        """
        Validates that the provided name contains only alphabetic characters and spaces.

        :param name: The name to validate.
        :type name: str
        :raises ValueError: If the name is invalid.
        :return: True if valid, raises ValueError otherwise.
        :rtype: bool
        """
        if not re.match(r'^[A-Za-z\s]+$', name):
            raise ValueError("Name must contain only alphabetic characters and spaces.")
        return True
    def validate_email(self, email):
        """
        Validates that the provided email format is correct.

        :param email: The email to validate.
        :type email: str
        :raises ValueError: If the email format is invalid.
        :return: True if valid, raises ValueError otherwise.
        :rtype: bool
        """
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            raise ValueError("Invalid email format.")
        return True
    def validate_id(self, input_id, id_type):
        """
        Validates that the provided ID is not empty.

        :param input_id: The ID to validate.
        :type input_id: str
        :param id_type: The type of ID (for error messaging).
        :type id_type: str
        :raises ValueError: If the ID is empty.
        :return: True if valid, raises ValueError otherwise.
        :rtype: bool
        """
        if not input_id:
            raise ValueError(f"{id_type} cannot be empty.")
        return True

    def add_student(self):
        """
        Adds a new student to the system after validating input fields. 
        Displays success or error messages accordingly.
        """
        name = self.student_name_input.text()
        age = self.student_age_input.value()
        email = self.student_email_input.text()
        student_id = self.student_id_input.text()

        try:
            self.validate_name(name)
            self.validate_email(email)
            self.validate_id(student_id, "Student ID")

            if any(student.student_id == student_id for student in self.students):
                raise ValueError("A student with this ID already exists.")

            student = Student(name, age, email, student_id)
            self.students.append(student)
            self.update_display_table()
            self.update_course_comboboxes()
            self.show_success("Success", "Student added successfully.")

        except ValueError as e:
            self.show_error("Error", str(e))
    def add_instructor(self):
        """
        Adds a new instructor to the system after validating input fields. 
        Displays success or error messages accordingly.
        """
        name = self.instructor_name_input.text()
        age = self.instructor_age_input.value()
        email = self.instructor_email_input.text()
        instructor_id = self.instructor_id_input.text()

        try:
            self.validate_name(name)
            self.validate_email(email)
            self.validate_id(instructor_id, "Instructor ID")

            if any(instructor.instructor_id == instructor_id for instructor in self.instructors):
                raise ValueError("An instructor with this ID already exists.")

            instructor = Instructor(name, age, email, instructor_id)
            self.instructors.append(instructor)
            self.update_display_table()
            self.update_course_comboboxes()
            self.show_success("Success", "Instructor added successfully.")

        except ValueError as e:
            self.show_error("Error", str(e))
    def add_course(self):
        """
        Adds a new course to the system after validating input fields. 
        Displays success or error messages accordingly.
        """
        course_name = self.course_name_input.text()
        course_id = self.course_id_input.text()

        try:
            self.validate_id(course_id, "Course ID")

            if any(course.course_id == course_id for course in self.courses):
                raise ValueError("A course with this ID already exists.")

            course = Course(course_id, course_name)
            self.courses.append(course)

            self.update_display_table()
            self.update_course_comboboxes()
            self.show_success("Success", "Course added successfully.")

        except ValueError as e:
            self.show_error("Error", str(e))

    def update_course_comboboxes(self):
        """
        Updates the course selection comboboxes in both the student and instructor tabs 
        with the latest course names.
        """
        course_names = [course.course_name for course in self.courses]

        self.student_course_combobox.clear()
        self.student_course_combobox.addItems(course_names)

        self.instructor_course_combobox.clear()
        self.instructor_course_combobox.addItems(course_names)

    # 5. Use a QTableWidget to display all students, instructors, and courses.
    def create_display_table(self):
        """
        Creates a table for displaying all students, instructors, and courses, with 
        functionality to edit and delete records.
        """
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "ID", "Type", "Edit", "Delete"])
        self.layout().addWidget(self.table)

    def update_display_table(self):
        """
        Updates the display table with the current list of students, instructors, and courses.
        """
        self.table.setRowCount(0)
        for student in self.students:
            self.add_table_row(student.name, student.student_id, "Student")

        for instructor in self.instructors:
            self.add_table_row(instructor.name, instructor.instructor_id, "Instructor")

        for course in self.courses:
            self.add_table_row(course.course_name, course.course_id, "Course")

    def add_table_row(self, name, id_value, record_type):
        """
        Adds a new row to the table with the specified name, ID, and record type.
        :param name: The name of the record (student, instructor, or course name).
        :type name: str
        :param id_value: The ID of the record.
        :type id_value: str
        :param record_type: The type of record ('Student', 'Instructor', or 'Course').
        :type record_type: str
        """
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(name))
        self.table.setItem(row, 1, QTableWidgetItem(id_value))
        self.table.setItem(row, 2, QTableWidgetItem(record_type))

        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(lambda: self.edit_record(row, record_type))
        self.table.setCellWidget(row, 3, edit_button)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_record(row, record_type))
        self.table.setCellWidget(row, 4, delete_button)

    # 3. Add functionality for students to register for courses from a dropdown list of available courses.
    # for simplicity, i implemented this function to register the last added student to the desired course(s)
    def register_student_for_course(self):
        """
        Registers the selected student for the selected course.
        """
        selected_student_name = self.student_name_input.text()
        selected_course_name = self.student_course_combobox.currentText()

        selected_student = next((student for student in self.students if student.name == selected_student_name), None)
        selected_course = next((course for course in self.courses if course.course_name == selected_course_name), None)

        if selected_student and selected_course:
            selected_student.register_course(selected_course)
            self.update_display_table()
            self.show_success("Success", f"{selected_student_name} registered for {selected_course_name}.")
        else:
            self.show_error("Error", "Invalid student or course selection.")

    # 4. Add functionality for instructors to be assigned to courses from a dropdown list of available courses.
    # for simplicity, i implemented this function to assign the last added instructor to the desired course(s)
    def assign_instructor_to_course(self):
        """
        Assigns the selected instructor to the selected course.
        """
        selected_instructor_name = self.instructor_name_input.text()
        selected_course_name = self.instructor_course_combobox.currentText()

        selected_instructor = next((instructor for instructor in self.instructors if instructor.name == selected_instructor_name), None)
        selected_course = next((course for course in self.courses if course.course_name == selected_course_name), None)

        if selected_instructor and selected_course:
            selected_instructor.assign_course(selected_course)
            self.update_display_table()
            self.show_success("Success", f"{selected_instructor_name} assigned to {selected_course_name}.")
        else:
            self.show_error("Error", "Invalid instructor or course selection.")

    # 6. Implement search functionality to filter records by name, ID, or course.
    def perform_search(self):
        """
        Performs a search in the table based on the input criteria (Name, ID, or Type).
        """
        query = self.search_input.text().lower()
        criteria = self.search_criteria.currentText()

        self.table.setRowCount(0)  

        if criteria == "Name":
            for student in self.students:
                if query in student.name.lower():
                    self.add_table_row(student.name, student.student_id, "Student")
            for instructor in self.instructors:
                if query in instructor.name.lower():
                    self.add_table_row(instructor.name, instructor.instructor_id, "Instructor")
            for course in self.courses:
                if query in course.course_name.lower():
                    self.add_table_row(course.course_name, course.course_id, "Course")

        elif criteria == "ID":
            for student in self.students:
                if query in student.student_id.lower():
                    self.add_table_row(student.name, student.student_id, "Student")
            for instructor in self.instructors:
                if query in instructor.instructor_id.lower():
                    self.add_table_row(instructor.name, instructor.instructor_id, "Instructor")
            for course in self.courses:
                if query in course.course_id.lower():
                    self.add_table_row(course.course_name, course.course_id, "Course")

        elif criteria == "Type":
            if query == "student":
                for student in self.students:
                    self.add_table_row(student.name, student.student_id, "Student")
            elif query == "instructor":
                for instructor in self.instructors:
                    self.add_table_row(instructor.name, instructor.instructor_id, "Instructor")
            elif query == "course":
                for course in self.courses:
                    self.add_table_row(course.course_name, course.course_id, "Course")
            else:
                self.show_error("Error", "Invalid type. Please enter 'student', 'instructor', or 'course'.")
    def create_search_bar(self):
        """
        Creates a search bar for filtering records in the table.
        """
        search_layout = QHBoxLayout()

        search_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        search_layout.addWidget(self.search_input)

        self.search_criteria = QComboBox()
        self.search_criteria.addItems(["Name", "ID", "Type"])
        search_layout.addWidget(self.search_criteria)

        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.perform_search)
        search_layout.addWidget(search_btn)

        self.tab_widget.addTab(QWidget(), "Search")
        self.tab_widget.widget(3).setLayout(search_layout)

    # Step 3: 1. Add buttons to edit and delete records from the system.
    def edit_record(self, row, record_type):
        """
        Edits the selected record based on its type and populates the inputs with its current values.
        
        :param row: The row number of the record in the table.
        :type row: int
        :param record_type: The type of record being edited ('Student', 'Instructor', or 'Course').
        :type record_type: str
        """
        id_value = self.table.item(row, 1).text()  

        if record_type == "Student":
            student = next((s for s in self.students if s.student_id == id_value), None)
            if student:
                self.student_name_input.setText(student.name)
                self.student_age_input.setValue(student.age)
                self.student_email_input.setText(student._email)
                self.student_id_input.setText(student.student_id)

                save_button = QtWidgets.QPushButton("Save Changes")
                save_button.clicked.connect(lambda: self.save_student_changes(student))
                self.layout().addWidget(save_button)

        elif record_type == "Instructor":
            instructor = next((i for i in self.instructors if i.instructor_id == id_value), None)
            if instructor:
                self.instructor_name_input.setText(instructor.name)
                self.instructor_age_input.setValue(instructor.age)
                self.instructor_email_input.setText(instructor._email)
                self.instructor_id_input.setText(instructor.instructor_id)

                save_button = QtWidgets.QPushButton("Save Changes")
                save_button.clicked.connect(lambda: self.save_instructor_changes(instructor))
                self.layout().addWidget(save_button)

        elif record_type == "Course":
            course = next((c for c in self.courses if c.course_id == id_value), None)
            if course:
                self.course_name_input.setText(course.course_name)
                self.course_id_input.setText(course.course_id)

                save_button = QtWidgets.QPushButton("Save Changes")
                save_button.clicked.connect(lambda: self.save_course_changes(course))
                self.layout().addWidget(save_button)

    def save_student_changes(self, student):
        """
        Saves the changes made to the student record.
    
        :param student: The student object being modified.
        :type student: Student
        """
        student.name = self.student_name_input.text()
        student.age = self.student_age_input.value()
        student._email = self.student_email_input.text()
        student.student_id = self.student_id_input.text()
        self.update_display_table()

    def save_instructor_changes(self, instructor):
        """
        Saves the changes made to the instructor record.
    
        :param instructor: The instructor object being modified.
        :type instructor: Instructor
        """
        instructor.name = self.instructor_name_input.text()
        instructor.age = self.instructor_age_input.value()
        instructor._email = self.instructor_email_input.text()
        instructor.instructor_id = self.instructor_id_input.text()
        self.update_display_table()

    def save_course_changes(self, course):
        """
        Saves the changes made to the course record.
    
        :param course: The course object being modified.
        :type course: Course
        """
        course.course_name = self.course_name_input.text()
        course.course_id = self.course_id_input.text()
        self.update_display_table()
        
    def delete_record(self, row, record_type):
        """
        Deletes the selected record from the list of students, instructors, or courses.
    
        :param row: The row number of the record in the table.
        :type row: int
        :param record_type: The type of record being deleted ('Student', 'Instructor', or 'Course').
        :type record_type: str
        """
        id_value = self.table.item(row, 1).text() 
        if record_type == "Student":
            self.students = [student for student in self.students if student.student_id != id_value]
        elif record_type == "Instructor":
            self.instructors = [instructor for instructor in self.instructors if instructor.instructor_id != id_value]
        elif record_type == "Course":
            self.courses = [course for course in self.courses if course.course_id != id_value]

        self.update_display_table()

    # Step 3: 2. Implement functionality to save the data to a file and load it back into the application.
    def save_data(self):
        """
        Save the current data of students, instructors, and courses to a JSON file. 
        The method gathers all student, instructor, and course data, converts it to JSON format, 
        and prompts the user to select a file location to save the data.

        :param self: The instance of the class.
        :type self: SchoolManagementSystem
        :ivar data: The data to be saved, including students, instructors, and courses.
        :vartype data: dict
        """
        data = {
            'students': [student.to_json() for student in self.students],
            'instructors': [instructor.to_json() for instructor in self.instructors],
            'courses': [course.to_json() for course in self.courses],
        }

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'w') as file:
                    json.dump(data, file, indent=4)
                self.show_success("Success", "Data saved successfully.")
            except Exception as e:
                self.show_error("Error", f"Failed to save data: {str(e)}")
    def load_data(self):
        """
        Load student, instructor, and course data from a JSON file.
        This method prompts the user to select a JSON file to load and populates the respective lists for students, 
        instructors, and courses.

        :param self: The instance of the class.
        :type self: SchoolManagementSystem
        :ivar data: The loaded data from the JSON file.
        :vartype data: dict
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Data", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    data = json.load(file)

                self.students = [Student(**student_data) for student_data in data.get('students', [])]
                self.instructors = [Instructor(**instructor_data) for instructor_data in data.get('instructors', [])]
                self.courses = [Course(course_data['course_id'], course_data['course_name']) for course_data in data.get('courses', [])]

                self.update_display_table()
                self.show_success("Success", "Data loaded successfully.")
            except Exception as e:
                self.show_error("Error", f"Failed to load data: {str(e)}")
    
    # Step 3: 3. Add functionality to export records to a CSV file for easy sharing and analysis.
    def export_to_csv(self):
        """
        Export student, instructor, and course data to a CSV file.
        This method allows the user to save the current lists of students, instructors, and courses to a CSV file for 
        easy sharing and analysis.

        :param self: The instance of the class.
        :type self: SchoolManagementSystem
        :ivar file_name: The name of the file selected for exporting data.
        :vartype file_name: str
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Export to CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(['Name', 'ID', 'Type'])
                    for student in self.students:
                        writer.writerow([student.name, student.student_id, 'Student'])
                    for instructor in self.instructors:
                        writer.writerow([instructor.name, instructor.instructor_id, 'Instructor'])
                    for course in self.courses:
                        writer.writerow([course.course_name, course.course_id, 'Course'])

                self.show_success("Success", "Data exported successfully.")
            except Exception as e:
                self.show_error("Error", f"Failed to export data: {str(e)}")
    
    def create_buttons(self):
        """
        Create buttons for saving, loading, and exporting data.
        This method initializes the layout for the buttons and connects them to their respective functionalities.

        :param self: The instance of the class.
        :type self: SchoolManagementSystem
        :ivar button_layout: The layout for the button widgets.
        :vartype button_layout: QHBoxLayout
        """
        button_layout = QtWidgets.QHBoxLayout()

        save_button = QtWidgets.QPushButton("Save Data")
        save_button.clicked.connect(self.save_data)
        button_layout.addWidget(save_button)

        load_button = QtWidgets.QPushButton("Load Data")
        load_button.clicked.connect(self.load_data)
        button_layout.addWidget(load_button)

        export_button = QtWidgets.QPushButton("Export to CSV")
        export_button.clicked.connect(self.export_to_csv)
        button_layout.addWidget(export_button)

        self.layout().addLayout(button_layout)
    
    def show_error(self, title, message):
        """
        Display an error message dialog.

        :param title: The title of the error dialog.
        :type title: str
        :param message: The message to be displayed in the dialog.
        :type message: str
        :param self: The instance of the class.
        :type self: SchoolManagementSystem
        """
        error_msg = QMessageBox()
        error_msg.setIcon(QMessageBox.Critical)
        error_msg.setWindowTitle(title)
        error_msg.setText(message)
        error_msg.exec_()
    def show_success(self, title, message):
        """
        Display a success message dialog.

        :param title: The title of the success dialog.
        :type title: str
        :param message: The message to be displayed in the dialog.
        :type message: str
        :param self: The instance of the class.
        :type self: SchoolManagementSystem
        """
        success_msg = QMessageBox()
        success_msg.setIcon(QMessageBox.Information)
        success_msg.setWindowTitle(title)
        success_msg.setText(message)
        success_msg.exec_()
    
def main():
    """
    Main function to start the application.
    This function initializes the QApplication, creates the main window of the school management system, and enters 
    the application's main event loop.

    :param: None
    :return: None
    """
    import sys
    app = QApplication(sys.argv)
    window = SchoolManagementSystem() 
    window.show()  
    sys.exit(app.exec_())  

if __name__ == '__main__':
    main()