import uiautomator2 as u2
import subprocess
import time
import json
from db.redis_tool import RedisQueue


class AutoScript(object):
    """
    使用uiautomator2模拟
    """
    @staticmethod
    def getphonelist():  # 获取手机设备
        cmd = r'adb devices'
        pr = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        pr.wait()  # 不会马上返回输出的命令，需要等待
        out = pr.stdout.readlines()  # out = pr.stdout.read().decode("UTF-8")
        devices = []
        for i in (out)[1:-1]:
            device = str(i).split("\\")[0].split("'")[-1]
            devices.append(device)
        return devices  # 手机设备列表

    @staticmethod
    def run(device):  # 执行用例
        d = u2.connect(device)  # uiautomator2 连接手机
        AutoScript.MultiDevice2(d)

    @staticmethod
    def MultiDevice3(d):
        # 打开信息
        d.app_start('com.oneplus.mms')
        while True:
            time.sleep(5)
            phone = RedisQueue(name="user_passwd").get_nowait()
            if not phone:
                print("==========等待ing=========")
                continue
            user_passwd = json.loads(phone)

            # 点击发短信的按钮
            d(resourceId="com.oneplus.mms:id/start_new_conversation_button").click_exists(timeout=10)
            input_button = d(resourceId="com.oneplus.mms:id/recipient_scroll_view")
            if input_button.exists:
                print('点击输入框，输入电话号码')
                input_button.click()
                print(user_passwd)
                input_button.child().send_keys(user_passwd["phone"])
                d.press('enter')
            d(resourceId="com.oneplus.mms:id/contact_type").click_exists(timeout=1)

            send_message = d(resourceId="com.oneplus.mms:id/compose_message_text")
            if send_message.exists:
                send_message.click()
                send_message.send_keys("test")

            d.xpath('//*[@resource-id="com.oneplus.mms:id/bottom_panel"]/android.widget.LinearLayout[1]').click()

            time.sleep(4)
            d.press("back")
            time.sleep(1)
            d.press("back")

    @staticmethod
    def MultiDevice2(d):
        while True:
            time.sleep(5)
            user_passwd = RedisQueue(name="user_passwd").get_nowait()
            if not user_passwd:
                print("==========等待ing=========")
                continue
            user_passwd = json.loads(user_passwd)
            d.app_start('sogou.mobile.explorer')

            # 首先进入首页
            index = d(resourceId="sogou.mobile.explorer:id/aec")
            if index.exists(timeout=10):
                print("点击进入首页")
                index.click()

            search_input = d(resourceId="sogou.mobile.explorer:id/xp")
            if search_input.exists(timeout=10):
                print("点击搜索框")
                search_input.click()

            input_button = d(resourceId="sogou.mobile.explorer:id/s1")
            if input_button.exists(timeout=10):
                print("输入网址")
                input_button.click()
                input_button.send_keys('https://login.taobao.com/member/login.jhtml')

            enter = d(resourceId="sogou.mobile.explorer:id/a5o")
            if enter.exists(timeout=10):
                print("点击跳转按钮")
                enter.click()

            for _ in range(10):
                if d(resourceId="refresh").exists(timeout=5): d(resourceId="refresh").click()

            name_input = d(resourceId="fm-login-id")
            if name_input.exists(timeout=20):
                name_input.click()
                name_input.send_keys(user_passwd["user"])

            passwd_input = d(resourceId="fm-login-password")
            if passwd_input.exists(timeout=20):
                passwd_input.click()
                passwd_input.send_keys(user_passwd["passwd"])

            login_button = d(description="登录")
            if login_button.exists(timeout=10):
                login_button.click()

            for _ in range(10):
                time.sleep(2)
                if d(resourceId="sogou.mobile.explorer:id/ri").exists(5):
                    d(resourceId="sogou.mobile.explorer:id/ri").click()

            index_page = d(description="首页")
            if index_page.exists(timeout=20):
                index_page.click()

            d.app_stop('sogou.mobile.explorer')

    @staticmethod
    def MultiDevice(d):  # 功能执行
        d.screen_on()
        while True:
            time.sleep(5)
            user_passwd = RedisQueue(name="user_passwd").get_nowait()
            if not user_passwd:
                continue
            user_passwd = json.loads(user_passwd)
            print(user_passwd)

            d.app_start('com.taobao.taobao')
            time.sleep(10)

            for _ in range(10):
                time.sleep(2)
                search_butten = d.xpath(
                    '//*[@resource-id="com.taobao.taobao:id/sv_search_view"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.view.View[2]')
                if search_butten.exists:
                    search_butten.click()
                    break

            # 定位到搜索框
            search_input = d(resourceId="com.taobao.taobao:id/searchEdit")
            if search_input.exists(timeout=10):
                search_input.send_keys(user_passwd['user'])

            lianxiang = d(resourceId="com.taobao.taobao:id/keyword")
            if lianxiang.exists(timeout=10):
                for i in lianxiang:
                    print(i.get_text())
            # 关闭应用
            d.app_stop('com.taobao.taobao')

