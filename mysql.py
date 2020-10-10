import pymysql


class Database:
    def __init__(self):
        conn = pymysql.connect(
            host="122.51.155.8",
            user="root",
            password="123",
            database="duonao",
            charset="utf8")

        self.cursor = conn.cursor()

    def get_all_id(self):
        sql = "select duonao_id from movie"
        try:
            l = list()
            # 执行 sql 语句
            self.cursor.execute(sql)
            # 显示出所有数据
            data_result = self.cursor.fetchall()
            for row in data_result:
                l.append(row[0])
            return l
            # 打印结果
        except:
            print("Error: unable to fetch data")


if __name__ == '__main__':
    print(Database().get_all_id())
