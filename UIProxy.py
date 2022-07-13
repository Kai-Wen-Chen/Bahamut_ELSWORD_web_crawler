import abc

from MacroDefine import (
    QUESTION_CONTENT_SOURCE, QUESTION_NEED_PAGE_RANGE, QUESTION_PAGE_START, QUESTION_PAGE_END, QUESTION_WRITE_DATA,
    SELECTION_CONTENT_SOURCE, SELECTION_NEED_PAGE_RANGE, SELECTION_WRITE_DATA
)


def ask(question='', selection='', numSelect=3):
    print(question)
    try:
        ret = input(selection)
    except EOFError:
        return 0

    ans = getSelection(ret, numSelect)
    return ans


def getSelection(_input, numSelect=3):
    try:
        ans = int(_input)
        if 1 <= ans <= numSelect:
            return ans
    except TypeError:
        return 0


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


class MyUIProxy(UIProxy, BaseException):
    def __init__(self):
        UIProxy.__init__(self)
        pass

    def askContentSource(self):
        while True:
            ret = ask(QUESTION_CONTENT_SOURCE, SELECTION_CONTENT_SOURCE)
            if ret == 0:
                print('You input an invalid option, please try again')
            else:
                break

        return ret

    def askPageRange(self, numPage=1):
        while True:
            ret = ask(QUESTION_NEED_PAGE_RANGE, SELECTION_NEED_PAGE_RANGE, numSelect=2)
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
            ret = ask(QUESTION_WRITE_DATA, SELECTION_WRITE_DATA)
            if ret == 0:
                print('You input an invalid option, please try again')
            else:
                break

        return True if ret == 1 else False
