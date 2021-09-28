from crontab import CronTab

cron = CronTab(user='jlopez')

getFondos = cron.new(command='getFondos.py')
getCarteras = cron.new(command='getCarteras.py')


getFondos.dow.on('MON', 'TUE', 'WED', 'THU', 'FRI')
getCarteras.dow.on('MON', 'TUE', 'WED', 'THU', 'FRI')

getFondos.day.every(1)
getCarteras.day.every(1)


for item in cron:
    print(item)

cron.write()
