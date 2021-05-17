import multiprocessing as np
from automation.auto_script import AutoScript


def main():
    for device in AutoScript.getphonelist():
        p = np.Process(target=AutoScript.run, args=(device,))
        p.start()


if __name__ == '__main__':
    # 当mumu模拟器无法被adb devices发现时，执行adb kill-server
    main()

