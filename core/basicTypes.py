import typing as ty
import commons as comm
if ty.TYPE_CHECKING:
    import tok

ops = comm.ops


# def error(errType:)

class VRepresentClass:
    def __init__(self, val:ty.Any) -> None:
        self.val = val

class BaseForAll:
    def __init__(self) -> None:
        self.name= ''
        self.val = ''
        self.valSym = ''
    
    def size(self) -> int:
        return len(str(self.val))
    
    def __eq__(self, other:object) -> bool:
        try:
            # Raises AttributeError if the other object doesn't have __dict__ (i.e. is not an instance)
            getattr(object, '__dict__')
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False
    
    def __hash__(self) -> int:
        return hash(self.val)

class VType(BaseForAll):
    def __init__(self) -> None:
        super().__init__()
        self.name = "TYP"
    
    def __repr__(self) -> ty.Any:
        return repr(self.val)
    
    def __str__(self) -> str:
        return str(self.val)
    
    def __bool__(self) -> bool:
        return bool(self.val)
    
    def __int__(self) -> int|None:
        try:
            return int(self.val)
        except TypeError:
            return None
    
    def __float__(self) -> float|None:
        try:
            return float(self.val)
        except TypeError:
            return None


class VInt(VType):
    def __init__(self, val:int) -> None:
        super().__init__()
        self.name = "INT"
        self.val:int = int(val)
    
    def __int__(self) -> int:
        return self.val
    
    def __add__(self, other:ty.Any) -> "VInt|VFloat|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            if isinstance(other, VInt):
                return VInt(self.val + other.val)
            return VFloat(self.val + other.val)
        else:
            coreErr.invArgs(msg=f"Illegal operation with '+': {self}, {other}")
    
    def __sub__(self, other:ty.Any) -> "VInt|VFloat|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            if isinstance(other, VInt):
                return VInt(self.val - other.val)
            return VFloat(self.val - other.val)
        else:
            coreErr.invArgs(msg=f"Illegal operation with '-': {self}, {other}")
    
    def __mul__(self, other:ty.Any) -> "VInt|VFloat|VString|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            if isinstance(other, VInt):
                return VInt(self.val * other.val)
            return VFloat(self.val * other.val)
        
        elif isinstance(other, VString):
            return VString(self.val * other.val)
        
        else:
            coreErr.invArgs(msg=f"Illegal operation with '*': {self}, {other}")
    
    def __truediv__(self, other:ty.Any) -> "VFloat|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VFloat(self.val / other.val)
        else:
            coreErr.invArgs(msg=f"Illegal operation with '/': {self}, {other}")
    
    def __neg__(self) -> "VInt":
        return VInt(-self.val)
    
    def __eq__(self, other: object) -> "VBool|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VBool(float(self.val) == float(other.val))
        coreErr.invDataTypes(VOperator('=='), (self, other))
    
    def __ne__(self, other: object) -> "VBool|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VBool(float(self.val) != float(other.val))
        coreErr.invDataTypes(VOperator('!='), (self, other))
    
    def __lt__(self, other: object) -> "VBool|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VBool(float(self.val) < float(other.val))
        coreErr.invDataTypes(VOperator('<'), (self, other))
    
    def __gt__(self, other: object) -> "VBool|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VBool(float(self.val) > float(other.val))
        coreErr.invDataTypes(VOperator('>'), (self, other))
    
    def __le__(self, other: object) -> "VBool|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VBool(float(self.val) <= float(other.val))
        coreErr.invDataTypes(VOperator('<='), (self, other))
    
    def __ge__(self, other: object) -> "VBool|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VBool(float(self.val) >= float(other.val))
        coreErr.invDataTypes(VOperator('>='), (self, other))
    
    # def __cmp__(self, other:ty.Any, comp:str) -> bool|None:
    #     if comp in ('==', '!=', '>', '<', '>=', '<='):
    #         if isinstance(other, (VInt, VFloat, VBool)):
    #             return ops[comp](self.val, other.val)
    #         elif isinstance(other, VString):
    #             return ops[comp](self.val, ord(other.val))
    #     else:
    #         coreErr.invArgs(msg=f"Illegal comparison with '{comp}': {self}, {other}")


