import csv

with open('message.csv') as csvfile:
    csvreader = csv.reader(csvfile)
    data = []
    for row in csvreader:
        for item in row:
            data.extend(list(item))

alphabet = list('abcdefghijklmnopqrstuvwxyz ')


def writeanswer(answer):
    with open('decrypted_file.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([answer])
        print(f'Answer written to decrypted_file.csv')


while True:
    shiftval = (input('Please enter a shift value.'))
    if shiftval.isnumeric():
        shiftval = int(shiftval)
        answer = ""
        for letter in data:
            if letter in alphabet:
                shift = (alphabet.index(letter) - shiftval) % len(alphabet)
                answer += alphabet[shift]
            else:
                answer += letter
        print(f'the decrypted form is \n{answer}')
        while True:
            yesorno = input('Do you want to write a CSV? (y/n)')
            match yesorno:
                case 'y':
                    writeanswer(answer)
                    break
                case 'n':
                    break
                case _:
                    'Please enter a valid answer.'
    else:
        print('Sorry, I did not understand your input. Please try again.')