"""For example."""
from datetime import datetime, timedelta
import os
import pickle
import random
import sys


def inserting_info_hot_day(hot_date_weekday: int, happy_users: list, user: dict):
    """
    Simple function to fill list of happy users of the next week.

        Parameters: 
            hot_date_weekday (int): Digit-day of week. 
            happy_users (list): List of users with upcoming birthdays. 
            user (dict): List of dictionaries with keys: "name"
                and "birthday".

        Returns: 
            happy_users (list): List of users with upcoming 
                birthdays (of the next week).
    """
    if hot_date_weekday == 5:
        hot_date_weekday = 0
        # to congratulate on Monday, but we need to know when it was
        add_service_info = "(Saturday), "
    elif hot_date_weekday == 6:
        hot_date_weekday = 0
        # to congratulate on Monday, but we need to know when it was
        add_service_info = "(Saturday), "
    else:
        add_service_info = ", "
    try:
        happy_user = happy_users.pop(hot_date_weekday)
    except IndexError:
        print("Disaster, there is no item to extract!")
        return happy_users
    happy_users.insert(hot_date_weekday, happy_user +
                       user.get("name", 'NONAME') + add_service_info)
    return happy_users


def get_birthdays_per_week(users: list, on_date=datetime.now().date()):
    """
    The function displays users with birthdays one week ahead 
    of the current day or on date.
    users =[{'name':'name1', 'birthday':datetime1},{'name':'name2', 
    'birthday':datetime2}, ... , {'name':'nameN', 'birthday':datetimeN}].

        Parameters: 
            users (list): List of dictionaries with keys: "name" 
                and "birthday", on_date - datetime obj.date().
            on_date (datetime.date() object): The date from which you need to prepare to wish users a happy birthday
                next week.
        
        Returns: 
            None.
    """
    happy_users = ['Monday: ', 'Tuesday: ',
                   'Wednesday: ', 'Thursday: ', 'Friday: ']
    current_datetime = on_date
    # from next(current) Saturday:
    start_date = current_datetime + \
        timedelta(days=int(5-current_datetime.weekday()))
    # to next Friday (including both):
    finish_date = start_date + timedelta(days=6)
    # for all users:
    for user in users:
        hot_date = user.get("birthday")
        # if the week is the last of the year:
        delta_next_year = 1 if hot_date.month == (
            finish_date.year-start_date.year) else 0
        hot_date = datetime(year=current_datetime.year +
                            delta_next_year, month=hot_date.month, day=hot_date.day)
        if start_date <= hot_date.date() <= finish_date:
            # if hot_date.weekday() == 5 or hot_date.weekday() == 6:
            happy_users = inserting_info_hot_day(
                hot_date.weekday(), happy_users, user)

    for happy_user in happy_users:
        if happy_user[-2] != ":":
            happy_user = happy_user[:-2]
            print(happy_user)


def check_user_data(users: list):
    """
    For check users data from file.

        Parameters: 
            users(list): Must be a list of dictionaries with keys: "name" 
                and "birthday".
        
        Returns: 
            users OR [].
    """
    if isinstance(users, list) and users:
        for element in users:
            if isinstance(element, dict) and \
                isinstance(element.get("name", None), str) \
                    and isinstance(element.get("birthday", None), datetime):
                continue
            else:
                return []
    else:
        return []
    return users


def load_users_list():
    """
    For load users list from file... "users.data". # (to enter a parameter?).

        Parameters: 
            None.

        Returns: 
            users (list): List from file... list of dictionaries with 
                keys: "name" and "birthday".
    """
    if os.path.isfile(os.path.join(os.path.abspath(os.path.dirname(__file__)), "users.data")):
        users = []
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "users.data"), 'rb') as fh:
            try:
                users = pickle.load(fh)
            except pickle.UnpicklingError:
                print('The File is corrupted, my apologies.')
                # raise
            except Exception as e:
                print(f'The File is corrupted, my apologies. {repr(e)}')
                # raise pickle.UnpicklingError(repr(e))
        users = check_user_data(users)
        if not users:
            print('There is no valid data in the file!')
    else:
        print('Sorry, but there is no File next to the py-file')
        users = []

    return users


def save_users_list(users: list):
    """
    For save users list in file... "users.data". # (to enter a parameter?).

        Parameters: 
            users (list): List of dictionaries with 
                keys: "name" and "birthday".
        
        Returns: 
            None.
    """
    if users and isinstance(users, list):
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "users.data"), 'wb') as fh:
            try:
                pickle.dump(users, fh)
            except pickle.UnpicklingError:
                print(
                    'Something went wrong while trying to write the file, you can try again.')
                # raise
            except Exception as e:
                print(f'Something went wrong while trying to write the file, you can try again. {repr(e)}')
                # raise pickle.UnpicklingError(repr(e))
    else:
        print("No data to save!")


