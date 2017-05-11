import datetime

def get_timestamp():
    return str(datetime.datetime.now()).replace('-','').replace(' ','').replace(':','').replace('.','')

def get_timestamp_short():
    return str(datetime.datetime.now()).replace('-','').replace(' ','').replace(':','').replace('.','')[:14]

if __name__ == '__main__':
    print get_timestamp()
    print get_timestamp_short()
