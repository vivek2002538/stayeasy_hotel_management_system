from datetime import datetime,timedelta

def calculate_TotalAmount(room_type,guest_count,checkin_date,checkout_date,completed_stays):
    check_in=datetime.strptime(checkin_date,"%d-%m-%Y")
    check_out=datetime.strptime(checkout_date,"%d-%m-%Y")
    nights=(check_out-check_in).days
    if room_type.lower()=="standard":
        room_rate=2500
    elif room_type.lower()=="deluxe":
        room_rate=4000
    elif room_type.lower()=="suite":
        room_rate=7500
    total_room_amount=0
    total_extra_amount=0
    total_gst=0
    per_night=[]
    current_date=check_in
    while current_date<check_out:
        perDay=room_rate
        if current_date.strftime("%A") in("Friday","Saturday"):
            perDay=room_rate*1.2
        extra_charge=0
        if room_type.lower() in ("suite","deluxe"):
            if guest_count>2:
                extra_charge=800*(guest_count-2)
        day_total=perDay+extra_charge
        if day_total>7500:
            gst=18
        else:
            gst=12
        gst_amount=perDay*(gst/100)

        total_room_amount+=perDay
        total_extra_amount+=extra_charge
        total_gst+=gst_amount

        per_night.append([current_date.strftime("%d-%m-%Y"),perDay,extra_charge,gst_amount])
        current_date+=timedelta(days=1)

    long_discount=0
    if nights>=7:
        long_discount=total_room_amount*0.1

    loyalty_discount=0
    if completed_stays>=3:
        loyalty_discount=total_room_amount*0.05

    total_discount=long_discount+loyalty_discount
    total_amount=total_room_amount+total_extra_amount+total_gst-total_discount
    return {"nights":nights,
            "room_charge":round(total_room_amount,2),
            "extra_amount":round(total_extra_amount,2),
            "long_discount":round(long_discount,2),
            "loyalty_discount":round(loyalty_discount,2),
            "total_gst":round(total_gst,2),
            "total_amount":round(total_amount,2),
            "per_night_details":per_night}

def calculate_refund(total_amount,checkin_date):
    checkin=datetime.strptime(checkin_date,"%d-%m-%Y")
    days=(checkin-datetime.today()).days
    if days>=7:
        return total_amount
    elif 2<=days<=6:
        return total_amount*0.5
    else:
        return 0