def validate_date(birthday_data: str):
    """A simple function to validate the date entered by the user.

        Parameters: 
            birthday_data(str): String line in format: YYYY-MM-DD.

        Returns: 
            False: if data must be re-entered, 
            else: birthday_data: datetime.
    """
    birthday_data = birthday_data.split('-')
    try:
        birthday_data = datetime(
            year=int(birthday_data[0]), month=int(birthday_data[1]), day=int(birthday_data[2]))
        if birthday_data > datetime.now().date():
            print("No man from the future!")

            return False

    except ValueError:
        return False

    return birthday_data


def manual_data_entry(users: list):
    """
    For manual data entry: users.

        Parameters: 
            users (list): List of dictionaries with keys: "name" 
                and "birthday".

        Returns: 
            users (list): Updated list of dictionaries with keys: "name" 
                and "birthday".
    """

    print('Be very careful when entering the data! ')
    answer_finish_input = ''
    while answer_finish_input != 'y' or answer_finish_input != 'Y':
        user_name = input('Name of person: ')  # username
        birthday_data = input('Enter Birthday (YYYY-MM-DD): ')
        birthday_data = validate_date(birthday_data)
        if not birthday_data:
            continue
        users.append({'name': user_name, 'birthday': birthday_data})
        answer_finish_input = input('Finish entering data? y=Yes, or No?: ')
        if answer_finish_input == 'y' or answer_finish_input == 'Y':
            break
    # save_users_list(users)

    return users


def create_users_data(users: list):
    """
    Create a test list of users and fill it yourself.
    The function allows you to create a list of users with
    birthdays OR/AND save this data in the file "users.data"
    next to the program, OR load this data from the file
    into the variable "users" - list of dictionaries with keys: "name" 
    and "birthday"

        Parameters: 
            users (list): List of dictionaries with keys: "name" 
                and "birthday".
        
        Returns: 
            users (list): Updated list of dictionaries with keys: "name" 
                and "birthday".
    """
    print('Now need create users list or load from file...')
    # answer = '0'
    while True:
        answer = input(
            '1 - Try load from file "users.data"\n2 - Manual data entry\n3 - exit\n')
        try:
            answer = int(answer)
        except ValueError:
            print('Invalid input, please try again ')
        if answer in (1, 2, 3):
            break
    if answer == 3:
        exit()
    if answer == 2:
        users = manual_data_entry(users)
    if answer == 1:
        users = load_users_list()

    return users


def random_date(start_month=1, end_month=12, start_day=1, end_day=31, max_year=datetime.now().year-1):
    """
    For generate random date in datetime object.

        Parameters: 
            all start parameters: limits of generator.

        Returns: 
            datetime object with random date.
    """
    if max_year < 1922:
        max_year = datetime.now().year - 1
    year = random.randint(1922, max_year)   # 2022, 2072
    month = random.randint(start_month, end_month)  # 1, 12
    day = random.randint(start_day, end_day)  # 1, 31  # 30/29/28
    while True:
        try:
            datetime(year=year, month=month, day=day)
            break
        except ValueError:
            day = random.randint(start_day, end_day)

    return datetime(year=year, month=month, day=day)


def generator_virtual_persons(persons_limit: int):
    """
    For create a test list of users from 144 to 288 (only for test).

        Returns: 
            users (list): Created list of dictionaries with keys: "name" 
                and "birthday".
    """
    users = []
    for num in range(persons_limit):
        current_month = 1 + num // (persons_limit // 12)
        start_day = 1 + 7 * (num % 4)
        end_day = start_day + 7  # 7? ! 30+31? -> 8 ) 32 )))
        users.append({'name': 'Name_' + str(num), 'birthday': random_date(
            current_month, current_month, start_day, end_day)})

    return users


def show_users(users: list):
    """
    For print list of users.

        Parameters: 
            users (list): List of dictionaries with keys: "name" 
                and "birthday".
    """
    if users:
        for user in users:
            print(user)


def main():
    """
    Basic function to display user birthdays per week.
    The function displays users with birthdays one week ahead 
    of the current day.
    1 - automatically form a list of users with random date and 
        numbered names - for example and for testing
    0 - manually create a list of users (or load from file - next try)
    """
    users = load_users_list()

    if len(sys.argv) < 2:
        print('No startup parameter entered, must be 1 or 0')
        print('1 - automatically form a list of users\n    with random date and numbered names')
        print('0 - manually create a list of users')
        input("Incorrect input start parameters! \n Press Enter for EXIT...")
        # # time to test:
        # users = load_users_list()  # time to test:
        show_users(users)
        get_birthdays_per_week(users)

        exit()
    if sys.argv[1] == "1":
        users = generator_virtual_persons(persons_limit=180)
        save_users_list(users)
    elif sys.argv[1] == "0":
        users = create_users_data(users)
        save_users_list(users)
    else:
        input("Incorrect input start parameters! ")
        exit()

    while True:
        specific_date = input(
            "Press enter for the current date, or enter a specific'\
                ' date (YYYY-MM-DD): ")
        if len(specific_date) == 0:
            get_birthdays_per_week(users)  # on_date=datetime.now().date()
            break
        else:
            specific_date = validate_date(specific_date)
            if not specific_date:
                continue
            get_birthdays_per_week(users, specific_date)
            break


if __name__ == "__main__":
    main()
