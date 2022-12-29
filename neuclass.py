# Ben Tunney
# Test Semester Grades

import pymysql
host = 'localhost'
database = 'neu'

def connector(username, password):
    """
    Parameters
    ----------
    hostname : string
        user-input username
    password : string
        user-input password

    Returns
    -------
    cnx : connection
        pymysql connection

    """
    cnx = pymysql.connect(host= host, user = username,
                              password= password,
                          db= database, charset='utf8mb4', autocommit = True,
                              cursorclass=pymysql.cursors.DictCursor)
    return cnx

def error(e):
    # return nothing when invalid user/password error occurs
    print()
    print('Error: %d: %s' % (e.args[0], e.args[1]))
    return

def create(cnx):
    
    print()
    print()
    print()

    # use contreadtable to continue create commands until user prompts otherwise
    contreadtable = True
    while contreadtable == True:

        # get data
        name = input("NAME OF CLASS TO CREATE? ")
        year = input("WHAT YEAR (EX: 2022-2023)? ")
        semester = input("SEMESTER? ")
        grade = input("GRADE IN CLASS (EX: A, A-, B+?) ")
        creds = input("# OF CREDITS? ")

        # clean data
        name = name.lower()
        name = name.title()
        semester = semester.lower()
        semester = semester.title()
        grade = grade.lower()
        grade = grade.title()

        # make cursor and class create class procedure
        cursor = cnx.cursor()
        cursor.callproc("createClass",(name, year, semester, grade, creds ))
        
        # close first cursor
        cursor.close() 
        print()

        print("SUCCESSFUL CREATE")
        print()
        
        # prompt user to enter only y/n to continue loop
        valid = False
        while valid == False:
            print("WOULD YOU LIKE TO CREATE ANOTHER TUPLE?")
            tf = str(input("ENTER Y/N: ")).lower()
            if tf == "y":
                contreadtable = True
                break
            elif tf == "n":
                contreadtable = False
                print()
                print()
                print()
                break
            else:
                print("ERROR: PLEASE ENTER A VALID VALUE: Y/N")
                continue
                
            print()

def readQuery(query, cnx):

    # make cursor
    print()
    cur1 = cnx.cursor()
        
    # execute query for all data in table
    cur1.execute(query)

    # fetch all pairs
    rows = cur1.fetchall()
    
    # return dictionary of data
    for row in rows:
        print(row)
        print()
    
    # close first cursor
    cur1.close() 
    
    if not rows:
        print("NO AVAILABLE DATA IN THIS TABLE")
        
def tableread(cnx):

    # make cursor
    c = cnx.cursor()

    # get all classes
    query = "CALL readAllClass();"
    c.execute(query)
    rows = c.fetchall()

    lst = []

    # append all classes
    for course in rows:
        semlst = []
        for key in course:
            semlst.append(course[key])
        lst.append(semlst)

    # print all classes
    for row in range(len(lst)):
        print(lst[row])

    # close cursor
    c.close()
    print()
    print()
        
    # ask user if they want to read another table
    # reprompt user to enter valid if invalid
    valid = False
    while valid == False:
        print("WOULD YOU LIKE TO READ AGAIN?")
        tf = str(input("ENTER Y/N: ")).lower()
        if tf == "y":
            contreadtable = True
            break
        elif tf == "n":
            contreadtable = False
            print()
            print()
            print()
            break
        else:
            print("ERROR: PLEASE ENTER A VALID VALUE: Y/N")
            continue
            
        print()
        
    else:
        print()
        print()
        print()
        print()
        print()
        print("-------------------------------------------")
        print(" ERROR: PLEASE ENTER A VALID TABLE")
        print("-------------------------------------------")
        print()
        print()
        contreadtable = True
        
    return contreadtable

