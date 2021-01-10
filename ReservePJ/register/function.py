
import datetime


#時間帯 + 開始時間(hh)で予約終了時間を算出
def calc_end_time(start , zone):
    base = datetime.timedelta(hours=start.hour,minutes=start.minute)
    hour = datetime.timedelta(hours=zone,minutes=0)
    end = base + hour 
    if end >= datetime.timedelta(days=1):
        #24時超過のケース
        #合計値から1日分の秒数を差し引いた後、時間・分を取得
        end = end - datetime.timedelta(seconds=86400.0)
    m, s = divmod(end.total_seconds(), 60)
    h, m = divmod(m, 60)
    end = datetime.timedelta(hours=h,minutes=m)
    end = str(end)
    return datetime.datetime.strptime(end,"%H:%M:%S")
