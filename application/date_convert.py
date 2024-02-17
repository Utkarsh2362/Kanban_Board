def convert_date(input_date):
    import datetime
    format = '%Y-%m-%d'
    datetime = datetime.datetime.strptime(input_date, format)
    return datetime.date()


def type_date(input_date):
    from datetime import datetime
    from datetime import date
    new_date = datetime.strptime(input_date, '%Y-%m-%d').date()
    return new_date
