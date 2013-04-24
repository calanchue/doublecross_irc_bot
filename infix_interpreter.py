# -*- coding:utf-8 -*-
'''
Created on 2013. 4. 24.

@author: Hwang-JinHwan
'''
import random
import re
import traceback

class CalHistory:
    def __init__(self):
        self.history = []
    def append(self, line):
        self.history.append(line)
    def __repr__(self):
        #print self.history
        return "\n".join(self.history)

class ExpElement:
    def __init__(self, value, type):
       self.value = value
       self.type = type
    
    def __repr__(self):
        return "(value : %s, type : %s)" % (self.value, self.type)
    def __trunc__(self):
        return self.value

class EType:
    ROP = 1  # rolling operator
    DTYPE = 2  # dice type
    NUMBER = 3  # number
    NOP = 4  # number operator
    
class Dice:
    def __init__(self, min, max):
        self.min = min
        self.max = max
    def roll(self):
        return random.randrange(self.min, self.max + 1)

OPERATORS = "+-*/()dmM"
PRIORITY = {'(' :-1, '+' : 0, '-' : 0, '*' : 1, '/' : 1, 'd':2, 'm':2, 'M':2 }
def infixToPostfix(infixExp):
    # tokenizing
    tokenized_exp = []
    pattern = re.compile(r"\s*(?:(?P<rop>d|m|M)|(?P<dtype>f)|(?P<number>[0-9]+)|(?P<nop>\+|\-|\*|\/|\(|\)))")
    scan = pattern.scanner(infixExp)
    while 1:
        m = scan.match()
        if not m:
            break
        tokenized_exp.append(ExpElement((m.group(m.lastindex)), m.lastindex))
    # print "tokenized", tokenized_exp
    s = []
    postfix_exp = []
    for el in tokenized_exp:
        if el.type in (EType.NUMBER, EType.DTYPE):
            postfix_exp.append(el)
        elif el.type in (EType.NOP, EType.ROP):
            if not s:                
                s.append(el)
            else:
                if el.value == ')':
                    while (s) and (s[-1].value != '('):
                        postfix_exp.append(s.pop())
                    s.pop()
                elif el.value == '(':
                    s.append(el)
                else:
                    while s and PRIORITY[s[-1].value] >= PRIORITY[el.value]:
                        postfix_exp.append(s.pop())
                    s.append(el)
        else :
            raise Exception, "can't handle"
    while s:
        postfix_exp.append(s.pop())
    return postfix_exp

def create_dice_func(dice_type):
    if dice_type == "f" or dice_type == "F":
        return lambda:random.randrange(0, 3) - 1
    elif isinstance(dice_type, int):
        return lambda:random.randrange(1, dice_type + 1)
    else:
        print "inappropriate dice : %s" % dice_type

class Calculation:
    def __init__(self, expr):
        self.input_exp = expr
        self.history = CalHistory()
        self.solved = False
    
    def __dice_total(self, roll, dice_type):
        roll_dice = create_dice_func(dice_type)
        dice_res = []
        total = 0
        for i in xrange(roll):
            value = roll_dice() 
            dice_res.append(value)
            total += value
        his = "%sd%s : %s, %s" % (roll, dice_type, total, dice_res)
        self.history.append(his)
        print his
        return total
    
    def __dice_max(self, roll, dice_type):
        roll_dice = create_dice_func(dice_type)
        dice_res = []
        max = roll_dice()
        dice_res.append(max)
        for i in xrange(roll - 1):
            value = roll_dice() 
            dice_res.append(value)
            if value > max:
                max = value
        his = "%sM%s: %s, %s" % (roll, dice_type, max, dice_res)
        self.history.append(his)
        print his
        return max
    
    def __dice_min(self, roll, dice_type):
        roll_dice = create_dice_func(dice_type)
        dice_res = []
        min = roll_dice() 
        dice_res.append(min)
        for i in xrange(roll - 1):
            value = roll_dice()
            dice_res.append(value)
            if value < min:
                min = value
        his = "%sm%s : %s, %s" % (roll, dice_type, min, dice_res)
        self.history.append(his)
        print his
        return min
    
    def __calculate(self, postfix_exp):
        s = []
        for el in postfix_exp:
            if(el.type in (EType.DTYPE, EType.NUMBER)):
                s.append(el)
            else:
                if(el.type is EType.ROP):
                    r_el = s.pop()
                    if r_el.type is EType.NUMBER:
                        r = int(r_el.value)
                    else :
                        r = r_el.value
                    l = int(s.pop().value)
                elif(el.type is EType.NOP):
                    r = int(s.pop().value)
                    l = int(s.pop().value)
                
                if  el.value == "+":
                    res = l + r
                elif el.value == "-":
                    res = l - r
                elif el.value == "*":
                    res = l * r
                elif el.value == "/":
                    res = l / r
                elif el.value == 'd':
                    res = self.__dice_total(l, r) 
                elif el.value == "m":
                    res = self.__dice_min(l, r)
                elif el.value == "M":
                    res = self.__dice_max(l, r)
                s.append(ExpElement(res, EType.NUMBER))
                
        fin_res = s.pop()
        his = "[RESULT]%s -> %s" %(self.input_exp, fin_res.value)
        self.history.append(his)
        return fin_res
        
    def solving_history(self):
        if not self.solved:
            try : 
                self.fin_res = self.__calculate(infixToPostfix(self.input_exp))
            except Exception, e:
                traceback.print_exc()
                self.history.append(e.__repr__())
            self.solved = True
        return self.history.__repr__()

def solve_expr(expr):
    return Calculation(expr).solving_history()

def interactive_service():
    prev_exp = None
    while 1 :
        infixExp = raw_input("Enter a infix experssion:")
        if len(infixExp) == 0 and prev_exp is not None: 
            infixExp = prev_exp
        elif len(infixExp) == 0 and prev_exp is None:
            raise Exception, "can't handle"
        prev_exp = infixExp
        postfixExp = infixToPostfix(infixExp)
        print postfixExp
        print calculate(postfixExp)

def __test():
    res = solve_expr("9M6+4")
    print "="*30
    print res
    

if __name__ == '__main__':
    __test()
    
    
