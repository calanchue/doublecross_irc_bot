# -*- coding:utf-8 -*-
'''
Created on 2013. 4. 24.

@author: Hwang-JinHwan
'''
import random
import re

class CalHistory:
    def __init__(self):
        pass
    def addHistory(self):
        pass

class ExpElement:
    def __init__(self, value, type):
       self.value = value
       self.type = type
    
    def __repr__(self):
        return "(value : %s, type : %s)" %(self.value, self.type)
    def __trunc__(self):
        return self.value

class EType:
    ROP = 1 # rolling operator
    DTYPE = 2 # dice type
    NUMBER = 3 # number
    NOP = 4 # number operator


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
    #print "tokenized", tokenized_exp
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

class Dice:
    def __init__(self, min, max):
        self.min = min
        self.max = max
    def roll(self):
        return random.randrange(self.min, self.max + 1)

def create_dice(dice_type):
    if dice_type == "f" or dice_type == "F":
        return Dice(-1, 1)
    elif isinstance(dice_type, int):
        return Dice(1, dice_type)
    else:
        print "inappropriate dice : %s" % dice_type
        

def dice_total(roll, dice_type):
    dice = create_dice(dice_type)
    dice_res = []
    total = 0
    for i in xrange(roll):
        value = dice.roll() 
        dice_res.append(value)
        total += value
    print "dice_total", total, dice_res
    return total

def dice_max(roll, dice_type):
    dice = create_dice(dice_type)
    dice_res = []
    max = dice.roll()
    for i in xrange(roll - 1):
        value = dice.roll() 
        dice_res.append(value)
        if value > max:
            max = value
    print "dice_max", dice_res, max
    return max

def dice_min(roll, dice_type):
    dice = create_dice(dice_type)
    dice_res = []
    min = dice.roll() 
    for i in xrange(roll - 1):
        value = dice.roll()
        dice_res.append(value)
        if value < min:
            min = value
    print "dice_min", dice_res, min
    return min

def calculate(postfix_exp):
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
                res = dice_total(l, r) 
            elif el.value == "m":
                res = dice_min(l, r)
            elif el.value == "M":
                res = dice_max(l, r)
            s.append(ExpElement(res, EType.NUMBER))
    return s.pop()

while 1 :
    infixExp = raw_input("Enter a infix experssion:")
    if len(infixExp) == 0: 
        print "lenght 0"
    postfixExp = infixToPostfix(infixExp)
    print postfixExp
    print calculate(postfixExp)
