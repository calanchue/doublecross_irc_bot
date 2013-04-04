dice_type = 10
max_num_dice = 10

# num_dice x targe_num table (max will be value)
ndtn_table = [[None for x in xrange(dice_type+1)] for x in xrange(max_num_dice+1)]
for i in xrange(1, dice_type+1):
    ndtn_table[i] = 0.1 

    

def init_ndtn(num_dice):
    if num_dice == 1:
        return [0.1 for i in range(dice_type)]
    else:
        p_list = [0 for x in xrange(11)]
        for x in in range(1, dice_type+1):
            for y in range(1, dice_type+1):
                p_list[max(x,y)] += 0.1*get_p(num_dice-1, y)
        ndtn_table[num_dice] = p_list

def get_p(num_dice, target_num):
    return ndtn[num_dice+1][target_num+1]

def get_p_above(num_dice, ceiling):
    p =0;
    for i in xrange(ceiling, dice_type+1)
        p += get_p(num_dice, i)
    return p
            
def get_ex_value(num_dice):
    for i in xrange(1, dice_type+1)
        exp_value += i * get_p(num_dice, i)
    return exp_value

def get_ex_value_above(num_dice, ceiling):
    ex_v =0; # expected value
    for i in xrange(ceiling, dice_type+1)
        ex_v += i * get_p(num_dice, i)
    return ex_v 

def get_ex_value_with_cirtical(num_dice, c_num):
    return get_ex_value + get_p_above * get_ex_value

