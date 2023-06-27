import abc

from MacroDefine import (
    QUESTION_CONTENT_SOURCE, QUESTION_NEED_PAGE_RANGE, QUESTION_PAGE_START, QUESTION_PAGE_END, QUESTION_WRITE_DATA,
    INPUT_USER_ID, INPUT_USER_PASSWORD, INPUT_CONTENT_SOURCE, INPUT_NEED_PAGE_RANGE, INPUT_WRITE_DATA, QUESTION_KEYWORD
)


def ask(question='', inputText='', numSelect=3, defaultSelect=0):
    if question:
        print(question)
    try:
        ret = input(inputText)
    except EOFError:
        return 0

    if numSelect > 0:
        ans = getSelection(ret, numSelect, defaultSelect)
    else:
        ans = ret
    return ans


def getSelection(_input, numSelect=3, defaultSelect=0):
    try:
        ans = int(_input)
        if 1 <= ans <= numSelect:
            return ans
        else:
            return numSelect + 1
    except (TypeError, ValueError):
        return numSelect + 1


class UIProxy(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def askContentSource(self):
        return NotImplemented

    @abc.abstractmethod
    def askPageRange(self):
        return NotImplemented

    @abc.abstractmethod
    def askWriteData(self):
        return NotImplemented

    @abc.abstractmethod
    def askKeyWord(self):
        return NotImplemented

    @abc.abstractmethod
    def printMessage(self, messages=None):
        return NotImplemented


class MyUIProxy(UIProxy, BaseException):
    def __init__(self):
        UIProxy.__init__(self)
        pass

    def askContentSource(self):
        while True:
            ret = ask(QUESTION_CONTENT_SOURCE, INPUT_CONTENT_SOURCE)
            if ret == 0:
                print('You input an invalid option, please try again')
            else:
                break

        return ret
    
    def askUserId(self):
        ret = ask(inputText=INPUT_USER_ID, numSelect=0)
        if not ret:
            print('Empty user id, end program')
        return ret
    
    def askUserPassword(self):
        ret = ask(inputText=INPUT_USER_PASSWORD, numSelect=0)
        if not ret:
            print('Empty user password, end program')
        return ret

    def askPageRange(self, numPage=1):
        while True:
            ret = ask(QUESTION_NEED_PAGE_RANGE, INPUT_NEED_PAGE_RANGE, numSelect=2)
            if ret == 0:
                print('You input an invalid option, please try again')
            else:
                break

        pageStart = 1
        pageEnd = -1
        print('Total page number is %d' % numPage)

        if ret == 1:
            try:
                while True:
                    ret = int(input(QUESTION_PAGE_START))
                    if ret < 1 or ret > numPage:
                        print('You input an invalid option, please try again')
                    else:
                        pageStart = ret
                        break
            except (TypeError, EOFError):
                print('Something wrong, set the start page as 1')
                pageStart = 1

            try:
                while True:
                    ret = int(input(QUESTION_PAGE_END))
                    if ret < pageStart or ret > numPage:
                        print('You input an invalid option, please try again')
                    else:
                        pageEnd = ret
                        break
            except (TypeError, EOFError):
                print('Something wrong, set the end page as the last page')
                pageEnd = -1

        return pageStart, pageEnd

    def askWriteData(self):
        while True:
            ret = ask(QUESTION_WRITE_DATA, INPUT_WRITE_DATA)
            if ret == 0:
                print('You input an invalid option, please try again')
            else:
                break

        return True if ret == 1 else False

    def askKeyWord(self):
        ret = ask(QUESTION_KEYWORD, '', 0)

        return ret

    def printMessage(self, messages=None):
        if isinstance(messages, list):
            for message in messages:
                print(message)
        elif isinstance(messages, str):
            print(messages)

    def showContents(self, dicResult):
        if not dicResult:
            print('No content')
        
        lsFloor = [int(floor) for floor in list(dicResult.keys())]
        lsFloor.sort()
        numPage = len(lsFloor) // 10 + (len(lsFloor) % 10 != 0)

        for i in range(numPage):
            for count in range(10):
                if i * 10 + count >= len(lsFloor):
                    break;
                
                floor = lsFloor[i * 10 + count]
                print('#%s:' % floor)
                print(dicResult[str(floor)])
                print()
            if i < numPage - 1:
                ret = 0
                while True:
                    ret = ask('Do you want to show the next 10 results?', 'Press the related number to select, YES(1) / no(2): ', numSelect=2, defaultSelect=1)
                    if ret != 1 and ret != 2:
                        self.printMessage('You input an invalid option, please try again')
                    else:
                        break
                
                if ret == 2:
                    self.printMessage()
                    break
            else:
                self.printMessage('All results showed')
        
        print()
