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



pn = 10000.0 #process num
class CaseStat : #case statistic
    def __init__(self, total, occ_val):
        self.total = total
        self.occ_val = occ_val
    def __repr__(self):
        a = [self.total,]
        merged = a + self.occ_val
        divided = [x/pn for x in merged]
        converted = tuple(merged)
        return "%d(%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)" % converted

def show_prob_table():

    for i in xrange(2,11):
        print i ,
    print ''
    occ_max_value = 100 #occurence_polling_max_value = 100
    cri_dice_table = [[0 for i in xrange(2,20)] for i in xrange(6,11)]

    for cri_ceiling in xrange(6, 11): # cri_ceiling
        #print base_format.format(cri_ceiling),
        print cri_ceiling,'|',
        for num_dice in xrange(2,20): # num_dice
            #print "num_dice %d" % num_dice
            total = 0
            occ_val = [0 for i in xrange(occ_max_value/10)]# occurence of value
            for i in xrange(10000) : #execution
                value = roll2dx(num_dice, cri_ceiling)
                total += value 
                if total < occ_max_value:
                    occ_val[total/10] += 1
            #print base_format.format(total/10000.0),           
            print total/10000.0, 
            #cri_dice_table[cri_ceiling][num_dice] = CaseStat(total, occ_val)
            #print CaseStat(total,occ_val),
        print ''
    

if __name__ == '__main__':
    show_prob_table()
