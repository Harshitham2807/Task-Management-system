import mysql.connector
from datetime import datetime
from typing import Tuple

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="harshitha28",  
    database="task_db"
)
cursor = connection.cursor()

STATUS_FLOW = {
    "Pending": "InProgress",
    "InProgress": "Completed"
}

def create_user():
    name = input("Enter user name: ")
    email = input("Enter user email: ")
    cursor.execute("INSERT INTO User (Name, Email) VALUES (%s, %s)", (name, email))
    connection.commit()
    print("User created.")

def view_users():
    cursor.execute("SELECT * FROM User")
    users = cursor.fetchall()
    for user in users:
        print(user)

def get_user_by_id():
    user_id = int(input("Enter user ID: "))
    cursor.execute("SELECT * FROM User WHERE Id = %s", (user_id,))
    user = cursor.fetchone()
    print(user if user else " User not found.")

def update_user():
    user_id = int(input("Enter user ID to update: "))
    name = input("Enter new name (leave blank to skip): ")
    email = input("Enter new email (leave blank to skip): ")

    updates = []
    params = []

    if name:
        updates.append("Name = %s")
        params.append(name)
    if email:
        updates.append("Email = %s")
        params.append(email)

    if not updates:
        print(" No updates provided.")
        return

    query = f"UPDATE User SET {', '.join(updates)} WHERE Id = %s"
    params.append(user_id)
    cursor.execute(query, tuple(params))
    connection.commit()
    print(" User updated.")

def delete_user():
    user_id = int(input("Enter user ID to delete: "))
    cursor.execute("DELETE FROM User WHERE Id = %s", (user_id,))
    connection.commit()
    print("User deleted.")


def validate_due_date(due_date: datetime) -> bool:
    return due_date > datetime.now()

def create_task():
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    status = input("Enter status (Pending/InProgress/Completed): ")
    priority = input("Enter priority (Low/Medium/High): ")
    due_date_str = input("Enter due date (YYYY-MM-DD HH:MM): ")
    user_id = int(input("Assign to user ID: "))

    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
    except ValueError:
        print(" Invalid date format.")
        return

    if not validate_due_date(due_date):
        print("Due date must be in the future.")
        return

    cursor.execute("""
        INSERT INTO TaskItem (Title, Description, Status, Priority, DueDate, UserId)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (title, description, status, priority, due_date, user_id))
    connection.commit()
    print("Task created.")

def view_tasks():
    cursor.execute("""
        SELECT t.Id, t.Title, t.Status, t.Priority, t.DueDate, u.Name AS UserName
        FROM TaskItem t
        LEFT JOIN User u ON t.UserId = u.Id
    """)
    tasks = cursor.fetchall()
    for task in tasks:
        print(task)

def get_task_by_id():
    task_id = int(input("Enter task ID: "))
    cursor.execute("SELECT * FROM TaskItem WHERE Id = %s", (task_id,))
    task = cursor.fetchone()
    print(task if task else "Task not found.")

def get_tasks_by_user():
    user_id = int(input("Enter user ID: "))
    cursor.execute("SELECT * FROM TaskItem WHERE UserId = %s", (user_id,))
    tasks = cursor.fetchall()
    if tasks:
        for task in tasks:
            print(task)
    else:
        print(" No tasks found for this user.")

def filter_tasks():
    status = input("Filter by status (leave blank to skip): ")
    priority = input("Filter by priority (leave blank to skip): ")
    date_start = input("Start due date (YYYY-MM-DD, leave blank to skip): ")
    date_end = input("End due date (YYYY-MM-DD, leave blank to skip): ")

    query = "SELECT * FROM TaskItem WHERE 1=1"
    params = []

    if status:
        query += " AND Status = %s"
        params.append(status)
    if priority:
        query += " AND Priority = %s"
        params.append(priority)
    if date_start and date_end:
        try:
            start = datetime.strptime(date_start, "%Y-%m-%d")
            end = datetime.strptime(date_end, "%Y-%m-%d")
            query += " AND DueDate BETWEEN %s AND %s"
            params.extend([start, end])
        except ValueError:
            print(" Invalid date format.")
            return

    cursor.execute(query, tuple(params))
    for task in cursor.fetchall():
        print(task)

def sort_tasks():
    sort_by = input("Sort by (DueDate/Priority): ")
    if sort_by not in ["DueDate", "Priority"]:
        print(" Invalid sort key.")
        return
    cursor.execute(f"SELECT * FROM TaskItem ORDER BY {sort_by}")
    for task in cursor.fetchall():
        print(task)

def update_task_status():
    task_id = int(input("Enter task ID: "))
    new_status = input("Enter new status: ")

    cursor.execute("SELECT Status FROM TaskItem WHERE Id = %s", (task_id,))
    result = cursor.fetchone()
    if not result:
        print(" Task not found.")
        return

    current_status = result['Status']
    allowed_next = STATUS_FLOW.get(current_status)

    if allowed_next != new_status:
        print(f" Invalid transition: {current_status} → {new_status}")
        return

    cursor.execute("UPDATE TaskItem SET Status = %s WHERE Id = %s", (new_status, task_id))
    connection.commit()
    print(" Status updated.")

def delete_task():
    task_id = int(input("Enter task ID to delete: "))
    cursor.execute("DELETE FROM TaskItem WHERE Id = %s", (task_id,))
    connection.commit()
    print(" Task deleted.")



def main():
    while True:
        print("\n Task Management System")
        print("1. Create User")
        print("2. View All Users")
        print("3. Get User by ID")
        print("4. Update User")
        print("5. Delete User")
        print("6. Create Task")
        print("7. View All Tasks")
        print("8. Get Task by ID")
        print("9. Get Tasks for a User")
        print("10. Filter Tasks")
        print("11. Sort Tasks")
        print("12. Update Task Status")
        print("13. Delete Task")
        print("0. Exit")

        choice = input("Select an option: ")

        try:
            if choice == "1":
                create_user()
            elif choice == "2":
                view_users()
            elif choice == "3":
                get_user_by_id()
            elif choice == "4":
                update_user()
            elif choice == "5":
                delete_user()
            elif choice == "6":
                create_task()
            elif choice == "7":
                view_tasks()
            elif choice == "8":
                get_task_by_id()
            elif choice == "9":
                get_tasks_by_user()
            elif choice == "10":
                filter_tasks()
            elif choice == "11":
                sort_tasks()
            elif choice == "12":
                update_task_status()
            elif choice == "13":
                delete_task()
            elif choice == "0":
                print(" Exiting...")
                break
            else:
                print(" Invalid option.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
connection.close()