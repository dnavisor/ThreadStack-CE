import prprcedog
if __name__ == '__main__':
    pointerList = prprcedog.ThreadStackFinder.get_ce_thread_stack("HWorks32.exe")
    print("TopList", pointerList)
    print("over")
