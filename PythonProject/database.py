import pyodbc
import traceback


class Database:
    def __init__(self):
        # Cấu hình kết nối SQL Server - thay đổi thông tin phù hợp với máy của bạn
        self.server = 'localhost'  # hoặc tên server SQL của bạn
        self.database = 'DuLieu'
        self.username = 'sa'  # thay đổi tên người dùng SQL Server
        self.password = 'YourPassword'  # thay đổi mật khẩu
        self.connection_string = f'DRIVER={{SQL Server}};SERVER={"hai\\SQLEXPRESS"};DATABASE={"DuLieu"};UID={"sa"};PWD={"123456"}'
        self.conn = None

    def connect(self):
        try:
            print(f"Attempting to connect with: {self.connection_string}")
            self.conn = pyodbc.connect(self.connection_string)
            print("Connection successful")
            return self.conn
        except Exception as e:
            print(f"Lỗi kết nối: {e}")
            print(traceback.format_exc())
            return None

    def execute_query(self, query, params=None):
        conn = None
        try:
            conn = self.connect()
            if not conn:
                raise Exception("Không thể kết nối đến cơ sở dữ liệu")
                
            cursor = conn.cursor()
            print(f"Executing query: {query}")
            print(f"With parameters: {params}")
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # Lấy kết quả nếu là SELECT
            if query.strip().upper().startswith('SELECT'):
                columns = [column[0] for column in cursor.description]
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
            else:
                conn.commit()
                return cursor.rowcount  # Trả về số dòng bị ảnh hưởng

        except Exception as e:
            print(f"Lỗi thực thi truy vấn: {e}")
            print(traceback.format_exc())
            if conn:
                conn.rollback()
            raise  # Re-raise the exception to handle it at a higher level
        finally:
            if conn:
                conn.close()


if __name__ == "__main__":
    db = Database()
    connection = db.connect()
    if connection:
        print("Kết nối thành công!")
        # Test a simple query
        try:
            result = db.execute_query("SELECT TOP 1 * FROM tblChatLieu")
            print(f"Query result: {result}")
        except Exception as e:
            print(f"Test query failed: {e}")
    else:
        print("Kết nối thất bại!")