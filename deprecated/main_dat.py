import settings.table as config
import settings.sysmsg_dep as msg
from dbms.Ddbms import LocalDBMethods
from model.N_v0 import UpBitNews


class SigInsert:
    def __init__(self):
        # Insert Database
        self.server = LocalDBMethods('binance.db')
        self.server.conn.execute(
            "PRAGMA journal_mode=WAL"
        )
        self.chk_server_status()
        self.insert_signal()

    def chk_server_status(self):
        t = self.server.get_table_list()
        if "stgyedr" not in t:
            print(msg.STATUS_1, config.TABLENAME_EVENTDRIVEN)
            self.server.create_table_w_pk(
                table_name=config.TABLENAME_EVENTDRIVEN,
                variables=config.TABLE_EVENTDRIVEN,
                pk_loc=[0, 1, 2, 3, 5]
            )

        if "stgyres" not in t:
            print(msg.STATUS_1, config.TABLENAME_ACCOUNT)
            self.server.create_table_w_pk(
                table_name=config.TABLENAME_ACCOUNT,
                variables=config.TABLE_ACCOUNT,
                pk_loc=[0, 1]
            )
        print(msg.STATUS_0, "ready")

    def insert_signal(self):
        upb = UpBitNews(database=self.server)
        upb.run()


if __name__ == '__main__':
    b = SigInsert()
