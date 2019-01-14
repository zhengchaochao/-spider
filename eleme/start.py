# @Time    : 2019/1/8 下午4:20
# @Author  : 郑超
# @Desc    :
import threading, datetime, time
from apscheduler.schedulers.blocking import BlockingScheduler
from eleme.red_envelopes import get_red_envelopes


def hongbao_default():
    return get_red_envelopes("default")


# def hongbao_default1():
#     return get_red_envelopes("default")


scheduler = BlockingScheduler()
# default用户
scheduler.add_job(hongbao_default, 'cron', hour=9, minute=59, second=59)
scheduler.add_job(hongbao_default, 'cron', hour=13, minute=59, second=59)
scheduler.add_job(hongbao_default, 'cron', hour=16, minute=59, second=59)
scheduler.add_job(hongbao_default, 'cron', hour=19, minute=59, second=59)

print("开始执行" + datetime.datetime.now().strftime('%H:%M:%S.%f'))
scheduler.start()

