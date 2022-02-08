def run(users,task_deadline):
    energy_rand_alloc = []
    for i in task_deadline:   
        count = 0
        for u in users.index:
            loc_time = users['cycles_req'][u]/users['cap'][u]
            if (loc_time <= i):
                count = count + 1
        energy_rand_alloc.append(count)   
    return energy_rand_alloc 