import os
from datetime import *
#from carpool import db, bcrypt
#from carpool.models import User, Car, CarManager

print("Welcome to Carpool!")
username = input("Enter username: ")
password = input("Enter password: ")


class TimeInterval:

    def __init__(self, start_date, end_date):
        self.end_date = end_date
        self.start_date = start_date

    def is_not_in_interval(self, requested_start_date: datetime, requested_end_date: datetime) -> bool:
        return (requested_start_date < self.start_date and requested_end_date < self.start_date) \
            or (requested_start_date > self.start_date and requested_end_date > self.end_date)


class RentableCar():  # ska inherita från car

    def __init__(self, id, car_name, model, license_plate, fuel, seats):
        self.booked_dates = []
        self.id = id
        self.car_name = car_name
        self.model = model
        self.license_plate = license_plate
        self.fuel = fuel
        self.seats = seats


    def add_booked_interval(self, interval):
        self.booked_dates.append(interval)

    def is_available(self, requested_interval: TimeInterval) -> bool:

        if len(self.booked_dates) == 0:
                return True

        for interval in self.booked_dates:
            if interval.is_not_in_interval(requested_interval.start_date, requested_interval.end_date):
                return True

        return False

    def __str__(self):
        return f"Car {self.id} information:\nName: {self.car_name}\nModel: {self.model}\nLicense plate: {self.license_plate}\nFuel level: {self.fuel}\nSeats: {self.seats}"


car1 = RentableCar(1, "Lighning McQueen", "Volvo V70", "LMG 204", "7", 5)
car2 = RentableCar(2, "Pelles bil", "Kia Venga", "ABG 907", "2", 5)
cars = [car1, car2]

available_cars = []

action = input("Would you like to book a car or view bookings? [Book/View]: ")

action.capitalize()

now = datetime.now()

print()
if action == "book":
    print(f"Current date and time: {now} ")
    print("What dates would you like to book?")
    first_date = input("Enter first date(YYYY-MM-DD): ")
    second_date = input("Enter last date(YYYY-MM-DD): ")

    try:
        desired_interval = TimeInterval(datetime.fromisoformat(first_date), datetime.fromisoformat(second_date))

        if datetime.fromisoformat(first_date) <= now or datetime.fromisoformat(second_date) <= now:
            print("The selected dates are in the past, please choose new ones.")

        # visa available cars, låt användaren välja

        elif car1.is_available(desired_interval):

            print("\nAvailable cars:\n")

            for car in cars:
                if car.is_available(desired_interval):
                    available_cars.append(car)
                    print(f"{car}\n")

            if len(available_cars) == 0:
                print("No available cars.")

            booked_car = available_cars[int(input("Select the car you wish to book by typing its id: "))]


            print(f"Successfully booked car {booked_car.id}, {booked_car.car_name}, {first_date} to {second_date}!")
            car1.add_booked_interval(desired_interval)
            print(f"\nThank you for using Carpool, {username.capitalize()}!")

        else:
            print("The dates you have selected are not available, please try again.")

    except:
        print("Your input is not valid. Try again!")


elif action == "view":
    print("Current bookings: ") #printa bokade datum mha databas

else:
    print("Please use commands [Book/View].")


if RentableCar == True:
    print("car is avalible")


#now = datetime.now()
#print (f"Current date and time: {now} ")
#print (now.strftime("%Y-%m-%d %H:%M:%S"))


