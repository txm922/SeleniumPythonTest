# coding=utf-8
'''
Created on 2015年10月14日
1.スペースのメンバーが作成したスペースを閲覧できること
2.スペースの参加者以外も作成されたスペースを閲覧できること
@author: QLLU
'''
# 导入需要的公共函数类
import time, unittest, sys, os

sys.path.append("..")
sys.path.append(os.getcwd() + "/src/")
from CommonFunction.DataOperations import DataOperations
from CommonFunction.QT_Operations import QT_Operations
from CommonFunction.WebDriverHelp import WebDriverHelp

class testcases_ceatePublicSpace(unittest.TestCase):
    '''
    新增space目录
    '''

    def setUp(self):
        WebDriverHelp("open", "firefox", "local").setup("fcn")  # 打开浏览器，并打开forest

    def test1_createPublicSpace(self):
        global dataoper, detail_url
        # 读取测试数据并登录
        dataoper = DataOperations('QT_Space_createPublicSpace.xml')
        QT_Operations().login(dataoper.readxml('login', 0, 'username'), dataoper.readxml('login', 0, 'password'))
        time.sleep(2)

        # 点击进入Garoon
        garoon_url = "https://qatest01.cybozu.cn/g/"
        WebDriverHelp().geturl(garoon_url)
        time.sleep(1)

        # 点击进入space
        WebDriverHelp().clickitem('bycss', dataoper.readxml('space', 0, 'space_icon'))
        time.sleep(2)

        # 创建space
        WebDriverHelp().clickitem('bylink', dataoper.readxml('space', 0, 'creat_link'))
        time.sleep(1)
        # 输入title
        WebDriverHelp().inputvalue('byid', dataoper.readxml('space', 0, 'space_title'),
                                   dataoper.readxml('space', 0, 'title'))
        time.sleep(1)
        # 搜索添加用户
        WebDriverHelp().inputvalue('byname', dataoper.readxml('space', 0, 'e_keyword'),
                                   dataoper.readxml('space', 0, 'keyword'))
        time.sleep(1)
        WebDriverHelp().clickitem('byxpath', dataoper.readxml('space', 0, 'search'))
        time.sleep(1)
        WebDriverHelp().clickitem('byid', dataoper.readxml('space', 0, 'add_user'))
        time.sleep(1)
        # 选择公开方式
        WebDriverHelp().clickitem('byid', dataoper.readxml('space', 0, 'public'))

        # 保存
        WebDriverHelp().clickitem('byid', dataoper.readxml('space', 0, 'save'))
        time.sleep(1)
        current_url = WebDriverHelp().currenturl()
        print "current_url:", current_url

        # 进入详细页面
        WebDriverHelp().clickitem('byid', dataoper.readxml('space', 0, 'droplist'))
        time.sleep(1)
        WebDriverHelp().clickitem('bylink', dataoper.readxml('space', 0, 'detail'))
        time.sleep(1)
        detail_url = WebDriverHelp().currenturl()

        # 验证
        check = WebDriverHelp().gettext('byxpath', dataoper.readxml('space', 0, 'check'))
        check2 = WebDriverHelp().gettext('byxpath', dataoper.readxml('space', 0, 'check2'))
        value = dataoper.readxml('space', 0, 'value')
        value2 = dataoper.readxml('space', 0, 'value2')
        self.assertEqual(check, value)
        self.assertEqual(check2, value2)

        # 退出
        QT_Operations().logout()
        time.sleep(1)

        # 使用其他用户确认
        QT_Operations().login(dataoper.readxml('confirm', 0, 'username'),
                              dataoper.readxml('confirm', 0, 'password'))
        print "open current_url..."
        WebDriverHelp().geturl(current_url)
        time.sleep(2)
        # 确认是否存在元素
        try:
            WebDriverHelp().isElementPresent('byclass', dataoper.readxml('confirm', 0, 'element'))
        except:
            print "页面元素不存在"
        else:
            print "存在页面元素"
        QT_Operations().logout()

    def tearDown(self):
        # 清空数据
        try:
            QT_Operations().login(dataoper.readxml('login', 0, 'username'), dataoper.readxml('login', 0, 'password'))
            time.sleep(2)
            WebDriverHelp().geturl(detail_url)
            time.sleep(2)
            WebDriverHelp().clickitem('byid', dataoper.readxml('space', 0, 'delete_link'))
            time.sleep(2)
            WebDriverHelp().clickitem('byxpath', dataoper.readxml('space', 0, 'delete_yes'))
            time.sleep(2)
        except Exception as msg:
            print msg
        finally:
            WebDriverHelp().teardown()  # 关闭浏览器


if __name__ == "__main__":
    unittest.main()