from datetime import datetime
import sqlite3
import sys
import os
from database import *
from models import *
from reports import *
from pricing import *

if len(sys.argv)>1:
    db_name=sys.argv[1]
else:
    db_name="stayeasy.db"

create_tables(db_name)
rooms=[]
room_numbers=[]
try:
    with open("app.log","a") as log,open("rooms.csv","r") as file:
        next(file)
        for i in file:
            line=i.strip().split(",")
            room_no=int(line[0])
            room_type=line[1]
            floor=int(line[2])

            if room_type not in ("Standard","Suite","Deluxe"):
                log.write(f"Invalid Room Type: {i}")
                continue
            if room_no in room_numbers:
                log.write(f"Duplicate room: {i}")
                continue
            room_numbers.append(room_no)
            rooms.append([room_no,room_type,floor])       
except FileNotFoundError:
    print("rooms.csv is not found")
total_rooms=len(rooms)

def get_available_rooms(room_type,checkin_date,checkout_date):
        checkin=datetime.strptime(checkin_date,"%d-%m-%Y")
        checkout=datetime.strptime(checkout_date,"%d-%m-%Y")
        
        available_rooms=[]
        con=sqlite3.connect(db_name)
        cursor=con.cursor()
        for i in rooms:
            room_no=i[0]
            if i[1].lower()!=room_type.lower():
                continue
            cursor.execute(""" select checkin_date,checkout_date
                from bookings
                where room_no=? and status in ('CHECKED_IN','CONFIRMED')
                """,(room_no,))
            bookings=cursor.fetchall()
            available=True
            for i in bookings:
                old_checkin=datetime.strptime(i[0],"%d-%m-%Y")
                old_checkout=datetime.strptime(i[1],"%d-%m-%Y")
                if (checkin<old_checkout and checkout>old_checkin):
                    available=False
                    break
            if available:
                available_rooms.append(room_no)
        con.close()
        available_rooms.sort()
        return available_rooms

