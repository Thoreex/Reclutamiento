from datetime import datetime

def utility_processor():
    def time_ago(date: datetime):
        now = datetime.now()
        diff = now - date

        seconds_in_minutes = 60
        minutes_in_hours = 60
        hours_in_days = 24

        long = diff.seconds
        if long < seconds_in_minutes:
            return 'Just now'
        
        long //= seconds_in_minutes
        if long >= 1 and long < minutes_in_hours:
            return str(long) + f' minute{"s" if long > 1 else ""} ago'

        long //= minutes_in_hours
        if long >= 1 and long < hours_in_days:
            return str(long) + f' hour{"s" if long > 1 else ""} ago'

        long //= hours_in_days
        return str(long) + f' day{"s" if long > 1 else ""} ago'

    return dict(time_ago=time_ago)

def init_app(app):
    app.context_processor(utility_processor)