class VFloat(VType):
    def __init__(self, val:float) -> None:
        super().__init__()
        self.name = "FLOAT"
        self.val:float = float(val)
    
    def __float__(self) -> float:
        return self.val
    
    def __add__(self, other:ty.Any) -> "VFloat|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VFloat(self.val + other.val)
        else:
            print("Illegal operation with '+':", other)
    
    def __sub__(self, other:ty.Any) -> "VFloat|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VFloat(self.val - other.val)
        else:
            coreErr.invArgs(msg=f"Illegal operation with '-': {self}, {other}")
    
    def __mul__(self, other:ty.Any) -> "VFloat|VString|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VFloat(self.val * other.val)
        
        elif isinstance(other, VString):
            return VString(int(self.val) * other.val) if int(self.val) == self.val else None
        
        else:
            coreErr.invArgs(msg=f"Illegal operation with '*': {self}, {other}")
    
    # def __rmul__() might be needed for reverse multiplication of String and Float.
    # Seems like it is not needed.
    
    def __truediv__(self, other:ty.Any) -> "VFloat|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VFloat(self.val / other.val)
        else:
            coreErr.invArgs(msg=f"Illegal operation with '/': {self}, {other}")
    
    def __neg__(self) -> "VFloat":
        return VFloat(-self.val)
    
    def __eq__(self, other: object) -> "VBool|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VBool(float(self.val) == float(other.val))
        coreErr.invDataTypes(VOperator('=='), (self, other))
    
    def __ne__(self, other: object) -> "VBool|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VBool(float(self.val) != float(other.val))
        coreErr.invDataTypes(VOperator('!='), (self, other))
    
    def __lt__(self, other: object) -> "VBool|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VBool(float(self.val) < float(other.val))
        coreErr.invDataTypes(VOperator('<'), (self, other))
    
    def __gt__(self, other: object) -> "VBool|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VBool(float(self.val) > float(other.val))
        coreErr.invDataTypes(VOperator('>'), (self, other))
    
    def __le__(self, other: object) -> "VBool|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VBool(float(self.val) <= float(other.val))
        coreErr.invDataTypes(VOperator('<='), (self, other))
    
    def __ge__(self, other: object) -> "VBool|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VBool(float(self.val) >= float(other.val))
        coreErr.invDataTypes(VOperator('>='), (self, other))
    
    # def __cmp__(self, other:ty.Any, comp:str) -> bool|None:
    #     if comp in ('==', '!=', '>', '<', '>=', '<='):
    #         if isinstance(other, (VInt, VFloat, VBool)):
    #             return ops[comp](self.val, other.val)
    #         elif isinstance(other, VString):
    #             return ops[comp](self.val, ord(other.val))
    #     else:
    #         coreErr.invArgs(msg=f"Illegal comparison with '{comp}': {self}, {other}")


class VString(VType):
    def __init__(self, val:str) -> None:
        super().__init__()
        self.name = "STRING"
        self.val = str(val)
    
    def join(self, iter:list[ty.Self]|tuple[ty.Self]|set[ty.Self]|dict[ty.Self, ty.Any]) -> "VString":
        result = self.val
        for i in iter:
            if isinstance(i, ty.Self):
                result += i.val
        return VString(result)
    
    def length(self) -> int:
        return len(self.val)
    
    def replace(self, old:ty.Any, new:ty.Any, returnVal:bool=True) -> "VString|None":
        if (isinstance(old, VString) and isinstance(new, VString)):
            if returnVal:
                return VString(self.val.replace(old.val, new.val))
            self.val = self.val.replace(old.val, new.val)
        else:
            coreErr.invArgs(msg=f"Incorrect type of arguments for method \"replace\" of type \"VString\": {old}, {new}")
    
    def __add__(self, other:ty.Any) -> "VString|None":
        if isinstance(other, VString):
            return VString(self.val + other.val)
        else:
            coreErr.invArgs(msg=f"Illegal operation with '+': {self}, {other}")
    
    def __sub__(self, other:ty.Any) -> "VString|None":
        if isinstance(other, VString):
            copy = str(self.val)
            while copy != '':
                if (ind:=copy.find(other.val)) != -1:
                    copy = copy[ind:len(other.val)]
                    continue
                break
            return VString(copy)

        else:
            coreErr.invArgs(msg=f"Illegal operation with '-': {self}, {other}")
    
    def __mul__(self, other:ty.Any) -> "VString|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            if isinstance(other, VFloat):
                if not int(other.val) == other.val:
                    coreErr.invDataTypes(VOperator('*'), (self.val, other.val))
                    return
            return VString(self.val*int(other.val))
    
    def __truediv__(self, other:ty.Any) -> None:
        coreErr.invDataTypes(VOperator('/'), (self.val, other.val))
    
    def __neg__(self) -> None:
        coreErr.invDataTypes(VOperator('-'), (self.val,))
    
    def __cmp__(self, other:ty.Any, comp:str) -> bool|None:
        if comp in ('==', '!=', '>', '<', '>=', '<='):
            if isinstance(other, (VInt, VFloat, VBool)):
                return ops[comp](ord(self.val), other.val)
            elif isinstance(other, VString):
                return ops[comp](self.val, other.val)
        else:
            coreErr.invArgs(msg=f"Illegal comparison with '{comp}': {self}, {other}")

    def __str__(self) -> str:
        return self.val


