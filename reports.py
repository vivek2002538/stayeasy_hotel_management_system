from datetime import datetime,timedelta
import sqlite3

def occupancy_report(db_name,start_date,end_date):
    con=sqlite3.connect(db_name)
    cursor=con.cursor()

    start=datetime.strptime(start_date,"%d-%m-%Y")
    end=datetime.strptime(end_date,"%d-%m-%Y")

    current_date=start
    total_rooms=0
    cursor.execute(""" select count(distinct room_no) from bookings""")
    data=cursor.fetchone()
    if data[0]:
        total_rooms=data[0]

    average=0
    days=0
    while current_date<=end:
        occupied=0

        cursor.execute("""select checkin_date,checkout_date,status
            from bookings
            where status in ('CONFIRMED','CHECKED_IN','CHECKED_OUT')""")
        bookings=cursor.fetchall()
        for i in bookings:
            checkin=datetime.strptime(i[0],"%d-%m-%Y")
            checkout=datetime.strptime(i[1],"%d-%m-%Y")
            if checkin<=current_date<checkout:
                occupied+=1
               
        percentage=0
        if total_rooms>0:
            percentage=(occupied/total_rooms)*100
        print(current_date.strftime("%d-%m-%Y"),occupied,total_rooms,round(percentage,2))
        average+=percentage
        days+=1

        current_date+=timedelta(days=1)
    if days>0:
        print("Average occupancy:",round(average/days,2),"%")
    con.close()

def revenue_report(db_name):
    con=sqlite3.connect(db_name)
    cursor=con.cursor()
    room_types=["standard","deluxe","suite"]
    for i in room_types:
        cursor.execute("""select count(*),sum(total_amount),sum(refund)
            from bookings
            where room_type=? and status='CHECKED_OUT' """,(i,))
        data=cursor.fetchone()
        stays=data[0]
        revenue=data[1]
        refund=data[2]

        if revenue is None:
            revenue=0
        if refund is None:
            refund=0
        gst=revenue*0.12
        print("room_type:",i)
        print("Completed_stays:",stays)
        print("revenue:",revenue)
        print("GST:",gst)
        print("Refund_amount:",round(refund,2))
    con.close()



    