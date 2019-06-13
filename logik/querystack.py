from logik import Kohortenabfrage as kh
class Querystack:

    __instance=None

    @staticmethod
    def getInstance():
        if Querystack.__instance == None:
            Querystack()

        return Querystack.__instance

    def __init__(self):
        if Querystack.__instance != None:
            raise Exception

        else:
            self.__stack=[kh.Kohortenabfrage(kriterien=[],verknüpfungen=[],flag_push=False)]
            Querystack.__instance = self

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

    def bottom(self):
        if self.__stack==[]:
            return None
        else:
            return self.__stack[0]