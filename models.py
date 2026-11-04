from abc import ABC, abstractmethod
import exceptions as e

class Room(ABC):
    def __init__(self,room_no,floor):
        self.room_no=room_no;
        self.floor=floor
    @abstractmethod
    def get_rate(self):
        pass
    @abstractmethod
    def get_max_guests(self):
        pass
    @abstractmethod
    def get_breakfast(self):
        pass
    @abstractmethod
    def get_extra_guest_charge(self):
        pass
    def __str__(self):
        return f"room_no:{self.room_no}"
        

class StandardRoom(Room):
    def get_rate(self): 
        return 2500
    def get_max_guests(self):
        return 2
    def get_breakfast(self):
        return "optional"
    def get_extra_guest_charge(self):
        return 0
    
class DeluxeRoom(Room):
    def get_rate(self):
        return 4000
    def get_max_guests(self):
        return 3
    def get_breakfast(self):
        return "included"
    def get_extra_guest_charge(self,guest_count):
        if guest_count>2:
            return 800
        return 0
    
class SuiteRoom(Room):
    def get_rate(self):
        return 7500
    def get_max_guests(self):
        return 4
    def get_breakfast(self):
        return "included"
    def get_extra_guest_charge(self,guest_count):
        if guest_count>2:
            return 800
        return 0

class Guest:
    def __init__(self,name,mobile,email):
        self.name=name;
        self.mobile=mobile;
        self.email=email
        self.validate()
    def validate(self):
        if self.name.strip()=="":
            raise ValueError("name cannot be empty")
        if len(self.mobile)!=10:
            raise ValueError("mobile number must be 10 digits")
        if not self.mobile.isdigit():
            raise ValueError("mobile number should contain only numbers")
        if not self.mobile[0] not in ("6789"):
            raise ValueError("mobile number should starts with 6,7,8,9")
        if "@." not in self.email:
            raise ValueError("invalid email")

class Booking:
    def __init__(self,bid,room_no,room_type,guest_mobile,checkin_date,checkout_date,guest_count,status,total_amount):
        self.booking_id=bid
        self.room_no=room_no
        self.room_type=room_type
        self.guest_mobile=guest_mobile
        self.checkin_date=checkin_date
        self.checkout_date=checkout_date
        self.guest_count=guest_count
        self.status=status
        self.total_amount=total_amount
    def check_in(self):
        if self.status!="CONFIRMED":
            raise e.InvalidStatusException("only confirmed booking is allowed to check_in")
        self.status="CHECKED_IN"
    def check_out(self):
        if self.status!="CHECKED_IN":
            raise e.InvalidStatusException("only checked_in booking can checked out")
        self.status="CHECKED_OUT"
    def cancel(self):
        if self.status!="CONFIRMED":
            raise e.InvalidStatusException("only confirmed candidates can cancel the booking")
        self.status="CANCELLED"
    def __str__(self):
        return (f"{self.booking_id}|{self.room_type}|{self.status}")