def queryread(cnx):

    # create cursor
    c = cnx.cursor()

    # get all semesters
    c.execute("SELECT DISTINCT year, semester FROM class")
    rows = c.fetchall()

    lst = []

    # append all sems
    for row in rows:
        semlst = []
        for x in row:
            semlst.append(row[x])
        lst.append(semlst)

    # close cursor
    c.close() 

    # print available semesters
    print("AVAILABLE SEMESTERS LIST:", lst)
    print()

    # get year and sem of interest
    year = input("WHAT YEAR WOULD YOU LIKE TO SEE GRADES FOR? ")
    sem = input("WHAT SEMESTER? ")
    sem = sem.lower()
    sem = sem.title()

    # make cursor
    cursor = cnx.cursor()
    cursor.callproc("readSemester",(year, sem))
    print()

    # get all classes for sem
    rows = cursor.fetchall()

    # print classes
    for row in rows:
        print(row)
        print()
    
    # close cursor
    cursor.close() 
    print()
    
    # ask user if they want to read another
    print()
    print()
    valid = False
    while valid == False:
        print("WOULD YOU LIKE TO READ AGAIN?")
        tf = str(input("ENTER Y/N: ")).lower()
        print()
        if tf == "y":
            contreadtable = True
            break
        elif tf == "n":
            contreadtable = False
            print()
            print()
            print()
            break
        else:
            print("ERROR: PLEASE ENTER A VALID VALUE: Y/N")
            continue
            
        print()
            
            
    # reprompt for valid table entry
    else:
        print()
        print()
        print()
        print("-------------------------------------------")
        print(" ERROR: PLEASE ENTER A VALID TABLE")
        print("-------------------------------------------")
        print()
        print()
        contreadtable = True
        
    return contreadtable
        
def read(cnx):
    
    # home for read operations
    print()
    print()
    print()
    
    # while loop to continue until user stops requesting reads
    contreadtable = True
    while contreadtable == True:
        print("WOULD YOU LIKE TO (1) READ ALL CLASSES ")
        print("                  (2) READ SPECIFIC SEMESTER")
        readchoice = int(input("ENTER 1 OR 2: "))
        
        if readchoice == 1:
            contreadtable = tableread(cnx)
        elif readchoice == 2:
            contreadtable = queryread(cnx)
        else:
            print()
            print()
            print()
            print("ERROR: PLEASE ENTER A VALID VALUE: 1 OR 2")
            print()
            continue
                 
def update(cnx):
    
    print()
    print()
    print()
    
    # prompt user with update options
    contreadtable = True
    while contreadtable == True:

        # create cursor
        c = cnx.cursor()

        # get all classes
        c.execute("SELECT name FROM class")
        rows = c.fetchall()

        lst = []

        # append all classes
        for row in rows:
            semlst = []
            for x in row:
                semlst.append(row[x])
            lst.append(semlst)
        
        c.close() 

        # print available classes
        print("AVAILABLE CLASSES:", lst)
        print()

        # get name and grade of class of interest
        name = input("CLASS NAME FOR UPDATE? ")
        grade = input("GRADE IN CLASS? EX: (A, A-, B+) ")
        name = name.lower()
        name = name.title()
        grade = grade.lower()
        grade = grade.title()

        # create cursor and update class
        cursor = cnx.cursor()
        cursor.callproc("updateGrade",(name, grade))

        # close cursor
        cursor.close() 
        print()

        print("SUCCESSFUL UPDATE")
        print()
        
        # ask user if they want another update
        valid = False
        while valid == False:
            print("WOULD YOU LIKE TO UPDATE ANOTHER GRADE?")
            tf = str(input("ENTER Y/N: ")).lower()
            if tf == "y":
                contreadtable = True
                break
            elif tf == "n":
                contreadtable = False
                print()
                print()
                print()
                break
            else:
                print("ERROR: PLEASE ENTER A VALID VALUE: Y/N")
                continue
                
            print()

