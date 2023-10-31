from model import Model
from view import View
import time

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self):
        while True:
            choice = self.view.show_main_menu()
            if choice == '1':
                self.run_options("Author")
            elif choice == '2':
                self.run_options("Publication")
            elif choice == '3':
                self.run_options("Collection")
            elif choice == '4':
                self.run_options("Publishing")
            elif choice == '5':
                self.run_queries()
            elif choice == '6':
                break

    def run_options(self, table_name):
        while True:
            choice = self.view.show_menu_options(table_name)
            if choice == '1':
                self.add(table_name)
            elif choice == '2':
                self.view_t(table_name)
            elif choice == '3' and not table_name == "Publishing":
                self.update(table_name)
            elif choice == '4':
                self.delete(table_name)
            elif choice == '5':
                self.generate_data(table_name)
            elif choice == '6':
                break

    def run_queries(self):
        while True:
            choice = self.view.show_queries()
            if choice == '1':
                self.run_q1()
            elif choice == '2':
                self.run_q2()
            elif choice == '3':
                self.run_q3()
            elif choice == '4':
                break

    def add(self, table_name):
        data = self.view.get_data_input(table_name)
        self.model.add_data(table_name, data)

    def update(self, table_name):
        cond_c, cond_v = self.view.get_pk(table_name)
        data = self.view.get_update_input(table_name, cond_v)
        self.model.update_data(table_name, data, cond_c, cond_v)

    def view_t(self, table_name):
        data = self.model.get_all(table_name)
        if table_name == "Author":
            self.view.show_author(data)
        elif table_name == "Publication":
            self.view.show_publication(data)
        elif table_name == "Collection":
            self.view.show_collection(data)
        else:
            self.view.show_publishing(data)

    def delete(self, table_name):
        if table_name == "Publishing":
            aid, val1, pid, val2, issn, val3 = self.view.get_pk(table_name)
            self.model.delete_data_publishing(table_name, aid, val1, pid, val2, issn, val3)
        else:
            pk, val = self.view.get_pk(table_name)
            self.model.delete_data(table_name, pk, val)

    def generate_data(self, table_name):
        num = self.view.get_num()
        self.model.generate_data(table_name, num)
        self.view.show_message("Generated successfully!")

    def run_q1(self):
        arr_l = ["ukrainian", "english", "spanish", "croatian", "portuguese", "french"]
        arr_f = ["medicine", "biology", "engineering", "economics", "physics", "chemistry", "history", "philosophy"]
        choice1 = self.view.show_q_choice_field()
        choice2 = self.view.show_q_choice_language()
        start_time = time.time()
        data = self.model.show_by_field_language(arr_f[choice1-1], arr_l[choice2-1])
        end_time = time.time()
        self.view.show_res_q1(data)
        execution_time_ms = (end_time - start_time) * 1000
        print(f"Execution time: {execution_time_ms} ms")

    def run_q2(self):
        arr_c = ["A", "B", "C"]
        choice = self.view.show_q_choice_category()
        start_time = time.time()
        data = self.model.show_by_category(arr_c[choice - 1])
        end_time = time.time()
        self.view.show_res_q2(data)
        execution_time_ms = (end_time - start_time) * 1000
        print(f"Execution time: {execution_time_ms} ms")

    def run_q3(self):
        issn = self.view.get_issn()
        start_time = time.time()
        data = self.model.show_collection(issn)
        end_time = time.time()
        self.view.show_res_q3(data)
        execution_time_ms = (end_time - start_time) * 1000
        print(f"Execution time: {execution_time_ms} ms")
