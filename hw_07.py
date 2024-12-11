from collections import UserDict
from datetime import datetime, date, timedelta

class Field:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
   
    def __init__(self, value):
        super().__init__(value) 
        self.name = value


class Phone(Field):
    def __init__(self, value):
        self.value = value
        if len(value) != 10:                  # Функция валидации номера(строго 10 цифр)
            raise ValueError(f"The number should contains 10 digits" )
        if not value.isdigit():
            raise ValueError(f"The number should contains 10 digits" )
        
        
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = value
            self.value =datetime.strptime(self.value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        

class Record:
    
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for i in self.phones:
            if i.value == phone:
                self.phones.remove(i)

    def edit_phone(self, old_phone, new_phone):
        if self.find_phone(old_phone) == None:
            raise ValueError(f" Please, check if the phone number is correct?")
        self.phones.insert(self.phones.index(self.find_phone((old_phone))), Phone(new_phone)) 
        self.phones.remove(self.find_phone(old_phone))

    def find_phone(self, phone):
        for i in self.phones:
            if i.value == phone:
                return (i)  
        
    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday
        return self.birthday

    def show_birthday(self):
        return self.birthday
        

    
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    

class AddressBook(UserDict):
    def add_record(self, record:Record):
        self.data[record.name.value] = record

    def find(self, name):
            return self.data.get(name)
            
    def delete(self,name):
        self.data.pop(name,None)

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()
        birthday_this_year =[]

        for record in self.data: 
            birthday =self.data.get(record).birthday
            if birthday:
                birthday_this_year.append({"name": record, "birthday": birthday})
            
        for i in birthday_this_year:
            birthday = i.get("birthday")
            birthday = birthday.value.replace(year = today.year)
           
            if birthday.weekday() >=5:
                birthday = birthday + timedelta(7-birthday.weekday())
                if 0 < timedelta(birthday - today) <= days:
                    i["birthday"] = birthday.strftime('%d.%m.%Y')
                    upcoming_birthdays.append(i)       
                    return upcoming_birthdays
        if len(upcoming_birthdays) == 0:
            return "No congratulation date on this week"
                
    
    def __str__(self):
            return f"Contacts info: {'; '.join(str(p) for p in self.data.values())} "  
    


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Please, check the data was input."
        except KeyError:
            return "Contact not founded. Check Name please."
        except IndexError:
            return "Please use 'add', 'phone', 'change' or 'all' command."

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message
    
    
@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    message = "Contact updated."
    if record:
        if record.find_phone(old_phone):
            record.edit_phone(old_phone,new_phone)
            return message
        else:
            return "The phone to change was not found"
    else:
        return "Contact not found. Please, use command 'add'"

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    return book.find(name)

@input_error
def add_birthday(args, book: AddressBook):
    name = args[0]
    birthday = Birthday(args[1])
    record = book.find(name)
    if not record:
        return "Contact not found. Please, check name'"
    else:
        record.add_birthday(birthday)
        return f"Birthday of {name} is added."
        

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        birthday = record.birthday
        if birthday:
            birthday = birthday.value.strftime('%d.%m.%Y')
            return f"Name: {record.name.value}, Birthday: {birthday}"
        else:
            return "No info about birthday"
    else:
        return "Contact not found"

@input_error
def birthdays(book: AddressBook):
    return book.get_upcoming_birthdays()

    
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(book)
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")
    

if __name__ == "__main__":
    main()