def delete(cnx):
    
    print()
    print()
    print()
    print()
    
    # loop for continuing delete operations
    contreadtable = True
    while contreadtable == True:

        # create cursor and query for all classes
        c = cnx.cursor()
        c.execute("SELECT name FROM class")
        rows = c.fetchall()

        lst = []

        # append each class from each sem
        for row in rows:
            semlst = []
            for x in row:
                semlst.append(row[x])
            lst.append(semlst)

        # close cursor
        c.close() 

        # print available classes
        print("AVAILABLE CLASSES:", lst)
        print()

        # get class name
        name = input("NAME OF CLASS TO DELETE? ")
        name = name.lower()
        name = name.title()

        # call delete procedure for class
        cursor = cnx.cursor()
        cursor.callproc("deleteClass",(name,))

        # close cursor
        cursor.close() 
        print()
        
        print("SUCCESSFUL DELETE")
        
        # ask user if they want to delete again
        valid = False
        while valid == False:
            print("WOULD YOU LIKE TO DELETE ANOTHER CLASS?")
            tf = str(input("ENTER Y/N: ")).lower()
            if tf == "y":
                contreadtable = True
                break
            elif tf == "n":
                contreadtable = False
                print()
                print()
                print()
                break
            else:
                print("ERROR: PLEASE ENTER A VALID VALUE: Y/N")
                continue

            print()

def testSem(cnx):

    # bool to decide whether to add another class
    contreadtable = True
    lst = []

    # get current gpa credit val
    curgpa, totalcredits = gpa(cnx)
    curgpa = curgpa * totalcredits

    print("INPUT TEST GRADES TO CALCULATE EFFECT ON CUMULATIVE GPA FOR ALL SEMESTERS: ")
    print()

    # while still adding classes
    while contreadtable == True:

        # input for class and creds
        grade = input("GRADE IN TEST CLASS? ")
        creds = input("# OF CREDITS? ")
        print()

        # string fix
        grade = grade.lower()
        grade = grade.title()

        # append tuple
        lst.append((grade, int(creds)))

        # add another class or no?
        valid = False
        while valid == False:
            print("WOULD YOU LIKE TO ADD ANOTHER TEST CLASS?")
            tf = str(input("ENTER Y/N: ")).lower()
            if tf == "y":
                contreadtable = True
                break
            elif tf == "n":
                contreadtable = False
                print()
                print()
                print()
                break
            else:
                print("ERROR: PLEASE ENTER A VALID VALUE: Y/N")
                continue
        
    # iterate through each added class
    for i in range(len(lst)):

        # add total credits and score value based on grade
        totalcredits += lst[i][1]
        if lst[i][0] == "A":
            curgpa += 4 * lst[i][1]
        elif lst[i][0] == "A-":
            curgpa += ((3+ (2/3)) * lst[i][1])
        elif lst[i][0] == "B+":
            curgpa += ((3+ (1/3)) * lst[i][1])
        elif lst[i][0] == "B":
            curgpa += (3 * lst[i][1])
        elif lst[i][0] == "B-":
            curgpa += ((2+ (2/3)) * lst[i][1])
        elif lst[i][0] == "C+":
            curgpa += ((2+ (1/3)) * lst[i][1])
        elif lst[i][0] == "C":
            curgpa += (2 * lst[i][1])
        elif lst[i][0] == "C-":
            curgpa += ((1+ (2/3)) * lst[i][1])
        elif lst[i][0] == "D+":
            curgpa += ((1+ (1/3)) * lst[i][1])
        elif lst[i][0] == "D":
            curgpa += (1 * lst[i][1])
        elif lst[i][0] == "D-":
            curgpa += ((2/3) * lst[i][1])

    # calc test gpa
    testgpa = round(curgpa / totalcredits, 3)

    # print testsem gpa
    print("CUMULATIVE GPA WITH TEST SEMESTER: ", testgpa)
    print()
    
    # loop for continuing test sem operations
    contreadtable = True
    while contreadtable == True:

        # ask user if they want to test again
        valid = False
        while valid == False:
            print("WOULD YOU LIKE TO TEST OTHER SEMESTER GRADES?")
            tf = str(input("ENTER Y/N: ")).lower()
            if tf == "y":
                contreadtable = True
                testSem(cnx)
            elif tf == "n":
                contreadtable = False
                print()
                print()
                print()
                break
            else:
                print("ERROR: PLEASE ENTER A VALID VALUE: Y/N")
                continue
                
            print()

