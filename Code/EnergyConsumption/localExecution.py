def run(users): 
    energy = 0
    count = 0
    for u in users.index:
        loc_time = users['cycles_req'][u]/users['cap'][u]
        if (loc_time <=  users['deadline'][u]):
            energy = energy + loc_time*users['compPow'][u]
            count = count + 1
    return energy,count
        