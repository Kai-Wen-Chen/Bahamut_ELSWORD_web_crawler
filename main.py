from WebCrawler import MyWebCrawler


if __name__ == '__main__':
    myWebCrawler = MyWebCrawler()
    while True:
        myWebCrawler.start()
        cmd = input('Input 0 to end program\n')

        if cmd == '0':
            break
