water_time = 25
No_Water = False
from water import water
def reservoir(s):
    global water_time
    water_time = water_time - s
    print("Water_Time_Remaining", water_time)
    if water_time <0:
        return False
        print("No water")
    else:
        return True

def pump(time):
    global No_Water, water_time
    print("Water for:", time)
    if not No_Water and reservoir(time):
        water(time, "Yes")
        water(0, "No")
    else:
        if not No_Water :
            remaining = water_time % time
            print("Remaining time", remaining)
            water(remaining, "Yes")
            No_Water = True
            print("Water Empty")
            
    if No_Water:
        print(water_time, "Return to shelter")
        return False, water_time
    else:
        print(water_time, "Return to shelter")
        return True, water_time

    

    