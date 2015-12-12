import MySQLdb
import datetime


class Canvas:
    def __init__(self):
        self.db = MySQLdb.connect(host='localhost',
                                db='project3-nudb',
                                user='root',
                                passwd='189154yzj')
        if self.db.open:
            print('Connected to MySQL database')
        self.db.autocommit(True) # open to right to update statement
        self.login()

    def login(self):
        studID = raw_input("studentID: ")
        password = raw_input("password: ")
        self.cur = self.db.cursor()
        self.cur.execute("select * from student where Id = '%s' and Password = '%s'" % (studID, password))
        result = self.cur.fetchall()
        if len(result) != 0:
            print("successfully log in")
            self.studentMenu(studID)
        else:
            print("studentID or password is not correct.")
            self.login()

    def studentMenu(self, studID):
        now = datetime.datetime.now()
        self.year = now.year
        month = now.month
        if month in (9,10,11,12):
            self.quarter = "Q1"
        elif month in (1,2,3):
            self.quarter = "Q2"
        elif month in (4,5,6):
            self.quarter = "Q3"
        else:
            self.quarter = "Q4"
        self.cur.execute("select t.UoSCode, u.UoSName \
            from transcript as t, unitofstudy as u \
            where t.StudId = '%s' and t.Semester = '%s' and t.Year = '%s' \
              and Grade is null and u.uoscode = t.uoscode" % (studID, self.quarter, self.year))
        result_menu = self.cur.fetchall()
        for row in result_menu:
            print row
        self.Select(studID)

    def Select(self, studID):
        print ("sections you can enter: Transcript, Enroll, Withdraw, Personal Details and Logout")
        next = raw_input("select section: ")
        if next.lower() == "transcript":
            self.Transcript(studID)
        elif next.lower() == "enroll":
            self.Enroll(studID)
        elif next.lower() == "withdraw":
            self.Withdraw(studID)
        elif next.lower() == "personal details":
            self.PersonDetail(studID)
        elif next.lower() == "logout":
            self.cur.close()
            self.login()
        else:
            print("no such section. please select again.")
            self.Select(studID)

    def Transcript(self, studID):
        self.cur.execute("select * from transcript where studid = '%s'" % studID)
        result = self.cur.fetchall()
        for raw in result:
            print raw
        self.transcript_sub(studID)

    def transcript_sub(self, studID):
        sub = raw_input("details or go back: ")
        if sub == 'details':
            num = raw_input("code of course you want to see: ")
            self.cur.execute("select u.uoscode, u.uosname, t.semester, t.year, uo.enrollment, uo.maxenrollment, f.name, t.grade\
                        from unitofstudy u, transcript t, uosoffering uo, faculty f \
                        where u.uoscode = '%s' and t.uoscode = '%s' and t.studid = '%s' and  uo.uoscode ='%s' and \
                        t.semester = uo.semester and t.year = uo.year and \
                        uo.instructorid = f.id" % (num, num, studID, num))
            result = self.cur.fetchall()
            for raw in result:
                print raw
            self.transcript_sub(studID)
        elif sub == 'go back':
            self.studentMenu(studID)
        else:
            print("action is not allowed")
            self.transcript_sub(studID)

    def Enroll(self, studID):
        if self.quarter == 'Q1':
            nextquarter = 'Q2'
            enrollyear = self.year + 1
        elif self.quarter == 'Q2':
            nextquarter = 'Q3'
            enrollyear = self.year
        elif self.quarter == 'Q3':
            nextquarter = 'Q4'
            enrollyear = self.year
        else:
            nextquarter = 'Q1'
            enrollyear = self.year
        self.cur.execute("select * from lecture where semester = '%s' and year = '%s'" % (self.quarter, self.year))
        current = self.cur.fetchall()
        print "course offered this quarter: "
        for raw in current:
            print raw
        self.cur.execute("select * from lecture where semester = '%s' and year = '%s'" % (nextquarter, enrollyear))
        nextenroll = self.cur.fetchall()
        print "courses offerred next quarter: "
        for raw in nextenroll:
            print raw
        enrollnum = raw_input("choose the course code you want to enroll or go back: ")
        if enrollnum == 'go back':
            self.studentMenu(studID)
        else:
            self.cur.close()
            self.cur = self.db.cursor()
            self.cur.execute("call enroll_try(%s,%s,%s,%s,%s,%s)", (enrollnum, self.quarter, self.year, nextquarter, enrollyear, studID))
            rresult = self.cur.fetchall()
            # self.cur.close()
            # self.cur = self.db.cursor()
            if len(rresult) != 0:
                if str(rresult[0][0][0:8]) == str(enrollnum):
                    print("already taken this course")
                else:
                    print("need prerequisits: ")
                    print rresult
                nextdo = raw_input("enroll or go back: ")
                if nextdo == "enroll":
                    self.cur.close()
                    self.cur = self.db.cursor()
                    self.Enroll(studID)
                else:
                    self.cur.close()
                    self.cur = self.db.cursor()
                    self.studentMenu(studID)
            else:
                print("successfully enroll")
                nextdo = raw_input("enroll or go back: ")
                if nextdo == "enroll":
                    self.Enroll(studID)
                else:
                    self.studentMenu(studID)

    def Withdraw(self, studID):
        self.cur.execute("select * from transcript where studid = '%s' and grade is null" % studID)
        result = self.cur.fetchall()
        for raw in result:
            print raw
        self.withdraw_sub(studID)

    def withdraw_sub(self, studID):
        draw = raw_input("course code you want to withdraw or go back: ")
        if draw == "go back":
            self.studentMenu(studID)
        else:
            self.cur.execute("call withdraw(%s,%s,%s,%s)", (studID, draw, self.quarter, self.year))
            result = self.cur.fetchall()
            for row in result:
                print row
            if len(result) != 0:
                print("withdraw successfully")
                self.cur.close()
                self.cur = self.db.cursor()
                self.cur.execute("select * from student where id = '0'")
                check = self.cur.fetchall()
                if len(check) != 0:
                    print ("enroll student is below requirement")
                    self.cur.execute("delete from student where id = '0'")
                self.Withdraw(studID)
            else:
                print("not allowed")
                self.Withdraw(studID)

    def PersonDetail(self, studID):
        self.cur.execute("select id, name, address from student where id = '%s'" % studID)
        result = self.cur.fetchall()
        print ("student ID: %d" % result[0][0])
        print("student name: %s" % result[0][1])
        print("student address: %s" % result[0][2])
        self.change(studID)

    def change(self, studID):
        next = raw_input("please enter 'password' or 'address' to change your password or address or 'logout' or 'go back': ")
        if next == 'password':
            new = raw_input("new password: ")
            flagp = raw_input("submission (Y or N) :")
            if flagp == 'Y':
                self.cur.execute("update student set password = '%s' where id = '%s'" % (new, studID))
                print ("password is updated")
                self.change(studID)
            else:
                self.change(studID)
        elif next == 'address':
            new = raw_input("new address: ")
            flaga = raw_input("submission (Y or N): ")
            if flaga == 'Y':
                self.cur.execute("update student set address = '%s' where id = '%s'" % (new, studID))
                print("address is updated")
                self.change(studID)
            else:
                self.change(studID)
        elif next == 'logout':
            self.cur.close()
            self.login()
        elif next == 'go back':
            self.studentMenu(studID)
        else:
            print("action is not allowed")
            self.change(studID)