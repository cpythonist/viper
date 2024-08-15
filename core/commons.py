import operator
import typing as ty

import other as ot

ANSI = ot.isANSISupported()
ops = {
    '+': operator.add,
    '-': operator.sub,
    '-': operator.neg,
    '*': operator.mul,
    '/': operator.truediv,
    '^': operator.pow,
    '//': operator.floordiv,
    '%': operator.mod,
    '==': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge,
    '+=': operator.iadd,
    '-=': operator.isub,
    '*=': operator.imul,
    '/=': operator.itruediv,
}


class Stack:
    def __init__(self, initVals:list[tuple[ty.Any, ...]]=[], unique:bool=False) -> None:
        self.stack:list[tuple[ty.Any, ...]] = initVals
        self.unique:bool = unique
    
    def push(self, val:tuple[ty.Any, ...]) -> None:
        if self.unique:
            for i in range(self.length()):
                if self.stack[i][0] == val[0]:
                    self.stack.pop(i)
                    self.stack.insert(i, val)
                    break
            else:
                self.stack.insert(0, val)
            
        else:
            self.stack.insert(0, val)
    
    def pop(self) -> tuple[ty.Any, ...]:
        return self.stack.pop()
    
    def peek(self) -> tuple[ty.Any, ...]:
        return self.stack[0]
    
    def length(self) -> int:
        return len(self.stack)
    
    def __list__(self) -> list[tuple[ty.Any, ...]]:
        return self.stack
    
    def __str__(self) -> str:
        return str(self.stack)


class Queue:
    def __init__(self, initVals:list[tuple[ty.Any, ...]]=[]) -> None:
        self.queue:list[tuple[ty.Any, ...]] = initVals
    
    def add(self, vals:list[tuple[ty.Any, ...]]) -> None:
        for val in vals:
            self.queue.append(val)
    
    def get(self, name:ty.Any):
        for i in self.queue:
            if i[0] == name:
                return i
    
    def __list__(self) -> list[tuple[ty.Any, ...]]:
        return self.queue
    
    def length(self) -> int:
        return len(self.queue)
    
    # def modify(self, name:str, typ:ty.Any|None=None, val:ty.Any|None=None) -> None:
    #     if name in self.names():
    #         changed = self.get(name)

    
    def zeroes(self):
        return [i[0] for i in self.queue]
    
    def ones(self):
        return [i[1] for i in self.queue]
    
    def twos(self):
        return [i[2] for i in self.queue]
    
    def __str__(self) -> str:
        return str(self.queue)
