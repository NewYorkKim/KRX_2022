import datetime as dt
today = dt.datetime.now()
dt.datetime.strptime()
(today - dt.timedelta(days=400)).strftime('%Y-%m-%d %H:%M:%S')
(today - dt.timedelta(days=400)) < today
type(today)

dt.datetime(2022,6,1,0,0) > today

[int(i) for i in '2022-06-30 14:00'.split()[0].split('-')]