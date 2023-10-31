from tabulate import tabulate


class View:
    def show_tasks(self, tasks):
        print("Tasks:")
        for task in tasks:
            print(f"ID: {task[0]}, Title: {task[1]}, Description: {task[2]}")

    def show_author(self, tasks):
        print("Authors:")
        headers = ["AuthorID", "Name", "Surname"]
        table = tabulate(tasks, headers, tablefmt="pretty")
        print(table)

    def show_res_q1(self, data):
        print("Result:")
        headers = ["Author's Name", "Author's Surname", "Publication", "Date"]
        table = tabulate(data, headers, tablefmt="pretty")
        print(table)

    def show_res_q2(self, data):
        print("Result:")
        headers = ["Author's Name", "Author's Surname", "PublicationCount"]
        table = tabulate(data, headers, tablefmt="pretty")
        print(table)

    def show_res_q3(self, data):
        print("Result:")
        headers = ["Language", "PublicationCount"]
        table = tabulate(data, headers, tablefmt="pretty")
        print(table)

    def show_publication(self, tasks):
        print("Publications:")
        headers = ["PublicationID", "Name", "Language", "Pages", "Field"]
        table = tabulate(tasks, headers, tablefmt="pretty")
        print(table)

    def show_collection(self, tasks):
        print("Collections:")
        headers = ["ISSN", "Name", "Type", "Category"]
        table = tabulate(tasks, headers, tablefmt="pretty")
        print(table)

    def show_publishing(self, tasks):
        print("Publishings:")
        headers = ["AuthorID", "PublicationID", "ISSN", "Date"]
        table = tabulate(tasks, headers, tablefmt="pretty")
        print(table)

    def get_data_input(self, table_name):
        if table_name == "Author":
            authorid = input("Enter AuthorID: ")
            name = input("Enter author's Name: ")
            surname = input("Enter author's Surname: ")
            data = {
                "\"AuthorID\"": authorid,
                "\"Name\"": name,
                "\"Surname\"": surname
            }
            return data
        elif table_name == "Publication":
            pid = input("Enter PublicationID: ")
            name = input("Enter publication's name: ")
            language = input("Enter language: ")
            field = input("Enter field: ")
            pages = input("Enter pages: ")
            data = {
                "\"PublicationID\"": pid,
                "\"Name\"": name,
                "\"Language\"": language,
                "\"Field\"": field,
                "\"Pages\"": pages
            }
            return data
        elif table_name == "Collection":
            issn = input("Enter ISSN: ")
            name = input("Enter collection's name: ")
            typec = input("Enter collection's type: ")
            category = input("Enter collection's category: ")
            data = {
                "\"ISSN\"": issn,
                "\"Name\"": name,
                "\"Type\"": typec,
                "\"Category\"": category
            }
            return data
        elif table_name == "Publishing":
            authorid = input("Enter AuthorID: ")
            pid = input("Enter PublicationID: ")
            issn = input("Enter ISSN: ")
            date = input("Enter Date: ")
            data = {
                "\"AuthorID\"": authorid,
                "\"PublicationID\"": pid,
                "\"ISSN\"": issn,
                "\"Date\"": date
            }
            return data

    def get_update_input(self, table_name, pk):
        if table_name == "Author":
            authorid = pk
            name = input("Enter author's Name: ")
            surname = input("Enter author's Surname: ")
            data = {
                "\"AuthorID\"": authorid,
                "\"Name\"": name,
                "\"Surname\"": surname
            }
            return data
        elif table_name == "Publication":
            pid = pk
            name = input("Enter publication's name: ")
            language = input("Enter language: ")
            field = input("Enter field: ")
            pages = input("Enter pages: ")
            data = {
                "\"PublicationID\"": pid,
                "\"Name\"": name,
                "\"Language\"": language,
                "\"Field\"": field,
                "\"Pages\"": pages
            }
            return data
        elif table_name == "Collection":
            issn = pk
            name = input("Enter collection's name: ")
            typec = input("Enter collection's type: ")
            category = input("Enter collection's category: ")
            data = {
                "\"ISSN\"": issn,
                "\"Name\"": name,
                "\"Type\"": typec,
                "\"Category\"": category
            }
            return data

    def get_task_id(self):
        return int(input("Enter task ID: "))

    def get_pk(self, table_name):
        if table_name == "Author":
            return "AuthorID", input("Enter AuthorID: ")
        elif table_name == "Publication":
            return "PublicationID", input("Enter PublicationID: ")
        elif table_name == "Collection":
            return "ISSN", int(input("Enter ISSN: "))
        elif table_name == "Publishing":
            return "AuthorID", input("Enter AuthorID: "), "PublicationID", input("Enter PublicationID: "), "ISSN", int(input("Enter ISSN: "))

    def show_message(self, message):
        print(message)

    def show_menu_options(self, table_name):
        self.show_message("\nMenu:")
        self.show_message("1. Add Task")
        self.show_message("2. View Tasks")
        if not table_name == "Publishing": self.show_message("3. Update Task")
        self.show_message("4. Delete Task")
        self.show_message("5. Generate data")
        self.show_message("6. Back")
        return input("Enter your choice: ")

    def show_main_menu(self):
        self.show_message("\nWelcome! Which table you want to work with?")
        self.show_message("1. Author")
        self.show_message("2. Publication")
        self.show_message("3. Collection")
        self.show_message("4. Publishing")
        self.show_message("5. Queries")
        self.show_message("6. Quit")
        return input("Enter your choice: ")

    def show_queries(self):
        self.show_message("\nChose query:")
        self.show_message("1. Show authors and publications by field and language")
        self.show_message("2. Show authors and the number of publications in the category")
        self.show_message("3. Show the number of publications by language in the collection")
        self.show_message("4. Back")
        return input("Enter your choice: ")

    def get_num(self):
        return int(input("Enter number of data to generate: "))


    def show_q_choice_field(self):
        self.show_message("Choose field:")
        self.show_message("1. Medicine")
        self.show_message("2. Biology")
        self.show_message("3. Engineering")
        self.show_message("4. Economics")
        self.show_message("5. Physics")
        self.show_message("6. Chemistry")
        self.show_message("7. History")
        self.show_message("8. Philosophy")
        return int(input("Enter your choice: "))

    def show_q_choice_language(self):
        self.show_message("Choose language:")
        self.show_message("1. Ukrainian")
        self.show_message("2. English")
        self.show_message("3. Spanish")
        self.show_message("4. Croatian")
        self.show_message("5. Portuguese")
        self.show_message("6. French")
        return int(input("Enter your choice: "))

    def show_q_choice_category(self):
        self.show_message("Choose category:")
        self.show_message("1. A")
        self.show_message("2. B")
        self.show_message("3. C")
        return int(input("Enter your choice: "))

    def get_issn(self):
        return int(input("Input ISSN: "))