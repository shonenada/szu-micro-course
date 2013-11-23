#-*- coding: utf-8 -*-
from datetime import datetime

from mooc.app import db
from mooc.account.model import User, SzuAccount, College, Teacher, Role
from mooc.course.model import Subject, Category, Course, Clip, LearnRecord


def _init_role():
    global roles
    roles = (
        Role('everyone'), Role('local_user'), Role('student'),
        Role('teacher'), Role('super_admin')
    )
    roles[1].parents.append(roles[0])
    roles[2].parents.append(roles[1])
    roles[3].parents.append(roles[1])
    roles[4].parents.append(roles[1])
    for role in roles:
        db.session.add(role)


def _init_college():
    global csse
    csse = College(name=u'计算机与软件学院', order=13)
    db.session.add(csse)


def _init_user():
    global shonenada, key
    shonenada = User('shonenada', '000000', 'shonenada', True)
    key = User('key', '123456', 'key', True)
    shonenada.active()
    key.active()
    shonenada.roles.append(roles[4])
    key.roles.append(roles[3])
    db.session.add(shonenada)
    db.session.add(key)


def _init_szu_account():
    global shonenada_account, key_account
    shonenada_account = SzuAccount(shonenada, '112020', '2011150000', csse, 'undergrade')
    key_account = SzuAccount(key, '113030', '2011150999', csse, 'teacher')
    db.session.add(shonenada_account)
    db.session.add(key_account)


def _init_teacher():
    global mr_key
    mr_key = Teacher('teacher', 'KEY', key_account)
    db.session.add(mr_key)


def _init_subject():
    global subjects
    subjects = (
        Subject(name=u'电类', description=u'电类'),
        Subject(name='Linux', description='Courses of Linux'),
        Subject(name=u'数据库', description='Courses of database'),
        Subject(name=u'Web开发', description='Courses of web development'),
    )
    for subject in subjects:
        db.session.add(subject)


def _init_category():
    global categorys
    categorys = (
        Category(u'数字电子技术', subjects[0]),

        Category(u'入门基础', subjects[1]),
        Category(u'系统服务', subjects[1]),
        Category(u'高级管理', subjects[1]),

        Category(u'MySQL基础', subjects[2]),
        Category(u'SQL 语言', subjects[2]),

        Category(u'Ruby语言', subjects[3]),
        Category(u'Python语言', subjects[3]),
    )
    for category in categorys:
        db.session.add(category)


def _init_course():
    global courses
    courses = (
        Course(u'数字逻辑与数字系统.多位加法器：串行加法器', u'课程介绍数字逻辑与数字系统', key, categorys[0]),

        Course(u'Linux基本操作', u'课程包含Linux图形界面下的日常操作维护及命令行（CLI）下的日常操作维护。', key, categorys[1]),
        Course(u'Linux磁盘及文件系统管理', u'课程包括磁盘基本概念、文件系统的基本概念及分区、文件系统的创建管理。', key, categorys[1]),
        Course(u'Linux下获取帮助', u'课程包括图形界面及命令行界面下如何获取所使用命令工具的帮助信息', key, categorys[1]),

        Course(u'rSyslog日志服务', u'本课程将为您介绍日志服务的基本概念及如何配置rsyslog服务', key, categorys[2]),
        Course(u'DNS域名服务', u'课程包括DNS基本概念、DNS架构介绍、bind服务配置', key, categorys[2]),

        Course(u'磁盘管理：LVM逻辑卷', u'课程包括LVM逻辑卷基本概念、逻辑卷的创建删除及逻辑卷的拉伸缩小。', key, categorys[3]),
        Course(u'Linux高级权限 - ACL', u'讲解如何通过访问控制列表（ACL）对Linux进行高级权限管理', key, categorys[3]),

        Course(u'MySQL数据库基础', u'介绍MySQL数据库的安装和配置，SQL语法，MySQL调优方式及实际配置案例，MySQL备份机制。', key, categorys[4]),

        Course(u'Oracle数据库入门基础', u'讲解Oracle数据库的常见知识、安装、管理及日常维护应用。', key, categorys[5]),

        Course(u'Ruby 开发语言', u'Ruby 是一种跨平台、面向对象的动态类型编程语言。Ruby 体现了表达的一致性和简单性， 它不仅是一门编程语言，更是表达想法的一种简练方式。', key, categorys[6]),
        
        Course(u'Python 语言基础', u'Python 是一种面向对象、直译式计算机程序设计语言，由Guido van Rossum于1989年底发明，第一个公开发行版发行于1991年。Python语法简捷而清晰，具有丰富和强大的类库。', key, categorys[7]),
    )
    for course in courses:
        db.session.add(course)


