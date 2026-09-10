# Bryan Helms
# CIS261
# WK10 Vibe Coding

FILE_NAME = "student_grades.txt"


class Student:
    """Store one student's scores and calculated grade information."""

    def __init__(self, name, student_id, test1, test2, test3):
        self.name = name
        self.student_id = student_id
        self.test1 = test1
        self.test2 = test2
        self.test3 = test3
        self.average = (test1 + test2 + test3) / 3
        self.grade = self.calculate_grade()

    def calculate_grade(self):
        if self.average >= 90:
            return "A"
        if self.average >= 80:
            return "B"
        if self.average >= 70:
            return "C"
        if self.average >= 60:
            return "D"
        return "F"


def load_students():
    """Load student records from the pipe-delimited data file."""
    students = []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                fields = line.rstrip("\n").split("|")
                if len(fields) != 7:
                    print(f"Warning: skipped malformed record on line {line_number}.")
                    continue
                try:
                    students.append(
                        Student(
                            fields[0],
                            fields[1],
                            float(fields[2]),
                            float(fields[3]),
                            float(fields[4]),
                        )
                    )
                except ValueError:
                    print(f"Warning: skipped invalid scores on line {line_number}.")
    except FileNotFoundError:
        return students
    except OSError as error:
        print(f"Could not load student records: {error}")
    return students


def save_students(students):
    """Save all student records to the pipe-delimited data file."""
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            for student in students:
                file.write(
                    f"{student.name}|{student.student_id}|"
                    f"{student.test1:.2f}|{student.test2:.2f}|"
                    f"{student.test3:.2f}|{student.average:.2f}|"
                    f"{student.grade}\n"
                )
        print(f"Saved {len(students)} student record(s).")
        return True
    except OSError as error:
        print(f"Could not save student records: {error}")
        return False


def get_text(prompt):
    """Read text input, returning None when the user presses ESC."""
    value = input(prompt)
    if value == "\x1b":
        return None
    return value.strip()


def get_score(prompt):
    """Read a score from 0 through 100, or return None for ESC."""
    while True:
        value = get_text(prompt)
        if value is None:
            return None
        try:
            score = float(value)
            if 0 <= score <= 100:
                return score
            print("Please enter a score from 0 through 100.")
        except ValueError:
            print("Please enter a valid number.")


def add_student(students):
    """Prompt for and add one student record.

    Return True when the user wants to add another student.
    """
    print("\nAdd Student (press ESC at any prompt to cancel)")
    name = get_text("Student name: ")
    if name is None:
        print("Add student cancelled.")
        return False
    student_id = get_text("Student ID: ")
    if student_id is None:
        print("Add student cancelled.")
        return False
    if not name or not student_id:
        print("Name and student ID cannot be blank.")
        return False

    scores = []
    for test_number in range(1, 4):
        score = get_score(f"Test {test_number} score: ")
        if score is None:
            print("Add student cancelled.")
            return False
        scores.append(score)

    student = Student(name, student_id, *scores)
    students.append(student)
    print(f"Added {name}: average {student.average:.2f}, grade {student.grade}.")

    while True:
        next_action = get_text("Add another student? (Y/N): ")
        if next_action is None or next_action.casefold() == "n":
            return False
        if next_action.casefold() == "y":
            return True
        print("Please enter Y for another student or N for the main menu.")


def display_students(students, heading="All Students"):
    """Display student records in a formatted table."""
    print(f"\n{heading}")
    if not students:
        print("No student records found.")
        return

    print(
        f"{'Name':<20} {'ID':<12} {'Test 1':>8} {'Test 2':>8} "
        f"{'Test 3':>8} {'Average':>9} {'Grade':>6}"
    )
    print("-" * 79)
    for student in students:
        print(
            f"{student.name[:20]:<20} {student.student_id[:12]:<12} "
            f"{student.test1:>8.2f} {student.test2:>8.2f} "
            f"{student.test3:>8.2f} {student.average:>9.2f} "
            f"{student.grade:>6}"
        )


def display_statistics(students):
    """Display highest, lowest, and class average scores."""
    print("\nClass Statistics")
    if not students:
        print("No student records found.")
        return
    averages = [student.average for student in students]
    print(f"Highest average: {max(averages):.2f}")
    print(f"Lowest average:  {min(averages):.2f}")
    print(f"Class average:   {sum(averages) / len(averages):.2f}")


def search_students(students):
    """Find and display students whose names contain the search text."""
    search_term = get_text("Search name: ")
    if search_term is None:
        print("Search cancelled.")
        return
    matches = [
        student for student in students
        if search_term.casefold() in student.name.casefold()
    ]
    display_students(matches, f"Search Results for '{search_term}'")


def display_menu():
    print("\nStudent Grade Calculator")
    print("1. Add student")
    print("2. Display all students")
    print("3. Display class statistics")
    print("4. Search by student name")
    print("5. Save records")
    print("ESC. Save and exit")


def main():
    students = load_students()
    print(f"Loaded {len(students)} student record(s).")

    while True:
        display_menu()
        choice = input("Choose an option: ")
        if choice == "\x1b" or choice.lower() == "esc":
            save_students(students)
            print("Goodbye!")
            break
        if choice == "1":
            while add_student(students):
                pass
        elif choice == "2":
            display_students(students)
        elif choice == "3":
            display_statistics(students)
        elif choice == "4":
            search_students(students)
        elif choice == "5":
            save_students(students)
        else:
            print("Please choose 1, 2, 3, 4, 5, or ESC.")


if __name__ == "__main__":
    main()
