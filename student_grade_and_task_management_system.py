import pickle, os, heapq
from datetime import datetime

class Grade:
    def __init__(self, subject, marks, max_marks, semester):
        self.subject, self.marks, self.max_marks, self.semester = subject, marks, max_marks, semester
        
    def get_percentage(self):
        return (self.marks / self.max_marks) * 100 if self.max_marks > 0 else 0
    
    def get_letter_grade(self):
        p = self.get_percentage()
        return 'A+' if p>=90 else 'A' if p>=80 else 'B+' if p>=70 else 'B' if p>=60 else 'C' if p>=50 else 'D' if p>=40 else 'F'

class Student:
    def __init__(self, student_id, name, roll_no, email):
        self.student_id, self.name, self.roll_no, self.email = student_id, name, roll_no, email
        self.grades = []
        
    def add_grade(self, subject, marks, max_marks, semester):
        self.grades.append(Grade(subject, marks, max_marks, semester))
        
    def calculate_gpa(self):
        if not self.grades: return 0.0
        return round((sum(g.get_percentage() for g in self.grades) / len(self.grades)) / 10, 2)

class Task:
    PRIORITY_MAP = {'high': 1, 'medium': 2, 'low': 3}
    def __init__(self, task_id, title, desc, priority, deadline, student_id):
        self.task_id, self.title, self.desc = task_id, title, desc
        self.priority, self.deadline, self.student_id = priority, deadline, student_id
        self.status, self.created_at = 'pending', datetime.now()
        
    def __lt__(self, other):
        return self.PRIORITY_MAP[self.priority] < self.PRIORITY_MAP[other.priority]
    
    def is_overdue(self):
        try: return datetime.now() > datetime.strptime(self.deadline, '%Y-%m-%d') and self.status != 'completed'
        except: return False

class System:
    def __init__(self, file='data.pkl'):
        self.file = file
        self.students, self.tasks, self.task_queue = {}, [], []
        if os.path.exists(self.file):
            try:
                with open(self.file, 'rb') as f:
                    data = pickle.load(f)
                    self.students, self.tasks = data.get('students', {}), data.get('tasks', [])
                    self.task_queue = [t for t in self.tasks if t.status == 'pending']
                    heapq.heapify(self.task_queue)
            except: print("Error loading data.")

    def save(self):
        with open(self.file, 'wb') as f: pickle.dump({'students': self.students, 'tasks': self.tasks}, f)

    def add_student(self, name, roll, email):
        if any(s.roll_no == roll for s in self.students.values()):
            print("Roll number exists."); return
        sid = f"STU{len(self.students)+1:04d}"
        self.students[sid] = Student(sid, name, roll, email)
        self.save(); print(f"Student {sid} added.")

    def delete_student(self, sid):
        if sid in self.students:
            del self.students[sid]
            self.tasks = [t for t in self.tasks if t.student_id != sid]
            self.task_queue = [t for t in self.tasks if t.status == 'pending']
            heapq.heapify(self.task_queue)
            self.save(); print("Deleted.")
        else: print("Not found.")

    def update_student(self, sid, name, roll, email):
        if sid in self.students:
            s = self.students[sid]
            if name: s.name = name
            if roll: s.roll_no = roll
            if email: s.email = email
            self.save(); print("Updated.")

    def add_grade(self, sid, sub, mrk, mx, sem):
        if sid in self.students:
            self.students[sid].add_grade(sub, mrk, mx, sem)
            self.save(); print("Grade added.")
        else: print("Student not found.")

    def view_student(self, sid):
        if sid not in self.students: print("Not found."); return
        s = self.students[sid]
        print(f"\nID: {s.student_id} | Name: {s.name} | GPA: {s.calculate_gpa()}")
        for g in s.grades: print(f"{g.subject}: {g.marks}/{g.max_marks} ({g.get_letter_grade()})")
        print("Tasks:", len([t for t in self.tasks if t.student_id == sid]))

    def add_task(self, title, desc, prio, due, sid):
        if sid not in self.students: print("Student not found."); return
        tid = f"TSK{len(self.tasks)+1:04d}"
        t = Task(tid, title, desc, prio, due, sid)
        self.tasks.append(t)
        heapq.heappush(self.task_queue, t)
        self.save(); print(f"Task {tid} added.")

    def complete_task(self, tid):
        t = next((x for x in self.tasks if x.task_id == tid), None)
        if t:
            t.status = 'completed'
            self.task_queue = [x for x in self.tasks if x.status == 'pending']
            heapq.heapify(self.task_queue)
            self.save(); print("Task completed.")

    def delete_task(self, tid):
        self.tasks = [t for t in self.tasks if t.task_id != tid]
        self.task_queue = [t for t in self.tasks if t.status == 'pending']
        heapq.heapify(self.task_queue)
        self.save(); print("Deleted.")

    def view_tasks(self, status=None):
        ts = [t for t in self.tasks if t.status == status] if status else self.tasks
        for t in sorted(ts, key=lambda x: x.PRIORITY_MAP[x.priority]):
            print(f"[{t.status[0].upper()}] {t.task_id} ({t.priority}): {t.title} - Due: {t.deadline}")

    def next_task(self):
        if self.task_queue:
            t = self.task_queue[0]
            print(f"NEXT: {t.title} ({t.priority}) due {t.deadline} for {self.students[t.student_id].name}")
        else: print("No pending tasks.")

    def report(self):
        print(f"Total Students: {len(self.students)}")
        if self.students:
            avg = sum(s.calculate_gpa() for s in self.students.values())/len(self.students)
            print(f"Class Avg GPA: {avg:.2f}")
        print(f"Tasks: {len(self.tasks)} Total, {len(self.task_queue)} Pending")

def main():
    sys = System()
    while True:
        print("\n1.Add Stu 2.List Stu 3.View Stu 4.Upd Stu 5.Del Stu")
        print("6.Add Grd 7.Add Tsk 8.View Tsk 9.Done Tsk 10.Del Tsk 11.Nxt Tsk 12.Rpt 13.Exit")
        ch = input("Choice: ")
        if ch=='1': sys.add_student(input("Name: "), input("Roll: "), input("Email: "))
        elif ch=='2': 
            for s in sys.students.values(): print(f"{s.student_id}: {s.name} (GPA: {s.calculate_gpa()})")
        elif ch=='3': sys.view_student(input("ID: "))
        elif ch=='4': sys.update_student(input("ID: "), input("Name: ") or None, input("Roll: ") or None, input("Email: ") or None)
        elif ch=='5': sys.delete_student(input("ID: "))
        elif ch=='6': 
            try: sys.add_grade(input("ID: "), input("Sub: "), float(input("Mk: ")), float(input("Max: ")), input("Sem: "))
            except: print("Invalid inputs")
        elif ch=='7': sys.add_task(input("Title: "), input("Desc: "), input("Prio(high/medium/low): "), input("Due(YYYY-MM-DD): "), input("ID: "))
        elif ch=='8': sys.view_tasks(input("Filter (pending/completed/enter for all): ") or None)
        elif ch=='9': sys.complete_task(input("Task ID: "))
        elif ch=='10': sys.delete_task(input("Task ID: "))
        elif ch=='11': sys.next_task()
        elif ch=='12': sys.report()
        elif ch=='13': break
        else: print("Invalid.")

if __name__ == "__main__": main()
