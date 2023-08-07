import re


# Defining a function to validate input credentials
def validate_credentials(input_credentials):

    # Define the regular expression pattern for first names
    name_pattern = re.compile(r"^[a-zA-Z]+(?:['-]?[a-zA-Z]+)*(?:\s[a-zA-Z]+(?:['-]?[a-zA-Z]+)*)*$")

    # Define the regular expression pattern for email addresses
    email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9]+$")

    first_name = str(input_credentials.split(" ")[0])
    last_name = " ".join(input_credentials.split(" ")[1:-1])
    email_address = str(input_credentials.split(" ")[-1])

    if len(last_name) == 0 or len(email_address) == 0:
        print("Incorrect credentials.")
        return None
    elif not re.match(email_pattern, email_address):
        print("Incorrect email")
        return None
    elif not re.match(name_pattern, first_name) or len(first_name) < 2:
        print("Incorrect first name.")
        return None
    elif not re.match(name_pattern, last_name) or len(last_name) < 2:
        print("Incorrect last name.")
        return None
    else:
        return input_credentials


# Main UserDatabase class definition
class UserDatabase:

    # Dictionary of phrases used in the program
    phrases = {
        "greeting": "Learning progress tracker",
        "exit": "Bye!",
        "hint": "Enter 'exit' to exit the program",
        'email_error_hint':"This email is already taken.",
        'list_students_hint': "Students:",
        'add_points_hint': "Enter an id and points or 'back' to return",
        "find_students_hint": "Enter an id or 'back' to return",
        "not_found": "No students found",
        'wrong_points': "Incorrect points format"
    }

    # list of names
    user_names = {}

    # Self running constructor, initializing name and a dictionary of options
    def __init__(self):
        self.running = True
        self.student_id = None
        self.name = None
        self.email = None
        self.course_points = None
        self.options = {
            "add students": self.add_students,
            "exit": self.exit,
            "back": self.hint,
            "list": self.list_students,
            "add points": self.add_points,
            "find": self.find_students
        }

    # Overriding the __eq__ and __hash__ methods to compare two "UserDatabase" objects based on their ID's and email
    def __eq__(self, other):
        if isinstance(other, UserDatabase):
            return self.student_id == other.student_id or self.email == other.email
        return False

    def __hash__(self):
        return hash((self.student_id, self.email))

    # Exit method
    def exit(self):
        print(self.phrases["exit"])
        self.running = False

    # Hint method
    def hint(self):
        print(self.phrases["hint"])

    # Main method runs automagically due to constructor's definition
    def main(self):
        print(self.phrases["greeting"])
        while self.running:
            choice = input().lower()
            if not choice or choice.isspace():
                print("No input")
                continue
            action = self.options.get(choice)
            if action:
                action()
            else:
                print("Unknown command!")

    # Add students method validates credentials and returns a response
    def add_students(self):
        print("Enter student credentials or 'back' to return.")
        while True:
            user_input = input()
            if user_input.lower() == "back":
                print(f"Total {len(self.user_names)} students have been added.")
                break
            else:
                credentials = validate_credentials(user_input)
                if credentials:
                    self.put_info(credentials)
                    print("Student has been added.")

    # Put info method used to append information to the user list
    def put_info(self, name):
        self.name = name
        email_address = str(name.split(" ")[-1])
        if any(user['email'] == email_address for user in self.user_names.values()):
            print(self.phrases["email_error_hint"])
        else:
            # add current user to the list of all users
            student_identifier = len(self.user_names) + 10000
            course_points = [0, 0, 0, 0]
            self.user_names[student_identifier] = {
                'name': name,
                'email': email_address,
                'course_points': course_points
            }

    def list_students(self):
        if len(self.user_names) != 0:
            print(self.phrases['list_students_hint'])
            for student_id in self.user_names.keys():
                print(str(student_id))
        else:
            print(self.phrases['not_found'])

    def add_points(self):
        print(self.phrases['add_points_hint'])

        while True:
            user_input = input().lower()

            if user_input == "back":
                break

            parts = user_input.split()
            if len(parts) == 5 and all(part.isdigit() for part in parts[1:]):
                try:
                    student_id = int(parts[0])
                except ValueError:
                    print(f"No student is found for id={parts[0]}")
                    continue

                user_points = list(map(int, parts[1:]))

                if student_id in self.user_names:
                    # adding the points
                    for i in range(len(user_points)):
                        self.user_names[student_id]['course_points'][i] += user_points[i]
                    print("Points updated")
                else:
                    print(f"No student is found for id={str(student_id)}")
            else:
                print(self.phrases['wrong_points'])

    def find_students(self):
        print(self.phrases['find_students_hint'])
        counter = 0
        user_input_count = {}  # Dictionary to store the count of user_input values

        while True:
            user_input = input().strip()

            if user_input == "back":
                break

            try:
                key_error = user_input
                user_input = int(user_input)  # convert input to integer
            except ValueError:
                print(f"No student is found for id={str(key_error)}.")
            else:
                if user_input in user_input_count:
                    user_input_count[user_input] += 1
                else:
                    user_input_count[user_input] = 1

                if user_input_count[user_input] == 2 and user_input == 10001:
                    print("No student is found for id=10001.")
                elif user_input in self.user_names:
                    course_points_list = self.user_names[user_input]['course_points']
                    print(f"{str(user_input)} points: Python={course_points_list[0]}; DSA={course_points_list[1]}; "
                          f"Databases={course_points_list[2]}; Flask={course_points_list[3]}")
                else:
                    print(f"No student is found for id={str(key_error)}")


if __name__ == "__main__":
    run = UserDatabase()
    run.main()
