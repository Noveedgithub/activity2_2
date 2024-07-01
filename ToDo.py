import unittest
import sqlite3

# Function to create a connection to the SQLite database
def create_connection(db_file=':memory:'):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    return conn, c

# Function to create the tasks table
def create_table(c, conn):
    c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        task TEXT NOT NULL,
        status TEXT NOT NULL
    )
    ''')
    conn.commit()

# Function to add a task
def add_task(c, conn, task):
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
    
# Function to mark a task as completed
def mark_task_completed(c, conn, task_id):
    c.execute('UPDATE tasks SET status = ? WHERE id = ?', ('completed', task_id))
    conn.commit()
    print(f"Task {task_id} marked as completed.")
    
# Function to update a task
def update_task(c, conn, task_id, new_task):
    c.execute('UPDATE tasks SET task = ? WHERE id = ?', (new_task, task_id))
    conn.commit()
    print(f"Task {task_id} updated successfully.")

# Unit tests for the to-do list application
class TestToDoApp(unittest.TestCase):

    def setUp(self):
        self.conn, self.c = create_connection(':memory:')  # Use in-memory database for testing
        create_table(self.c, self.conn)

    def tearDown(self):
        self.conn.close()

    def test_add_task(self):
        add_task(self.c, self.conn, "Test Task 1")
        tasks = view_tasks(self.c)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][1], "Test Task 1")
        self.assertEqual(tasks[0][2], "pending")

    def test_view_tasks(self):
        add_task(self.c, self.conn, "Test Task 1")
        add_task(self.c, self.conn, "Test Task 2")
        tasks = view_tasks(self.c)
        self.assertEqual(len(tasks), 2)
        
    def test_mark_task_completed(self):
        add_task(self.c, self.conn, "Test Task 1")
        tasks = view_tasks(self.c)
        task_id = tasks[0][0]
        mark_task_completed(self.c, self.conn, task_id)
        tasks = view_tasks(self.c)
        self.assertEqual(tasks[0][2], "completed")

    def test_update_task(self):
        add_task(self.c, self.conn, "Test Task 1")
        tasks = view_tasks(self.c)
        task_id = tasks[0][0]
        update_task(self.c, self.conn, task_id, "Updated Task 1")
        tasks = view_tasks(self.c)
        self.assertEqual(tasks[0][1], "Updated Task 1")
        
if __name__ == '__main__':
    # Run the tests
    unittest.main(exit=False)
