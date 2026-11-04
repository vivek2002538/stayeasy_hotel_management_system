class StayEasyException(Exception): 
    pass
class InvalidDateException(StayEasyException):
    pass
class RoomUnavailableException(StayEasyException):
    pass
class InvalidStatusException(StayEasyException):
    pass
class BookingNotFoundException(StayEasyException):
    pass
