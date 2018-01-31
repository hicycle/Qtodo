import sqlite3


def transaction(sql, db='tasks.sqlite'):
    conn = sqlite3.connect(db)
    results = None
    try:
        cursor = conn.execute(sql)
        results = cursor.fetchall()
    except Exception:
        conn.rollback()
    conn.commit()
    conn.close()
    return results


class DbOperation:
    def __init__(self, task):
        self.task_content = task.task_content
        self.task_date = task.task_date
        self.taskid = task.taskid

    @staticmethod
    def addTask(task_content, task_date):
        return transaction(
            "INSERT INTO TASKS (ID,TASK,DATE) VALUES (null, '%s', %f)" % (task_content, task_date))

    @staticmethod
    def queryTask(done=0):
        return transaction("SELECT * FROM TASKS WHERE DONE=%d" % done)

    @staticmethod
    def queryNewTask():
        return transaction("SELECT * FROM TASKS ORDER BY ID DESC LIMIT 1")[0]

    def updateTask(self):
        return transaction("UPDATE TASKS SET TASK = '%s', DATE = '%f' WHERE ID = %d;" % (
            self.task_content, self.task_date, self.taskid))

    def delTask(self):
        return transaction("DELETE FROM TASKS WHERE ID = %d;" % self.taskid)

    def doneTask(self):
        return transaction("UPDATE TASKS SET DONE = 1 WHERE ID = %d;" % self.taskid)