class VBool(VType):
    def __init__(self, val:bool) -> None:
        super().__init__()
        self.name = "BOOL"
        self.val = bool(val)
    
    def __bool__(self) -> bool:
        return self.val
    
    def __add__(self, other:ty.Any) -> "VBool|VFloat|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            if isinstance(other, VBool):
                # bool() required here as Python returns int for Boolean addition
                return VBool(bool(self.val + other.val))
            return VFloat(self.val + other.val)
        else:
            print(f"Illegal operation with '+': {self}, {other}")
    
    def __sub__(self, other:ty.Any) -> "VBool|VFloat|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            if isinstance(other, VBool):
                # bool() required here as Python returns int for Boolean subtraction
                return VBool(bool(self.val - other.val))
            return VFloat(self.val - other.val)
        else:
            coreErr.invArgs(msg=f"Illegal operation with '-': {self}, {other}")
    
    def __mul__(self, other:ty.Any) -> "VFloat|VString|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VFloat(self.val * other.val)
        
        elif isinstance(other, VString):
            return VString(self.val * other.val)
        
        else:
            coreErr.invArgs(msg=f"Illegal operation with '*': {self}, {other}")
    
    def __truediv__(self, other:ty.Any) -> "VFloat|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VFloat(self.val / other.val)
        else:
            coreErr.invArgs(msg=f"Illegal operation with '/': {self}, {other}")
    
    def __neg__(self) -> VInt:
        return VInt(-int(self.val))
    
    def __eq__(self, other: object) -> "VBool|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VBool(float(self.val) == float(other.val))
        coreErr.invDataTypes(VOperator('=='), (self, other))
    
    def __ne__(self, other: object) -> "VBool|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VBool(float(self.val) != float(other.val))
        coreErr.invDataTypes(VOperator('!='), (self, other))
    
    def __lt__(self, other: object) -> "VBool|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VBool(float(self.val) < float(other.val))
        coreErr.invDataTypes(VOperator('<'), (self, other))
    
    def __gt__(self, other: object) -> "VBool|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VBool(float(self.val) > float(other.val))
        coreErr.invDataTypes(VOperator('>'), (self, other))
    
    def __le__(self, other: object) -> "VBool|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VBool(float(self.val) <= float(other.val))
        coreErr.invDataTypes(VOperator('<='), (self, other))
    
    def __ge__(self, other: object) -> "VBool|None":
        if isinstance(other, (VInt, VFloat, VBool)):
            return VBool(float(self.val) >= float(other.val))
        coreErr.invDataTypes(VOperator('>='), (self, other))
    
    # def __cmp__(self, other:ty.Any, comp:str) -> bool|None:
    #     if comp in ('==', '!=', '>', '<', '>=', '<='):
    #         if isinstance(other, (VInt, VFloat, VBool)):
    #             return ops[comp](self.val, other.val)
    #         elif isinstance(other, VString):
    #             return ops[comp](self.val, ord(other.val))
    #     else:
    #         coreErr.invArgs(msg=f"Illegal comparison with '{comp}': {self}, {other}")


