import csv
import time as timer
from csv import DictWriter
from colorama import *
from tabulate import tabulate
from datetime import *

#File handling

with open('loaned.csv') as csvfile:
    csvreader = csv.reader(csvfile)
    loaned = list(csvreader)[1:]

with open('staff.csv') as csvfile:
    csvreader = csv.reader(csvfile)
    data = list(csvreader)[1:]

with open('borrowers.csv') as csvfile:
    csvreader = csv.reader(csvfile)
    borrowers = list(csvreader)[1:]


def staffupdate(targetcolumn, targetval, update, new):
    header = ['UserID', 'Name', 'Role', 'Email', 'PhoneNumber', 'HireDate', 'Password', 'Status']
    targetindex = header.index(targetcolumn)
    updateindex = header.index(update)

    for row in data:
        if row[targetindex] == targetval:
            row[updateindex] = new
    with open('staff.csv', mode='w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        csvwriter.writerows(data)


with open('inventories.csv') as csvfile:
    csvreader = csv.reader(csvfile)
    books = list(csvreader)[1:]


def loanedupdate(targetcolumn, targetval, update, new):
    header = ['BookID', 'BorrowerID', 'Due']
    targetindex = header.index(targetcolumn)
    updateindex = header.index(update)

    for row in borrowers:

        if row[targetindex] == targetval:
            row[updateindex] = new

    with open('loaned.csv', mode='w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        csvwriter.writerows(books)


def invupdate(targetcolumn, targetval, update, new):
    header = ['BookID', 'Title', 'Author', 'Genre', 'PublishedYear', 'TotalCopies', 'CopiesAvailable', 'OnLoan',
              'Deleted']
    targetindex = header.index(targetcolumn)
    updateindex = header.index(update)
    for row in books:
        if row[targetindex] == targetval:
            row[updateindex] = new
    with open('inventories.csv', mode='w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        csvwriter.writerows(books)

    # array for welcome title


title = ['╔', 'University Library Management System', '', '']
longest = max(title, key=len)
longestint = len(longest)

directory = []
showndirectory = ["Test", "Test2", "Test3"]


def main():
    while True:
        try:
            printtitle()
            login()
        except:
            print('Theres an error')
            mainpage(details[1], details[2])


def printtitle():
    print(f"╔", '═' * longestint + '╗' + '\n', '║' + title[1], ' ' * (longestint - len(title[1])), '║', '\n', '║',
          title[2], ' ' * (longestint - len(title[2])), '║', '\n', '║', title[3], ' ' * (longestint - len(title[3])),
          '║', '\n', '╚', '═' * longestint, '╝', '\n', sep='', end="\r")


def changedirectory(p):
    directory.append(p)
    showndirectory.append(p)
    if len(showndirectory) > 3:
        showndirectory.pop(0)
    title[3] = ' → '.join(showndirectory)


def go_back():
    if len(directory) > 1:
        directory.pop()
        prev_location = directory[-1]
        showndirectory.clear()
        showndirectory.extend(directory[-3:])
        title[3] = ' → '.join(showndirectory)
        print(f"Moved back to: {prev_location}")
    else:
        print("can't go back further.")


def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1


def loading(menu):
    for x in range(4):
        print(Style.BRIGHT, Fore.CYAN, f'Loading {menu}', '.' * x, Style.RESET_ALL, end="\r", )
        timer.sleep(1)


def mainpage(fullname, role):
    title[2] = f'{role} Options'
    changedirectory('Main Menu')
    printtitle()
    if role == 'Supervisor':
        print(f'Welcome {fullname}', 'Please Choose an Option:', '1 - Manage Book Inventories', '2 - Manage Accounts',
              '3 - Exit', sep='\n')
        loop = True
        while loop:
            option = input(f'>')
            match option:
                case '1':
                    managebookinv()
                case '2':
                    loop = False
                    manageaccount()
                case '3':
                    go_back()
                    login()
                case _:
                    print('Not an option')
                    loop = True
    else:
        print(f'Welcome {fullname}', 'Please Choose an Option:', '1 - Loan Books', '2 - Return Books',
              '3 - Extend loan period', '4 - Search for a book', '5 - Exit', sep='\n')
        loop = True
        while loop:
            option = input(f'>')
            match option:
                case '1':
                    loanbooks()
                case '2':
                    returnbooks()
                case '3':
                    extendloan()
                case '4':
                    search4abook()
                case '5':
                    print('4 - Exit')
                    go_back()
                    login()
                case _:
                    print('Not an option')
                    loop = True


def loanbooks():
    changedirectory('Loan Books')
    title[2] = 'Librarian Loan Books'
    printtitle()
    print('Please search for the Book you wish to loan:')
    search = input(f'>')
    found = False
    results = [
        ["Index", "BookID", "Title", "Author", "Genre", "PublishedYear", "TotalCopies", "CopiesAvailable", "OnLoan",
         "Deleted"]]
    count = 0
    for row in books:
        if search in str(row).lower():
            newrow = [str(len(results))] + row
            results.append(newrow)
            found = True
        count += 1
    if not found:
        print(Style.BRIGHT, Fore.RED, f'Book Not Found', Style.RESET_ALL)
        loanbooks()
    else:
        print("I found these following books:")
        print(tabulate(results, headers="firstrow"))
        if len(results) == 2:
            loop = True
            while loop:
                answer = input('Do you want to loan this book?\ntype yes or no\n>')
                match answer.lower():
                    case 'yes' | 'y':
                        loop = False
                        newrow = results[1]
                        userloan(newrow[1])
                    case 'no':
                        loop = False
                        mainpage(details[1], details[2])
                    case _:
                        print('Not an option')
        else:
            loop = True
            while loop:
                answer = input('Please input the index of the book you want to loan\n>')
                try:
                    answer = int(answer)
                    selected = results[answer]
                    newrow = results[answer]
                    swoop = True
                    while swoop:
                        selected = [results[answer]]
                        print(tabulate(selected, headers="firstrow"))
                        answer = input('Is this the book you want to loan? Type yes or no\n>')
                        match answer:
                            case 'yes':
                                swoop = False
                                userloan(newrow[1])
                            case 'no':
                                print('No')
                                swoop = False
                            case _:
                                print('Not an option')
                                swoop = True
                except Exception as error:
                    print(error)


def userloan(book):
    print('Please search for the User you wish to loan to:')
    search = input(f'>')
    found = False
    results = [
        ["Index", "BorrowerID", "Name", "Address", "PhoneNumber", "Email", "MembershipDate"]]
    count = 0
    for row in borrowers:
        if search in str(row).lower():
            newrow = [str(len(results))] + row
            results.append(newrow)
            found = True
        count += 1
    if not found:
        print(Style.BRIGHT, Fore.RED, f'User Not Found', Style.RESET_ALL)
        userloan(book)
    else:
        print("I found these following Users:")
        print(tabulate(results, headers="firstrow"))
        if len(results) == 2:
            loop = True
            while loop:
                answer = input('Do you want to loan to this user?\ntype yes or no\n>')
                match answer:
                    case 'yes':
                        loop = False
                        newrow = results[1]
                        loanbookadd(book, newrow[1])
                    case 'no':
                        loop = False
                        mainpage(details[1], details[2])
                    case _:
                        print('Not an option')
        else:
            loop = True
            while loop:
                answer = input('Please input the index of the user you want to loan to\n>')
                try:
                    answer = int(answer)
                    selected = results[answer]
                    newrow = results[answer]
                    swoop = True
                    while swoop:
                        selected = [results[answer]]
                        print(tabulate(selected, headers="firstrow"))
                        answer = input('Is this the user you want to loan to? Type yes or no\n>')
                        match answer:
                            case 'yes':
                                swoop = False
                                loanbookadd(book, newrow[1])
                            case 'no':
                                print('No')
                                swoop = False
                            case _:
                                print('Not an option')
                                swoop = True
                except Exception as error:
                    print(error)


def loanbookadd(book, user):
    dateofreturn = datetime.today() + timedelta(days=14)
    dateofreturnbutastr = dateofreturn.strftime('%d/%m/%Y')
    things = [book, user, dateofreturn.strftime('%d/%m/%Y')]
    print(f'this book will be due on the {dateofreturnbutastr}')
    answer = input('Do you want to loan this book? Type yes or no\n>')
    match answer:
        case 'yes':
            x = 0
            y = 0
            for row in books:
                if str(row[0]) == str(book):
                    x = int(row[7]) + 1
                if str(row[0]) == str(book):
                    y = int(row[6]) + 1
            invupdate('BookID', book, 'OnLoan', x)
            with open('loaned.csv', 'a') as inv:
                inv.write(','.join(str(item) for item in things) + '\n')
            print(Style.BRIGHT, Fore.RED, f'LOAN ADDED TO LIST', Style.RESET_ALL)
            loading('Main Menu')
            mainpage(details[1], details[2])
        case 'no':
            mainpage(details[1], details[2])


def returnbooks():
    changedirectory('Return Books')
    title[2] = 'Librarian Return Books'
    printtitle()
    print('Please search for the userID, bookID, or Date of the loan entry')
    search = input(f'>')
    found = False
    results = [['BookID', 'BorrowerID', 'Due']]
    count = 0
    for row in loaned:
        if search in str(row).lower():
            newrow = [str(len(results))] + row
            results.append(newrow)
            found = True
        count += 1
    if not found:
        print(Style.BRIGHT, Fore.RED, f'Return entry Not Found', Style.RESET_ALL)
        returnbooks()
    else:
        print("I found these following enteries:")
        print(tabulate(results, headers="firstrow"))
        if len(results) == 2:
            loop = True
            while loop:
                answer = input('Do you want to return this book?\ntype yes or no\n>')
                match answer:
                    case 'yes':
                        loop = False
                        newrow = results[1]
                        returnbookadd(results[1][1], results[1][2])
                    case 'no':
                        loop = False
                        mainpage(details[1], details[2])
                    case _:
                        print('Not an option')
        else:
            loop = True
            while loop:
                answer = input('Please input the index of the loan entry you wish to change\n>')
                try:
                    answer = int(answer)
                    selected = results[answer]
                    newrow = results[answer]
                    swoop = True
                    while swoop:
                        selected = [results[answer]]
                        print(tabulate(selected, headers=["Index", "BookID", "BorrowerID", "Due"]))
                        answer = input('Is this the book you want to return? Type yes or no\n>')
                        match answer:
                            case 'yes':
                                swoop = False
                                returnbookadd(newrow[1], newrow[2])
                            case 'no':
                                print('No')
                                swoop = False
                            case _:
                                print('Not an option')
                                swoop = True
                except Exception as error:
                    print(error)


def returnbookadd(book, user):
    things = [book, user]
    x = 0
    y = 0
    for row in books:
        if str(row[0]) == str(book):
            if x == -1:
                print(Style.BRIGHT, Fore.RED, f'ERROR IN BOOK COUNT, 0 BOOKS TO BE RETURNED', Style.RESET_ALL)
                loading('Main Menu')
                mainpage(details[1], details[2])
            else:
                x = int(row[7]) - 1
        if str(row[0]) == str(book):
            if y == -1:
                print(Style.BRIGHT, Fore.RED, f'ERROR IN BOOK COUNT, 0 BOOKS TO BE RETURNED', Style.RESET_ALL)
                loading('Main Menu')
                mainpage(details[1], details[2])
            else:
                y = int(row[6]) - 1
    invupdate('BookID', book, 'OnLoan', x)
    invupdate('BookID', book, 'CopiesAvailable', y)
    with open('loaned.csv', 'r') as inv:
        loans = list(csv.reader(inv))
        header = loans[0]
        rows = loans[1:]
    newrow = []
    removed = False
    for row in rows:
        if row[0] == str(book) and row[1] == str(user):
            removed = True
        else:
            newrow.append(row)
    if removed == False:
        print('Error in returning book, please try again')
        mainpage(details[1], details[2])

    with open('loaned.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(newrow)
    print(Style.BRIGHT, Fore.GREEN, f'BOOK RETURNED', Style.RESET_ALL)
    loading('Main Menu')
    mainpage(details[1], details[2])


def extendloan():
    changedirectory('Extend Loan')
    title[2] = 'Librarian Extend Loan Time'
    printtitle()
    print('Please search for the userID, bookID, or Date of the loan entry')
    search = input(f'>')
    found = False
    results = [['BookID', 'BorrowerID', 'Due']]
    count = 0
    for row in loaned:
        if search in str(row).lower():
            newrow = [str(len(results))] + row
            results.append(newrow)
            found = True
        count += 1
    if not found:
        print(Style.BRIGHT, Fore.RED, f'Return entry Not Found', Style.RESET_ALL)
        extendloan()
    else:
        print("I found these following enteries:")
        print(tabulate(results, headers="firstrow"))
        if len(results) == 2:
            loop = True
            while loop:
                answer = input('Do you want to extend the time on this book?\ntype yes or no\n>')
                match answer:
                    case 'yes':
                        loop = False
                        newrow = results[1]
                        extendadd(results[1][1], results[1][2])
                    case 'no':
                        loop = False
                        mainpage(details[1], details[2])
                    case _:
                        print('Not an option')
        else:
            loop = True
            while loop:
                answer = input('Please input the index of the loan entry you wish to extend\n>')
                try:
                    answer = int(answer)
                    selected = results[answer]
                    newrow = results[answer]
                    swoop = True
                    while swoop:
                        selected = [results[answer]]
                        print(tabulate(selected, headers=["Index", "BookID", "BorrowerID", "Due"]))
                        answer = input('Is this the book you want to extend the loan time on? Type yes or no\n>')
                        match answer:
                            case 'yes':
                                swoop = False
                                extendadd(newrow[1], newrow[2])
                            case 'no':
                                print('No')
                                swoop = False
                            case _:
                                print('Not an option')
                                swoop = True
                except Exception as error:
                    print(error)


def extendadd(book, user):
    with open('loaned.csv', 'r') as inv:
        loans = list(csv.reader(inv))
        header = loans[0]
        rows = loans[1:]
    for i in range(len(rows)):
        row = rows[i]
        if row[0] == str(book) and row[1] == str(user):
            currenttime = datetime.strptime(row[2], '%d/%m/%Y')
            extendedtime = currenttime + timedelta(days=14)
            x = extendedtime.strftime('%d/%m/%Y')
            rows[i][2] = x
            print(Style.BRIGHT, Fore.GREEN, f'THE NEW DUE DATE IS {rows[i][2]}', Style.RESET_ALL)

    with open('loaned.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)
    print(Style.BRIGHT, Fore.GREEN, f'EXTENDED TIME ADDED', Style.RESET_ALL)
    loading('Main Menu')
    mainpage(details[1], details[2])


def search4abook():
    changedirectory('Search Books')
    title[2] = 'Search A Book'
    printtitle()
    print('Please search for the Book')
    search = input(f'>')
    found = False
    results = [
        ["Index", "BookID", "Title", "Author", "Genre", "PublishedYear", "TotalCopies", "CopiesAvailable", "OnLoan",
         "Deleted"]]
    count = 0
    for row in books:
        if search in str(row).lower():
            newrow = [str(len(results))] + row
            results.append(newrow)
            found = True
        count += 1
    if not found:
        print(Style.BRIGHT, Fore.RED, f'Book Not Found', Style.RESET_ALL)
        findbook()
    else:
        print("I found these following books:")
        print(tabulate(results))
        if len(results) == 2:
            loop = True
            while loop:
                answer = input('Press any key to continue\n>')
                mainpage(details[1], details[2])
        else:
            loop = True
            while loop:
                answer = input('Please input the index of the book you want to manage\n>')
                try:
                    answer = int(answer)
                    selected = results[answer]
                    newrow = results[answer]
                    swoop = True
                    while swoop:
                        selected = [results[answer]]
                        print(tabulate(selected,
                                       headers=["Index", "BookID", "Title", "Author", "Genre", "PublishedYear",
                                                "TotalCopies", "CopiesAvailable", "OnLoan", "Deleted"]))
                        answer = input('Please press any key to continue\n>')
                        mainpage(details[1], details[2])
                except:
                    print("please enter a valid integer in range")


def managebookinv():
    changedirectory('Manage Book Inventories')
    title[2] = 'Manage Book Inventories'
    printtitle()
    print(f'Please Choose an Option:', '1 - Add a New Book', '2 - Find a book to Update', '3 - Back', sep='\n')
    loop = True
    while loop:
        option = input(f'>')
        match option:
            case '1':
                addbook()
            case '2':
                findbook()
            case '3':
                go_back()
                login()
            case _:
                print('Not an option')
                loop = True


def addbook():
    changedirectory('Add Book')
    printtitle()
    with open('inventories.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        books = list(csvreader)[1:]

    answer = input('Do you want to add a new book?\ntype yes or no\n>')
    lastbook = int(books[(len(books) - 1)][0])
    print(lastbook)
    newbook = lastbook + 1
    if answer == 'yes':
        things = []
        print(f'The last book in the list was {lastbook} this will make the BookID of this new book {newbook} ')
        things.append(newbook)
        titleinp = input('what do you want the title of this book to be?\n>')
        things.append(titleinp)
        authorinp = input('what do you want the author of this book to be?\n>')
        things.append(authorinp)
        genreinp = input('what do you want the genre of this book to be?\n>')
        things.append(genreinp)
        publishedinp = input('what do you want the published year of this book to be?\n>')
        things.append(publishedinp)
        totalcopiesinp = input('what do you want the total copies of this book to be?\n>')
        things.append(totalcopiesinp)
        copiesavaiableinp = input('what do you want the available copies of this book to be?\n>')
        things.append(copiesavaiableinp)
        onloaninp = input('what do you want the total copies on loan of this book to be?\n>')
        things.append(onloaninp)
        deleteinp = input('what do you want the value deleted of this book to be?\n>')
        things.append(deleteinp)

        header = ["BookID", "Title", "Author", "Genre", "PublishedYear", "TotalCopies", "CopiesAvailable", "OnLoan",
                  "Deleted"]
        print(tabulate([things], headers=header))
        answer = input(
            "Here is finished result of the added book are you sure you wish you add it? (type yes or no)\n>")
        if answer == 'yes':
            with open('inventories.csv', 'a',newline='') as inv:
                inv.write(','.join(str(item) for item in things) + '\n')
            print(Style.BRIGHT, Fore.RED, f'BOOK ADDED TO LIST', Style.RESET_ALL)
            loading('Main Menu')
            mainpage(details[1], details[2])
        else:
            print('Returning to main menu')
            go_back()
            mainpage(details[1], details[2])

    else:
        go_back()
        mainpage(details[1], details[2])


def findbook():
    changedirectory('Search Books')
    title[2] = 'Manage Book Inventories'
    printtitle()
    with open('inventories.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        books = list(csvreader)[1:]

    print('Please search for the Book you wish to manage:')
    search = input(f'>')
    found = False
    results = [
        ["Index", "BookID", "Title", "Author", "Genre", "PublishedYear", "TotalCopies", "CopiesAvailable", "OnLoan",
         "Deleted"]]
    count = 0
    for row in books:
        if search in str(row).lower():
            newrow = [str(len(results))] + row
            results.append(newrow)
            found = True
        count += 1
    if not found:
        print(Style.BRIGHT, Fore.RED, f'Book Not Found', Style.RESET_ALL)
        findbook()
    else:
        print("I found these following books:")
        print(tabulate(results))
        if len(results) == 2:
            loop = True
            while loop:
                answer = input('Do you want to manage this book?\ntype yes or no\n>')
                match answer:
                    case 'yes':
                        loop = False
                        newrow = results[1]
                        book(search, results[1])
                    case 'no':
                        loop = False
                        managebookinv()
                    case _:
                        print('Not an option')
        else:
            loop = True
            while loop:
                answer = input('Please input the index of the book you want to manage\n>')
                try:
                    answer = int(answer)
                    selected = results[answer]
                    newrow = results[answer]
                    swoop = True
                    while swoop:
                        selected = [results[answer]]
                        print(tabulate(selected,
                                       headers=["Index", "BookID", "Title", "Author", "Genre", "PublishedYear",
                                                "TotalCopies", "CopiesAvailable", "OnLoan", "Deleted"]))
                        answer = input('Is this the book you want to manage? Type yes or no\n>')
                        match answer:
                            case 'yes':
                                swoop = False
                                book(search, newrow)
                            case 'no':
                                swoop = False
                                findbook()
                            case _:
                                print('Not an option')
                                swoop = True
                except:
                    print("please enter a valid integer in range")


def book(search, newrow):
    changedirectory("'" + search + "'")
    printtitle()
    results = ["Index", "BookID", "Title", "Author", "Genre", "PublishedYear", "TotalCopies", "CopiesAvailable",
               "OnLoan", "Deleted"]
    print(
        f'What would you like to do with {newrow[1]}?\n1- Available\n2- On Loan\n3- Delete\n4- Book Information\n5- exit to main menu')
    loop = True
    while loop:
        option = input(f'>')
        match option:
            case '1':
                available = int(
                    input(f'Please enter the new amount of available, current amount stands at {newrow[7]}\n>'))
                invupdate('BookID', newrow[1], 'CopiesAvailable', available)
                print(Style.BRIGHT, Fore.RED,
                      f'UPDATED THE AMOUNT OF COPIES AVAILABLE TO {available}\nRETURNING TO MAIN MENU', Style.RESET_ALL)
                loading('Main Menu')
                mainpage(details[1], details[2])
                loop = False
            case '2':
                OnLoan = int(
                    input(f'Please enter the new amount of books OnLoan, current amount stands at {newrow[8]}\n>'))
                invupdate('BookID', newrow[1], 'OnLoan', OnLoan)
                print(Style.BRIGHT, Fore.RED,
                      f'UPDATED THE AMOUNT OF COPIES ON LOAN TO {OnLoan}\nRETURNING TO MAIN MENU', Style.RESET_ALL)
                loading('Main Menu')
                mainpage(details[1], details[2])
                loop = False
            case '3':
                delete = int(
                    input(f'Please enter the new amount of books deleted, current amount stands at {newrow[9]}\n>'))
                invupdate('BookID', newrow[1], 'Deleted', delete)
                print(Style.BRIGHT, Fore.RED,
                      f'UPDATED THE AMOUNT OF COPIES ON LOAN TO {delete}\nRETURNING TO MAIN MENU', Style.RESET_ALL)
                loading('Main Menu')
                mainpage(details[1], details[2])
                loop = False
            case '4':
                print(tabulate([newrow], headers=results))
                skip = input('Press any key to return to main menu\n>')
                if skip == '':
                    loading('Main Menu')
                    mainpage(details[1], details[2])
            case '5':
                mainpage(details[1], details[2])
                loop = False
            case _:
                print('Not an option')


def manageaccount():
    changedirectory('Manage Accounts')
    title[2] = 'Manage Accounts'
    printtitle()
    print('Please search for the account you wish to manage:')
    search = input(f'>')
    found = False
    results = [["index", "UserID", "Name", "Role", "Email", "PhoneNumber", "HireDate", "Status"]]
    count = 0
    for row in data:
        if search in str(row):
            newrow = [str(len(results))] + row
            newrow.remove(newrow[7])
            results.append(newrow)
            found = True
        count += 1
    if not found:
        print(Style.BRIGHT, Fore.RED, f'Account Not Found', Style.RESET_ALL)
        manageaccount()
    else:
        print("I found these following accounts:")
        print(tabulate(results))
        if len(results) == 2:
            loop = True
            while loop:
                answer = input('Do you want to manage this account?\ntype yes or no\n>')
                match answer:
                    case 'yes':
                        loop = False
                        accountmanagement_account_selected(search, newrow)
                    case 'no':
                        loop = False
                        print('No')
                    case _:
                        print('Not an option')
        else:
            loop = True
            while loop:
                answer = input('Please input the index of the account you want to manage\n>')
                try:
                    answer = int(answer)
                    selected = results[answer]
                    swoop = True
                    while swoop:
                        answer = input(f'Is {selected[2]} the account you want to manage? type yes or no\n>')
                        match answer:
                            case 'yes':
                                swoop = False
                                accountmanagement_account_selected(search, selected)
                            case 'no':
                                print('No')
                                swoop = False
                            case _:
                                print('Not an option')
                                swoop = True
                except:
                    print("please enter a valid integer in range")


def accountmanagement_account_selected(searchterm, selectedaccount):
    changedirectory("'" + searchterm + "'")
    printtitle()
    print(
        f'What would you like to do with {selectedaccount[2]}?\n1- make account active\n2- make account inactive\n3- block the account\n4- exit to main menu')
    loop = True
    while loop:
        option = input(f'>')
        match option:
            case '1':
                staffupdate('Name', selectedaccount[2], 'Status', 'active')
                print(Style.BRIGHT, Fore.RED, f'UPDATED THE STATUS OF {selectedaccount[2]} TO ACTIVE', Style.RESET_ALL)
                loading('main page')
                mainpage(details[1], details[2])
                loop = False
            case '2':
                staffupdate('Name', selectedaccount[2], 'Status', 'inactive')
                print(Style.BRIGHT, Fore.RED, f'UPDATED THE STATUS OF {selectedaccount[2]} TO INACTIVE',
                      Style.RESET_ALL)
                loading('main page')
                mainpage(details[1], details[2])
                loop = False
            case '3':
                staffupdate('Name', selectedaccount[2], 'Status', 'blocked')
                print(Style.BRIGHT, Fore.RED, f'UPDATED THE STATUS OF {selectedaccount[2]} TO BLOCKED', Style.RESET_ALL)
                loading('main page')
                mainpage(details[1], details[2])
            case '4':
                loading('main page')
                mainpage(details[1], details[2])
                loop = False
            case _:
                print('Not an option')
                loop = True

            # password


def password(userpass, details):
    attempts = 3
    while attempts > 0:
        passID = input('Please enter your password\n>')
        if passID == userpass:
            mainpage(details[1], details[2])
            return
        attempts -= 1
        print(f'Wrong password, {attempts} attempts left' if attempts else '\nYour account has been blocked')
    staffupdate('Name', details[1], 'Status', 'blocked')
    login()


# loginf
def login():
    changedirectory('Login')
    while True:
        userID = input('\nPlease enter your user ID\n>')
        for row in data:
            if row[0] == userID:
                if row[7] == 'blocked':
                    print(Style.BRIGHT, Fore.RED, 'Account is Blocked', Style.RESET_ALL)
                    login()
                    break
                if row[7] == 'inactive':
                    print(Style.BRIGHT, Fore.RED, 'Account is inactive', Style.RESET_ALL)
                    break
                global details
                details = row
                password(details[6], details)
                return details
        print(Style.BRIGHT, Fore.RED, f'User not found', Style.RESET_ALL)


main()