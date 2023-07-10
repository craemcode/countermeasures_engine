
from app.model import engine, Vulnerability, VulnTree, Children, Countermeasure
from app.vulnerability_tree import VulnerabilityTree
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.vulnerabilityNode import VulNode

#import csv
# from pyfiglet import Figlet


def welcome_menu():
    # pretty_print = Figlet(font='larry3d')
    # print(pretty_print.renderText("C-Engine"))
    print('Welcome to the smart countermeasures engine\n\n')
    print('Option 1: Make a vulnerability tree\n'
          'Option 2: Show vulnerability relationships\n'
          'Option 3: Provide a Description\n'
          'Option 4: Show Countermeasures for a vulnerability'
          'Option 5: Exit from the Program')
    true = True

    while true:
        print("MAIN MENU.\n Choose Option ")
        choice = input()
        if choice == "1":
            try:
                store_tree_to_db()
            except Exception as e:
                print(f'F1 Error: {e}')
        elif choice == "2":
            try:
                show_tree_from_db()
            except Exception as e:
                print(f'F2 Error: {e}')
        elif choice == "3":
            try:
                show_description()
            except Exception as e:
                print(f'F3 Error: {e}')
        elif choice == "4":
            try:
                show_countermeasure()
            except Exception as e:
                print(f'F3 Error: {e}')
        elif choice == 'Exit' or 'EXIT':
            print("Thankyou for choosing the countermeasures engine !")
            true = False


"""
session = Session(engine)


def add_records():
    file = open('new_data_frame.csv')
    csv_reader = csv.reader(file)

    test_pool = []
    for line in csv_reader:
        test = Vulnerability(
                id=line[1],
                description=line[2],
        )
        test_pool.append(test)

    try:
        session.add_all(test_pool)
        session.commit()
        session.close()
        print("SUCCESS!")
    except Exception as e:
        session.close()
        print(f'Error: {e} happened')

"""
"""
I want to do all the database operations in this file because of complications with the session object.
This database operation class will accept requests from functions in the vulnerability tree and nodes to act
as infrays into the table.
"""


class DatabaseOperations:
    session = Session(engine)

    def __init__(self):
        ...

    def __enter__(self):
        return self

    @classmethod
    def get_vuln(cls, message):
        print(f'{message}')
        vuln = input()
        c_vuln = vuln.rstrip()
        try:
            statement = select(Vulnerability).where(Vulnerability.id == c_vuln)
            record = cls.session.scalars(statement).one()
            return record
        except Exception as e:
            print(f'Error: {e}')

    @classmethod
    def get_tree(cls, message):
        print(f'{message}')
        tree = input()
        c_tree = tree.rstrip()
        try:
            statement = select(VulnTree).where(VulnTree.root_node == c_tree)
            record = cls.session.scalars(statement).one()
            return record
        except Exception as e:
            print(f'Error {e}')

    @classmethod
    def get_tree_id(cls, root_id):
        try:
            statement = select(VulnTree).where(VulnTree.root_node == root_id)
            record = cls.session.scalars(statement).one()
            return record.id
        except Exception as e:
            print(f'Error {e}')

    @classmethod
    def store_tree(cls, tree):
        ftree = VulnTree(
            root_node=tree.root.id
        )
        try:
            cls.session.add(ftree)
            cls.session.commit()
            print("Tree successfully stored!")
        except Exception as e:
            print(f'Error: {e} ')

    @classmethod
    def get_children(cls, tree):
        try:
            statement = select(Children).where(Children.tree_id == tree.id)
            records = cls.session.scalars(statement).all()
            return records
        except Exception as e:
            print(f'Error: {e}')

    @classmethod
    def store_children(cls, tree_id, children):

        pool = []
        for child in children:
            chld = Children(
                my_id=child.id,
                tree_id=tree_id,
                parent_id=child.parent,
                edu_complexity=child.education_value
            )
            pool.append(chld)

        try:
            cls.session.add_all(pool)
            cls.session.commit()
            print("Children successfully stored!")
        except Exception as e:
            print(f'Error: {e} ')

    @classmethod
    def store_countermeasure(cls, node):
        countermeasure = Countermeasure(
            text=node.countermeasure,
            vuln_id=node.id
        )
        try:
            cls.session.add(countermeasure)
            cls.session.commit()
            print("Countermeasures successfully stored!")
        except Exception as e:
            print(f'Error {e} happened')

    @classmethod
    def get_countermeasure(cls, vuln_id):
        try:
            statement = select(Countermeasure).where(Countermeasure.vuln_id == vuln_id)
            record = cls.session.scalars(statement).one()
            return record
        except Exception as e:
            print(f'Error: {e} happened.')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


def create_node(message):
    db = DatabaseOperations()
    with db:
        record = db.get_vuln(message)

    node = VulNode()
    node.id = record.id


    return node


def make_tree():
    """This function makes the vulnerability tree using nodes"""

    root = create_node("Enter CVE for root node:")
    education_input = int(input("Enter Educational complexity for root node\n"))
    root.education_value = education_input
    measure_txt = input("Enter Countermeasure for Root Node\n")
    root.countermeasure = measure_txt

    tree = VulnerabilityTree(root)

    add_more = True
    while add_more:
        begin = input("Press any button to begin. Press Exit to quit:")
        if begin == 'Exit':
            break

        child = create_node("Enter CVE for child node:")
        education_input = int(input("Enter Educational complexity for node \n"))
        child.education_value = education_input
        measure_txt = input("Enter Countermeasure for Node\n")
        child.countermeasure = measure_txt
        parent = input("Enter Parent ID\n")
        child.parent = parent.rstrip()

        tree.add_node(child)
        # this part of the code is used for stopping the program..or continuing

        option = input('Do you want to add another child? Y/N:')

        if option == 'N':
            return tree
        elif option == 'Y':
            continue

    return tree


def store_tree_to_db():
    tree = make_tree()
    items = tree.nodes

    with DatabaseOperations() as db:
        db.store_tree(tree)
        tree_id = db.get_tree_id(tree.root.id)
        db.store_children(tree_id, items)

        for node in tree.nodes:
            db.store_countermeasure(node)


def show_tree_from_db():
    try:
        with DatabaseOperations() as db:
            tree = db.get_tree("Enter the CVE for the root node of a vulnerability tree")
            children = db.get_children(tree)
            root = children[0] #first element

        tot = 0
        print(f'The root vulnerability is {root.my_id} with complexity {root.edu_complexity}')
        for child in children[1::]:
            print(f'\t Exploit {child.parent_id} through {child.my_id} with education complexity {child.edu_complexity}')
            tot += child.edu_complexity
        average = (tot+root.edu_complexity)/len(children)
        print(f'Average Complexity: {abs(average)}')
    except Exception as e:
        print(f'Error {e} happened')


def show_description():

    prompt = "Enter CVE which you want to see countermeasures. Press Exit to quit\n"
    try:
        with DatabaseOperations() as db:
            record = db.get_vuln(prompt)
            print(f'Vulnerability: { record.id}\n Description: { record.description}')
    except Exception as e:
        print(f'Error {e} happened')


def show_countermeasure():
    show = True
    while show:
        prompt = input("Enter CVE which you want to see countermeasures. Press Exit to quit \n")
        if prompt == 'Exit':
            show = False
        else:
            c_prompt = prompt.rstrip()
            with DatabaseOperations() as db:
                counterm = db.get_countermeasure(c_prompt)
                print(f'Vulnerability\t\tCountermeasure\n'
                      f'{counterm.vuln_id}\t\t{counterm.text}\n')


if __name__ == '__main__':
    welcome_menu()
