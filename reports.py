from datetime import datetime, timedelta
import sqlite3

def occupancy_report(db_name, start_date, end_date, total_rooms):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()

    start = datetime.strptime(start_date,"%d-%m-%Y")
    end = datetime.strptime(end_date,"%d-%m-%Y")
    current_date = start
    total_percentage = 0
    total_days = 0

    print("="*50)
    while current_date <= end:
        cursor.execute("""select room_no,checkin_date,checkout_date
            from bookings
            where status!='CANCELLED'
            """)
        bookings = cursor.fetchall()
        occupied_rooms =[]

        for i in bookings:
            room_no = i[0]
            checkin = datetime.strptime(i[1],"%d-%m-%Y")
            checkout = datetime.strptime(i[2],"%d-%m-%Y")
            if checkin <=current_date<checkout:
                if room_no not in occupied_rooms:
                    occupied_rooms.append(room_no)
        occupied = len(occupied_rooms)
        percentage = 0
        if total_rooms > 0:
            percentage = (occupied /total_rooms)*100

        print(current_date.strftime("%d-%m-%Y"),occupied,total_rooms,round(percentage, 2))
        total_percentage += percentage
        total_days += 1

        current_date += timedelta(days=1)

    if total_days > 0:
        average = (total_percentage /total_days)
        print("Average Occupancy :",round(average, 2),"%")
    con.close()

def revenue_report(db_name):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    room_types = ["standard","deluxe","suite"]

    print("\n revenue report")
    print("="*50)
    for i in room_types:
        cursor.execute(""" select  count(*),sum(total_amount),sum(gst)
                        from bookings
                        where room_type=? and status='CHECKED_OUT' """, (i.lower(),))

        data = cursor.fetchone()
        completed_stays = data[0]
        room_revenue = data[1]
        gst_collected=data[2]
        if room_revenue is None:
            room_revenue = 0

        if gst_collected is None:
            gst_collected=0

        cursor.execute(""" select sum(total_amount-refund)
                        from bookings
                        where room_type=? and status='CANCELLED' """, (i.lower(),))
        cancelled_amount = cursor.fetchone()[0]

        if cancelled_amount is None:
            cancelled_amount = 0

        print("\nroom type:", i)
        print("Completed Stays: ",completed_stays)
        print("Room Revenue: ",round(room_revenue, 2))
        print("gst_collected: ",round(gst_collected,2))
        print("Amount Kept From Cancellations: ",round(cancelled_amount, 2))
    con.close()