import csv


def readDataCsv(csvfile, type='all'):
    # 读取csv至字典
    csvFile = open(csvfile, "r")
    reader = csv.reader(csvFile)
    # 建立空字典
    result = []
    for item in reader:
        # 忽略第一行
        if reader.line_num == 1:
            continue
        if type == 'all':
            result += [item]
        elif isinstance(type, int) and type < len(item):
            result += [float(item[type])]

    csvFile.close()
    return result


if __name__ == '__main__':
    cvsfile = "test.csv"
    ret = readDataCsv(cvsfile, 2)
    print(ret)
