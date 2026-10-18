def CalculateDay(date):
    centurycode = 0
    monthcode = 0 
    yearcode = 0
    leapyearcode = 0
    julian = (date[2], date[1], date[0]) < (1752, 9, 14)
    checkcent =  date[2] // 100
    if julian: #Julian 
        centurycode = (18 - (date[2] // 100)) % 7
        if date[2] % 4 == 0:
            leapyearcode = 1
    else: #greg
        centurycode = (6 - 2 * (checkcent % 4)) % 7
        leapyearcode = int(date[2] % 4 == 0 and (date[2]% 100 != 0 or date[2]% 400 == 0))    
    checkyear = int(str(date[2])[-2:])
    yearcode = (checkyear + (checkyear // 4)) % 7
    month_codes = {1: 0, 2: 3, 3: 3, 4: 6, 5: 1, 6: 4,
               7: 6, 8: 2, 9: 5, 10: 0, 11: 3, 12: 5}
    monthcode = month_codes[int(date[1])]
    if int(date[1]) <= 2:
        monthcode -= leapyearcode
    days = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
        4: "Thursday", 5: "Friday", 6: "Saturday"}
    day = (yearcode + monthcode + centurycode + date[0]) % 7
    print(f"{date[0]:02}/{date[1]:02}/{date[2]} is a {days[day]}")

def ValidDateCheck():
    while True:
        try:
            date = input("Please input date DD/MM/YYYY\n>")
            date = date.split('/')
            date = [int(i) for i in date]
            date = [abs(i) for i in date] #convert to pos using abs
            if not len(date) == 3:
                print("Not vaild")
                continue
            elif not date[0] <= 31:
                print("Not vaild")
                continue    
            elif not date[1] <= 12:
                print("Not vaild")
                continue
            else: 
                CalculateDay(date)
        except:
            print("Not vaild")



ValidDateCheck()