def _init_clip():
    global clips
    clips = (
        Clip(u'.多位加法器：串行加法器', u'本课程为您讲解多位加法器：串行加法器', shonenada, courses[0], 1, True),

        Clip(u'GNOME图形界面基本操作', u'本课程为您讲解Linux系统主流图形界面GNOME的基本操作使用', shonenada, courses[1], 1, True),
        Clip(u'命令行BASH的基本操作', u'本课程为您讲解Linux命令行界面（CLI）BASH的基本操作使用', shonenada, courses[1], 2, True),

        Clip(u'磁盘基本概念', u'本课程为您讲解磁盘的基本概念，包括磁盘结构、扇区、磁臂、柱面的概念以及MBR、GPT的分区管理知识', shonenada, courses[2], 1, True),
    )

    clips[0].knowledge_point = u'<ul><li>知识点1</li><li>知识点2</li><li>...</li></ul>'
    clips[0].record_time = datetime(2013, 11, 06)
    clips[0].record_address = u'教学楼A101'
    clips[0].video_url = 'http://mooc.shonenada.com/static/upload/videos/2013-11-06.caiye.mp4'
    clips[0].video_length = 16

    clips[1].knowledge_point = u'<ul><li>GNOME最早诞生于1999年，主要由redhat员工开发</li><li>GNOME是Linux系统以及其他类Unix系统下使用最为广泛的开源图形化界面系统</li><li>GNOME使用X11作为底层图形驱动服务</li></ul>'
    clips[1].record_time = datetime(2013, 11, 12)
    clips[1].record_address = u'教学楼A210'
    clips[1].video_url = 'http://112.124.15.99:8888//linux-basic/2.mp4'
    clips[1].video_length = 42

    clips[2].knowledge_point = u'<ul><li>Shell（壳）是用户与操作系统底层（通常是内核）之间交互的中介程序，负责将用户指令、操作传递给操作系统底层</li><li>Shell一般分为：图形化Shell（GUI）、命令行Shell（CLI）</li><li>Linux中一般默认GUI为：GNOME，默认CLI为：BASH</li><li>BASH提示符以#或$起始，#代表当前用户为root用户，$代表当前用户为普通用户</li><li>我们可以通过键盘上的Tab按键对命令或文件名进行自动补全</li><li>BASH会记录我们以往操作的命令，可以通过history命令查看</li><li>BASH可以通过以下方式调用历史记录以简化操作：</li></ul><div><strong>!! &nbsp; &nbsp; &nbsp; 重复前一个命令</strong></div><div><strong>!字符 &nbsp; 重复前一个以指定字符开头的命令</strong><br><strong>!num &nbsp; 按历史记录序号执行命令</strong><br><strong>!?abc &nbsp;重复之前包含abc的命令</strong><br><strong>!-n &nbsp; &nbsp; 重复n个命令之前那个命令</strong></div><ul><li>我们可以通过 ctrl + r 来对历史记录进行搜索查询</li><li>命令su可以切换用户</li><li>命令passwd可以修改当前用户的密码</li><li>命令id可以显示当前用户的信息</li><li>通过在命令后追加一个&amp;，可以将该命令放入后台运行</li><li>通过以下命令可以管理后台作业：</li></ul><p><strong>jobs &nbsp;显示后台作业</strong><br><strong>fg &nbsp; &nbsp;将后台作业调到前台执行</strong><br><strong>bg &nbsp; &nbsp;继续执行一个后台作业</strong></p>'
    clips[2].record_time = datetime(2013, 11, 13)
    clips[2].record_address = u'教学楼A313'
    clips[2].video_url = 'http://112.124.15.99:8888//linux-basic/3.mp4'
    clips[2].video_length = 23

    clips[3].knowledge_point = u'<p>磁盘基本概念：</p><p><strong>cylinder（柱面）</strong></p><p><strong>sector（扇区）</strong></p><p><strong>head（磁头）</strong></p><p>Linux系统中，磁盘以磁盘文件形式保存在/dev目录下，文件名以hd或sd开头（IDE设备以hd开头，usb、sata、SCSI、SAS等设备以sd开头），以a、b、c等表示编号，如第一块硬盘叫做/dev/sda，第二块叫做/dev/sdb，以此类推</p><p>分区使用设备名+分区号形式表示，如第一个磁盘的第一个分区：/dev/sda1，第二个分区：/dev/sda2</p><p>MBR是PC架构计算机使用的最为广泛的分区机制，特点如下：</p><p><strong>支持32位及64位系统</strong></p><p><strong>支持的分区数量有限</strong></p><p><strong>支持最大空间为2T</strong></p><p>MBR分区概念：</p><p><strong>主分区</strong></p><p><strong>扩展分区</strong></p><p><strong>逻辑分区</strong></p><p>GPT是较MBR更新、更先进的分区机制，应用于支持uEFI的计算机上，特点如下：</p><p><strong>支持超过2T的空间</strong></p><p><strong>向后兼容MBR</strong></p><p><strong>必须使用64bit系统</strong></p><p><strong>底层硬件必须使用EFI</strong></p><p>&nbsp;</p>'
    clips[3].record_time = datetime(2013, 11, 15)
    clips[3].record_address = u'教学楼A313'
    clips[3].video_url = 'http://112.124.15.99:8888//linux-basic/9.mp4'
    clips[3].video_length = 23

    for clip in clips:
        db.session.add(clip)


def _init_learn_record():
    for clip in clips:
        learn_record = LearnRecord(clip, shonenada)
        db.session.add(learn_record)


def init_db():
    _init_role()
    _init_college()
    _init_user()
    _init_szu_account()
    _init_teacher()
    _init_subject()
    _init_category()
    _init_course()
    _init_clip()
    _init_learn_record()
    db.session.commit()
