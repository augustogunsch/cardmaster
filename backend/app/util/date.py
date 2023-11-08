def normalize(date):
    offset = date.utcoffset()

    if offset:
        date = date - offset
        return date.replace(tzinfo=None)

    return date