# TODO: Not yet used. Improve, then add to lexer (or parser?)
class VNull(VType):
    def __init__(self) -> None:
        super().__init__()
        self.name = "NULL"
        self.val  = None


class VKeyWd(VType):
    def __init__(self, val:str) -> None:
        super().__init__()
        self.name = "KEYWD"
        self.val  = val


class VIdent(VType):
    def __init__(self, name:str, typ:"tok.TokenTypes|None"=None, val:ty.Any=None) -> None:
        super().__init__()
        self.name = name
        self.typ  = typ
        self.val  = val
    
    def size(self) -> int:
        return len(str(self.name))


class VInvalid(VType):
    def __init__(self, val:ty.Any) -> None:
        super().__init__()
        self.name = "INV"
        self.val  = val


class VOperator(BaseForAll):
    def __init__(self, val:str) -> None:
        super().__init__()
        self.name   = "OP"
        self.valSym = str(val)
        self.val    = ops[str(val)]    # Might need to be changed! Take a look if there are any errors related to it!
    
    def __repr__(self) -> ty.Any:
        return repr(self.val)
    
    def __str__(self) -> str:
        return str(self.valSym)


class VAssign(BaseForAll):
    def __init__(self, val:str) -> None:
        super().__init__()
        self.name = "ASSIGN"
        self.val  = val
    
    def __repr__(self) -> ty.Any:
        return repr(self.val)
    
    def __str__(self) -> str:
        return str(self.val)


class VSymbol(BaseForAll):
    def __init__(self, val:str) -> None:
        super().__init__()
        self.name = "SYM"
        self.val  = val
    
    def __repr__(self) -> str:
        return repr(self.val)
    
    def __str__(self) -> str:
        return str(self.val)


class VAttribute(BaseForAll):
    def __init__(self, val:str) -> None:
        super().__init__()
        self.name = "ATTR"
        self.val  = val
    
    def __repr__(self) -> str:
        return repr(self.val)
    
    def __str__(self) -> str:
        return str(self.val)


class VSeparator(BaseForAll):
    def __init__(self, val:str) -> None:
        super().__init__()
        self.name = "SEP"
        self.val  = val
    
    def __repr__(self) -> str:
        return repr(self.val)
    
    def __str__(self) -> str:
        return str(self.val)


class VProgDecl(BaseForAll):
    def __init__(self, val:str) -> None:
        super().__init__()
        self.name = "PROGDECL"
        self.val  = val
    
    def __repr__(self) -> str:
        return repr(self.val)
    
    def __str__(self) -> str:
        return str(self.val)


class VEOF(BaseForAll):
    def __init__(self, val:str) -> None:
        super().__init__()
        self.name = "EOF"
        self.val  = val
    
    def __repr__(self) -> str:
        return repr(self.val)
    
    def __str__(self) -> str:
        return str(self.val)


class coreErr:
    class invArgs:
        def __init__(self, msg:str|None=None, *args:ty.Any) -> None:
            self.metatyp = "core"
            self.msg     = f"{self.metatyp}.{self.__class__.__name__}: Invalid arguments to operation function: {str(args)[1:-1]}" if msg is None else msg
            print(self.msg)
        
        def __str__(self) -> str:
            return self.msg
    
    class invDataTypes:
        def __init__(self, operation:VOperator, operands:tuple[ty.Any, ...], msg:str|None=None, *args:ty.Any) -> None:
            self.metatyp = "core"
            self.msg     = f"{self.metatyp}.{self.__class__.__name__}: Invalid data types for operation \'{operation}\': {str(operands)[1:-1]}" if msg is None else msg
            print(self.msg)
        
        def __str__(self) -> str:
            return self.msg
    
    # class zeroDivErr:
    #     def __init__(self, operands:tuple[ty.Any, ...], msg:str|None=None, *args:ty.Any) -> None:
    #         self.metatyp = "core"
    #         self.msg     = f"{self.metatyp}.{self.__class__.__name__}: Division by zero: {operands}" if msg is None else msg
    #         print(self.msg)
        
    #     def __str__(self) -> str:
    #         return self.msg