def gpa(cnx):
    
    print()
    print()
    print()

    # create cursor and query for all grades
    c = cnx.cursor()
    c.execute("SELECT grade, credits FROM class")
    rows = c.fetchall()

    lst = []

    # for each grade in semester
    for row in rows:

        # append semester grafes
        semlst = []
        for x in row:
            semlst.append(row[x])
        lst.append(semlst)

    # close cursor
    c.close() 

    # calculate gpa
    gpa = 0
    totalcredits = 0
    for grade in lst:
        totalcredits += grade[1]
        if grade[0] == "A":
            gpa += 4 * grade[1]
        elif grade[0] == "A-":
            gpa += ((3+ (2/3)) * grade[1])
        elif grade[0] == "B+":
            gpa += ((3+ (1/3)) * grade[1])
        elif grade[0] == "B":
            gpa += (3 * grade[1])
        elif grade[0] == "B-":
            gpa += ((2+ (2/3)) * grade[1])
        elif grade[0] == "C+":
            gpa += ((2+ (1/3)) * grade[1])
        elif grade[0] == "C":
            gpa += (2 * grade[1])
        elif grade[0] == "C-":
            gpa += ((1+ (2/3)) * grade[1])
        elif grade[0] == "D+":
            gpa += ((1+ (1/3)) * grade[1])
        elif grade[0] == "D":
            gpa += (1 * grade[1])
        elif grade[0] == "D-":
            gpa += ((2/3) * grade[1])

    # round gpa and print
    gpa = gpa / totalcredits
    roundgpa = round(gpa, 3)
    print("CURRENT GPA: ", roundgpa)
    print()

    return gpa, totalcredits

def main():

    print()
    print()
    username = input("Enter MySQL username: ")
    password = input("Enter MySQL password: ")

    try:
        cnx = connector(username, password)
        
    except pymysql.err.OperationalError as e:
        # if input username/password is invalid stop program
        return error(e)

    try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
        # display main menu
        print()
        print()
        print("----------------------------------------")
        print("   SUCCESSFUL ENTRY - GRADES DATABASE")
        print("----------------------------------------")
        print()
        print()
        
        # loop for chooosing CRUD or exit operation
        cont = True
        while cont == True:
            print("WHICH FUNCTIONALITY WOULD YOU LIKE TO USE?")
            optionalitylst = ["create", "read", "update", "delete", 
                              "test semester", "current gpa","exit database", "test", "gpa", "exit"]
            optionality = input("ENTER CREATE, READ, UPDATE, DELETE, "
                            "TEST SEMESTER, CURRENT GPA, OR EXIT DATABASE: ")
            
            optionality = optionality.lower()
            if optionality not in optionalitylst:
                print()
                print()
                print()
                print("-------------------------------------------")
                print(" ERROR: PLEASE ENTER A VALID FUNCTIONALITY")
                print("-------------------------------------------")
                print()
                print()
                continue
            
            # call specified option
            if optionality == "create":
                create(cnx)
                
            elif optionality == "read":
                read(cnx)
                
            elif optionality == "update":
                update(cnx)
                
            elif optionality == "delete":
                delete(cnx)
                
            elif optionality == "test semester" or optionality == "test":
                testSem(cnx)
                
            elif optionality == "current gpa" or optionality == "gpa":
                gpa(cnx)
            
            # end program if requested
            elif optionality == "exit database"or optionality == "exit":
                print()
                print("THANK YOU GOOD BYE")
                print()
                cont = False
                

    except pymysql.Error as e:
        # if input username/password is invalid stop program
        return error(e)

    finally:
        # close connection to db
        cnx.close()

if __name__ == "__main__":
    main()
    
    
