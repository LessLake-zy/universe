import jaydebeapi
import pandas as pd

class JDBCConnector:
    def __init__(self, class_name, user_id, pwd, jdbc_path, property=None):
        """
        初始化JDBC连接器
        :param class_name: JDBC驱动类名
        :param user_id: 用户ID
        :param pwd: 密码
        :param jdbc_path: JDBC路径
        :param property: 连接属性，可选
        """
        self.class_name = class_name
        self.user_id = user_id
        self.pwd = pwd
        self.jdbc_path = jdbc_path
        self.property = property
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        建立数据库连接
        :return: 数据库连接对象
        """
        try:
            if self.property is None:
                # 建立esp连接
                self.connection = jaydebeapi.connect(
                    self.class_name,
                    self.jdbc_path,
                    [self.user_id, self.pwd]
                )
            else:
                # 建立sscd连接
                self.connection = jaydebeapi.connect(
                    self.class_name,
                    self.jdbc_path,
                    [self.user_id, self.pwd],
                    self.property
                )
            self.cursor = self.connection.cursor()
            return self.connection, self.cursor
        except Exception as e:
            raise Exception(f"数据库连接失败: {str(e)}")

    def query_to_dataframe(self, sql):
        """
        执行SQL查询并返回DataFrame
        :param connection: 数据库连接
        :param sql: SQL查询语句
        :return: pandas DataFrame
        """
        try:
            cursor, conn = self.connect()
            cursor.execute(sql)
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            return pd.DataFrame(data, columns=columns)
        except Exception as e:
            raise Exception(f"查询执行失败: {str(e)}")

    def save_dataframe(self, df, file_path):
        """
        保存DataFrame到文件
        :param df: pandas DataFrame
        :param file_path: 文件保存路径
        """
        try:
            # 根据文件扩展名选择保存格式
            if file_path.endswith('.csv'):
                df.to_csv(file_path, index=False)
            elif file_path.endswith('.xlsx'):
                df.to_excel(file_path, index=False)
            else:
                df.to_csv(file_path, index=False)  # 默认保存为CSV
        except Exception as e:
            raise Exception(f"文件保存失败: {str(e)}")

    def close(self):
        """
        关闭数据库连接和游标
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except Exception as e:
            raise Exception(f"关闭连接失败: {str(e)}")