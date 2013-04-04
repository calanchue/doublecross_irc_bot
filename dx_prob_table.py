import random


def roll():
   return random.randrange(1,11)

def roll2dx(num_dice, cri_ceiling):
    num_cri_dice = 0
    ret = 0 
    for i in xrange(num_dice):
        r = roll()
        ret = max(ret, r)
        if r >= cri_ceiling :
            num_cri_dice+=1
    if num_cri_dice > 0:
        return 10 + roll2dx(num_cri_dice, cri_ceiling)
    return ret

def roll2dx_print(num_dice, cri_ceiling):
    num_cri_dice = 0
    ret = 0 
    for i in xrange(num_dice):
        r = roll()
        print r,
        ret = max(ret, r)
        if r >= cri_ceiling :
            num_cri_dice+=1
    if num_cri_dice > 0:
        print '=>', num_cri_dice
        return 10 + roll2dx(num_cri_dice, cri_ceiling)
    print '#',ret
    return ret

for i in xrange(2,11):
    print i ,
print ''

dice_range = [i in range(2,11)]

base_format ="{:>15}"
row_format =base_format * (len(dice_range) + 1)
print row_format.format("", *dice_range)

dice_range = [i in range(2,11)]
"""
for i in xrange(10):
    roll2dx_print(10,10) 
    """

for cri_ceiling in xrange(6, 11): # cri_ceiling
    #print base_format.format(cri_ceiling),
    print cri_ceiling,'|',
    for num_dice in xrange(2,11): # num_dice
        #print "num_dice %d" % num_dice
        total = 0
        num_at_value = {}
        for i in xrange(10000) : #execution
            total += roll2dx(num_dice, cri_ceiling)
            num_at_value[total/10] 

        #print base_format.format(total/10000.0),           
        print total/10000.0, 
    print ''

