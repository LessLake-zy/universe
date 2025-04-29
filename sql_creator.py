class SQLCreator:
    def __init__(self, platform, sql_type, ppdasat, pdasat, tdasat, client):
        """
        初始化SQL创建器
        :param platform: 平台类型 (esp/sscd)
        :param sql_type: SQL类别 (trx/val/fx)
        :param ppdasat: 第一个日期
        :param pdasat: 第二个日期
        :param tdasat: 第三个日期
        :param client: 客户端
        """
        if platform not in ['esp', 'sscd']:
            raise ValueError("平台类型必须是 'esp' 或 'sscd'")
        
        if sql_type not in ['trx', 'val', 'fx']:
            raise ValueError("SQL类别必须是 'trx', 'val' 或 'fx'")
            
        self.platform = platform
        self.sql_type = sql_type
        self.ppdasat = ppdasat
        self.pdasat = pdasat
        self.tdasat = tdasat
        self.client = client

    def replace_variables(self, sql):
        """
        替换SQL语句中的变量
        :param sql: 原始SQL语句
        :return: 替换变量后的SQL语句
        """
        # 创建替换映射
        replacements = {
            'ppdasat': self.ppdasat,
            'pdasat': self.pdasat,
            'tdasat': self.tdasat,
            'client': self.client
        }
        
        # 执行替换
        result_sql = sql
        for key, value in replacements.items():
            result_sql = result_sql.replace(f'${key}', str(value))
            # 支持大写变量名替换
            result_sql = result_sql.replace(f'${key.upper()}', str(value))
            
        return result_sql