while True:
    print("====stay easy hotel====")
    print("1.search room availability")
    print("2.create booking")
    print("3.check in")
    print("4.check out")
    print("5.cancel booking")
    print("6.view booking details")
    print("7.guest stay history")
    print("8.occupancy report")
    print("9.revenue report")
    print("10.export all bookings to CSV")
    print("11.exit")

    option=input("enter your option (1 to 11): ")

    if option=="1":
        room_type=input("enter room type: ")
        checkin_date=input("enter checkin date: ")
        checkout_date=input("enter checkout date: ")
        try:
            checkin=datetime.strptime(checkin_date,"%d-%m-%Y")
            checkout=datetime.strptime(checkout_date,"%d-%m-%Y")
        except ValueError:
            print("invalid date format")
            continue
        if checkout<=checkin:
            print("checkout date must be after checkin date")
            continue
        available_rooms=get_available_rooms(room_type,checkin_date,checkout_date)
        if len(available_rooms)==0:
            print("no rooms available")
        else:
            print("Available Rooms:",available_rooms)
    elif option=="2":
        name=input("enter name: ")
        mobile=input("enter mobile number: ")
        email=input("enter email: ")
        room_type=input("enter room type: ")
        guest_count=int(input("enter number of guest: "))
        limits={"standard":2,"deluxe":3,"suite":4}
        if room_type.lower() not in limits:
            print("invalid room type")
            continue
        if guest_count>limits[room_type.lower()]:
            print("guest count exceeds room limit")
            continue
        checkin_date=input("enter checkin date: ")
        checkout_date=input("enter checkout date: ")
        try:
            checkin=datetime.strptime(checkin_date,"%d-%m-%Y")
            checkout=datetime.strptime(checkout_date,"%d-%m-%Y")
        except ValueError:
            print("invalid date format")
            continue
        if checkout<=checkin:
            print("checkout date must be after checkin date")
            continue
        available_rooms=get_available_rooms(room_type,checkin_date,checkout_date)
        if len(available_rooms)==0:
            print("no rooms available")
        else:
            guest=Guest(name,mobile,email)
            add_guest(db_name,guest)
            completed=completed_stays(db_name,mobile)
            amount=calculate_TotalAmount(room_type,guest_count,checkin_date,checkout_date,completed)
            room_no=available_rooms[0]
            booking=Booking(None,room_no,room_type,mobile,checkin_date,checkout_date,guest_count,"CONFIRMED",amount["total_amount"],amount["total_gst"])
            add_booking(db_name,booking)
            print("booking created successfully")
            print("allocated: ",room_no)
            print("total amount: ",amount["total_amount"])
        
    elif option=="3":
        booking_id=int(input("enter booking id: "))
        booking=get_booking(db_name,booking_id)
        if booking is None:
            print("booking not found")
        else:
            checkin_date=booking[4]
            status=booking[7]
            today=datetime.today().strftime("%d-%m-%Y")
            if status!="CONFIRMED":
                print("only confirmed booking can check in")
            elif today!=checkin_date:
                print("check in is allowed only on checkin date")
            else:
                update_status(db_name,booking_id,"CHECKED_IN")
                print("check in successfull")
    elif option=="4":
        booking_id=int(input("enter booking id: "))
        booking=get_booking(db_name,booking_id)
        if booking is None:
            print("booking not found")
        else:
            if booking[7]!="CHECKED_IN":
                print("only checked in booking can be checked out")
            else:
                update_status(db_name,booking_id,"CHECKED_OUT")
                if not os.path.exists("invoices"):
                    os.mkdir("invoices")
                with open(f"invoices/{booking_id}.txt","w") as file:
                    file.write(f"booking id: {booking_id}")
                    file.write(f"room no: {booking[1]}")
                    file.write(f"room type: {booking[2]}")
                    file.write(f"guest mobile: {booking[3]}")
                    file.write(f"checkin date:{booking[4]}")
                    file.write(f"check out date:{booking[5]}")
                    file.write(f"guest count:{booking[6]}")
                    file.write(f"total_amount:{booking[8]}")
                print("checked out successfully")
                print("invoice generated")

    elif option=="5":
        booking_id=int(input("enter the booking id: "))
        booking=get_booking(db_name,booking_id)
        if booking is None:
            print("no booking found")
        else:
            if booking[7]!="CONFIRMED":
                print("only confirmed booking can be cancelled")
            else:
                refund=calculate_refund(booking[8],booking[4])
                update_status(db_name,booking_id,"CANCELLED")
                update_refund(db_name,booking_id,refund) 
                print("booking cancelled")
                print("refund amount:",round(refund,2))
                
    elif option=="6":
        booking_id=int(input("enter booking id: "))
        booking=get_booking(db_name,booking_id)
        if booking is None:
            print("no booking found")
        else:
            print("\n booking details")
            for i in booking:
                print(i)
    elif option=="7":
        mobile=input("enter mobile number: ")
        data=guest_history(db_name,mobile)
        if len(data)==0:
            print("no booking history")
        else:
            for i in data:
                print(i)
    elif option=="8":
        start_date=input("enter start date: ")
        end_date=input("enter end date: ")
        occupancy_report(db_name,start_date,end_date,total_rooms)
    elif option=="9":
        revenue_report(db_name)
    elif option=="10":
        bookings=get_all_bookings(db_name)
        with open("bookings_export.csv","w") as file:
            file.write("booking_id,room_no,room_type,guest_mobile,checkin_date,checkout_date,guest_count,status,total_amount,gst,refund\n")
            for i in bookings:
                file.write(f"{i[0]},{i[1]},{i[2]},{i[3]},{i[4]},{i[5]},{i[6]},{i[7]},{i[8]},{i[9]},{i[10]}\n")
            print("bookings exported successfully")
    elif option=="11":
        print("thank you")
        break
    else:
        print("invalid option")



