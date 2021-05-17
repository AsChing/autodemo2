
import xlrd
from log import my_log


class ReadExcel(object):

    def __init__(self, fileName, SheetName="Sheet1"):
        self.data = xlrd.open_workbook(fileName)
        self.table = self.data.sheet_by_name(SheetName)

        # 获取总行数、总列数
        self.nrows = self.table.nrows
        self.ncols = self.table.ncols
        self.logger = my_log.Logger('../log/log/all.log', level='debug').logger

    def read_data(self):
        if self.nrows > 1:
            # 获取第一行的内容，列表格式
            keys = self.table.row_values(0)
            keys.append('row')
            listApiData = []
            # 获取每一行的内容，列表格式
            for row in range(1, self.nrows):    # 去除定义的首行
                values = self.table.row_values(row)
                values.append(row + 1)
                # keys，values组合转换为字典
                api_dict = dict(zip(keys, values))
                listApiData.append(api_dict)
            return listApiData
        else:
            self.logger.warning("-----------------------表格中没有测试数据!--------------------------")
            return None
