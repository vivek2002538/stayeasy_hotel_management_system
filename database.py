import sqlite3

def create_tables(db_name):
    con=sqlite3.connect(db_name)
    cursor=con.cursor()
    cursor.execute(""" 
    create table if not exists guests(
        mobile text primary key,
        name text not null,
        email text not null)""")

    cursor.execute(""" 
    create table if not exists bookings(
    booking_id integer  primary key autoincrement,
    room_no integer not null ,
    room_type text not null ,
    guest_mobile text not null references guests(mobile),
    checkin_date text not null,
    checkout_date text not null,
    guest_count integer not null,
    status text not null,
    total_amount decimal not null,
    gst decimal default 0,
    refund decimal default 0) """)
    con.commit()
    con.close()

def add_guest(db_name,guest):
    con=sqlite3.connect(db_name)
    cursor=con.cursor()
    cursor.execute(""" 
    insert or ignore  into guests values(?,?,?)""",(guest.get_mobile(),guest.get_name(),guest.get_email()))
    con.commit()
    con.close()

def add_booking(db_name,booking):
    con=sqlite3.connect(db_name)
    cursor=con.cursor()
    cursor.execute("""insert into bookings(room_no,room_type,guest_mobile,checkin_date,checkout_date,guest_count,status,total_amount,gst,refund) values(?,?,?,?,?,?,?,?,?,?)""",
                  (booking.room_no,
                   booking.room_type,
                   booking.guest_mobile,
                   booking.checkin_date,
                   booking.checkout_date,
                   booking.guest_count,
                   booking.status,
                   booking.total_amount,
                   booking.gst,
                   0))
    con.commit()
    con.close()

def get_booking(db_name,booking_id):
    con=sqlite3.connect(db_name)
    cursor=con.cursor()
    cursor.execute(" select * from bookings where booking_id=?",(booking_id,))
    data=cursor.fetchone()
    con.close()
    return data

def update_status(db_name,booking_id,new_status):
    con=sqlite3.connect(db_name)
    cursor=con.cursor()
    cursor.execute("update bookings set status=? where booking_id=?",(new_status,booking_id))
    con.commit()
    con.close()

def update_refund(db_name,booking_id,refund_amount):
    con=sqlite3.connect(db_name)
    cursor=con.cursor()
    cursor.execute("update bookings set refund=? where booking_id=?",(refund_amount,booking_id))
    con.commit()
    con.close()

def guest_history(db_name,mobile):
    con=sqlite3.connect(db_name)
    cursor=con.cursor()
    cursor.execute("select * from bookings where guest_mobile=?",(mobile,))
    data=cursor.fetchall()
    con.close()
    return data

def get_all_bookings(db_name):
    con=sqlite3.connect(db_name)
    cursor=con.cursor()
    cursor.execute("select * from bookings")
    data=cursor.fetchall()
    con.close()
    return data

def completed_stays(db_name,mobile):
    con=sqlite3.connect(db_name)
    cursor=con.cursor()
    cursor.execute("""select count(*)
        from bookings
        where guest_mobile=? and status='CHECKED_OUT'
        """,(mobile,))
    count=cursor.fetchone()[0]
    con.close()
    return count


