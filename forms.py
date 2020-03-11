class TimeInterval:

    def __init__(self, start_date, end_date):
        self.end_date = end_date
        self.start_date = start_date

    def is_not_in_interval(self, requested_start_date: datetime, requested_end_date: datetime) -> bool:
        return (requested_start_date < self.start_date and requested_end_date < self.start_date) \
               or (requested_start_date > self.start_date and requested_end_date > self.end_date)
	
	
class RentableCar(Car):  # ska inherita från car

    def __init__(self):
        self.booked_dates = []


    def add_booked_interval(self, interval):
        self.booked_dates.append(interval)

    def is_available(self, requested_interval: TimeInterval) -> bool:

        if len(self.booked_dates) == 0:
            return True

        for interval in self.booked_dates:
            if interval.is_not_in_interval(requested_interval.start_date, requested_interval.end_date):
                return True

        return False


first_date = input("Enter first date(YYYY-MM-DD): ")
second_date = input("Enter last date(YYYY-MM-DD): ")
test_interval = TimeInterval(datetime.fromisoformat(first_date), datetime.fromisoformat(second_date))


car = RentableCar()
if car.is_available(test_interval):
    print(f"Successfully booked {first_date} to {second_date}!")
    car.add_booked_interval(test_interval)
else:
    print("The dates you have selected are not available, please try again.")
