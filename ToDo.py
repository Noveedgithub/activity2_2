import unittest
import sqlite3

def create_connection(db_file=':memory:'):      # Function to create a connection to the SQLite database
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    return conn, c

def create_table(c, conn):                      # Function to create the tasks table
    c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        task TEXT NOT NULL,
        status TEXT NOT NULL
    )
    ''')
    conn.commit()

def add_task(c, conn, task):                    # Function to add a task
    c.execute('INSERT INTO tasks (task, status) VALUES (?, ?)', (task, 'pending'))
    conn.commit()
    print("Task added successfully.")

# Function to view all tasks
def view_tasks(c):
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    if tasks:
        return tasks
    else:
        return []
    
def mark_task_completed(c, conn, task_id):      # Function to mark a task as completed
    c.execute('UPDATE tasks SET status = ? WHERE id = ?', ('completed', task_id))
    conn.commit()
    print(f"Task {task_id} marked as completed.")
    
def update_task(c, conn, task_id, new_task):    # Function to update a task
    c.execute('UPDATE tasks SET task = ? WHERE id = ?', (new_task, task_id))
    conn.commit()
    print(f"Task {task_id} updated successfully.")
    
def delete_task(c, conn, task_id):              # Function to delete a task
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    print(f"Task {task_id} deleted successfully.")

def main():                                     # Main function to run the application (while loop)
    conn, c = create_connection()
    create_table(c, conn)
    
    while True:
        print("\nActivity 2.2 - To-Do App Menu")
        print("1. Add task")
        print("2. View tasks")
        print("3. Mark task as completed")
        print("4. Update task details")
        print("5. Delete task")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            task = input("Enter task description: ")
            add_task(c, conn, task)
        elif choice == '2':
            tasks = view_tasks(c)
            if tasks:
                for task in tasks:
                    print(f"ID: {task[0]}, Task: {task[1]}, Status: {task[2]}")
            else:
                print("No tasks found.")
        elif choice == '3':
            task_id = int(input("Enter task ID to mark as completed: "))
            mark_task_completed(c, conn, task_id)
        elif choice == '4':
            task_id = int(input("Enter task ID to update: "))
            new_task = input("Enter new task description: ")
            update_task(c, conn, task_id, new_task)
        elif choice == '5':
            task_id = int(input("Enter task ID to delete: "))
            delete_task(c, conn, task_id)
        elif choice == '6':
            print("\nThank you for using the Activity 2.2 - To-Do App\n")
            break
        else:
            print("Invalid choice. Please try again.")

    conn.close()
class TestToDoApp(unittest.TestCase):

    def setUp(self):
        self.conn, self.c = create_connection(':memory:')  # Use in-memory database for testing
        create_table(self.c, self.conn)

    def tearDown(self):
        self.conn.close()

    def test_add_task(self):                               # Add task test
        add_task(self.c, self.conn, "Test Task 1")
        tasks = view_tasks(self.c)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][1], "Test Task 1")
        self.assertEqual(tasks[0][2], "pending")

    def test_view_tasks(self):                              # view task test
        add_task(self.c, self.conn, "Test Task 1")
        add_task(self.c, self.conn, "Test Task 2")
        tasks = view_tasks(self.c)
        self.assertEqual(len(tasks), 2)
        
    def test_mark_task_completed(self):                     # Task marked as completed test
        add_task(self.c, self.conn, "Test Task 1")
        tasks = view_tasks(self.c)
        task_id = tasks[0][0]
        mark_task_completed(self.c, self.conn, task_id)
        tasks = view_tasks(self.c)
        self.assertEqual(tasks[0][2], "completed")

    def test_update_task(self):                             # Update task test
        add_task(self.c, self.conn, "Test Task 1")
        tasks = view_tasks(self.c)
        task_id = tasks[0][0]
        update_task(self.c, self.conn, task_id, "Updated Task 1")
        tasks = view_tasks(self.c)
        self.assertEqual(tasks[0][1], "Updated Task 1")
        
    def test_delete_task(self):                             # Delete task test
        add_task(self.c, self.conn, "Test Task 1")
        tasks = view_tasks(self.c)
        task_id = tasks[0][0]
        delete_task(self.c, self.conn, task_id)
        tasks = view_tasks(self.c)
        self.assertEqual(len(tasks), 0)
    
if __name__ == '__main__':
    unittest.main(exit=False)
    main()