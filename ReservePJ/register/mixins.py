
import calendar
from collections import deque
import datetime
from django.utils import timezone
from .models import Day_of_the_week
from reserve.models import office_category,Floor,Room,Seats
from django.db.models import Count
from django.db import connection

now = timezone.localtime(timezone.now())
class BaseCalendarMixin:
    """カレンダー関連Mixinの、基底クラス"""
    #0は月曜から
    first_weekday = 0
    #曜日名を取得
    week_names = Day_of_the_week.objects.all().order_by('name_id')
    #カレンダーに表示する見出し情報
    #カテゴリー見出し
    office_category = office_category.objects.all().order_by('category_id')
    #各カテゴリーの値を取得
    floor_category = Floor.objects.all().order_by('floor_id')
    room_category = Room.objects.all().order_by('floor','room_id')
    seats_category = Seats.objects.all().order_by('room','seats_id')

    #各カテゴリーをリスト化
    #0,0,0 = フロア,ルーム,シート として格納
    resultlist = []
    for f in floor_category:
        for r in room_category:
            if f == r.floor:
                for s in seats_category:
                    if r == s.room:
                        resultlist.append([[f],[r],[s]]) 

    def setup_calendar(self):
        """内部カレンダーの設定処理

        calendar.Calendarクラスの機能を利用するため、インスタンス化します。
        Calendarクラスのmonthdatescalendarメソッドを利用していますが、デフォルトが月曜日からで、
        火曜日から表示したい(first_weekday=1)、といったケースに対応するためのセットアップ処理です。

        """
        self._calendar = calendar.Calendar(self.first_weekday)

    def get_week_names(self):
        """first_weekday(最初に表示される曜日)にあわせて、week_namesをシフトする"""
        week_names = deque(self.week_names)
        week_names.rotate(-self.first_weekday)  # リスト内の要素を右に1つずつ移動...なんてときは、dequeを使うと中々面白いです
        return week_names

class WeekCalendarMixin(BaseCalendarMixin):
    """週間カレンダーの機能を提供するMixin"""

    def get_week_days(self):
        """その週の日を全て返す"""
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()

        for week in self._calendar.monthdatescalendar(date.year, date.month):
            if date in week:  # 週ごとに取り出され、中身は全てdatetime.date型。該当の日が含まれていれば、それが今回表示すべき週です
                return week

    def get_week_calendar(self):
        """週間カレンダー情報の入った辞書を返す"""
        self.setup_calendar()
        days = self.get_week_days()
        first = days[0]
        last = days[-1]
        calendar_data = {
            'now': datetime.date.today(),
            'week_days': days,
            'week_previous': first - datetime.timedelta(days=7),
            'week_next': first + datetime.timedelta(days=7),
            'week_names': self.get_week_names(),
            'week_first': first,
            'week_last': last,
            'office_category': self.office_category,
            'resultlist':self.resultlist,
        }
        return calendar_data

class WeekWithScheduleMixin(WeekCalendarMixin):
    """スケジュール付きの、週間カレンダーを提供するMixin"""

    def get_week_schedules(self, start, end, days):
        """それぞれの日とスケジュールを返す"""
        lookup = {
            # '例えば、date__range: (1日, 31日)'を動的に作る
            '{}__range'.format(self.date_field): (start, end)
        }
        # 例えば、Schedule.objects.filter(date__range=(1日, 31日)) になる
        queryset = self.model.objects.filter(**lookup)

        # {1日のdatetime: 1日のスケジュール全て, 2日のdatetime: 2日の全て...}のような辞書を作る
        day_schedules = {day: [] for day in days}
        for Reserve in queryset:
            schedule_date = getattr(Reserve, self.date_field)
            day_schedules[schedule_date].append(Reserve)
        return day_schedules

    def get_week_calendar(self):
        calendar_context = super().get_week_calendar()
        calendar_context['week_day_schedules'] = self.get_week_schedules(
            calendar_context['week_first'],
            calendar_context['week_last'],
            calendar_context['week_days']
        )
        return calendar_context