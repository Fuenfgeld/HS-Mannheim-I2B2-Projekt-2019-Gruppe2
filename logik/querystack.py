class Querystack:

    def __init__(self):
        self.__stack=[]


    def peek(self):
        if self.__stack==[]:
            return None
        else:
            return self.__stack[-1]

    def pop(self):
        if self.__stack==[]:
            return None
        else:
            return self.__stack.pop()

    def push(self,new_query):
        self.__stack.append(new_query)

    def size(self):
        return len(self.__stack)