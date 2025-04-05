from database import Database
import traceback


class SanPham:
    def __init__(self, MaSP=None, TenSP=None, ChatLieu=None, MoTa=None, GiaNhap=None, GiaBan=None, SoLuong=None):
        self.MaSP = MaSP
        self.TenSP = TenSP
        self.ChatLieu = ChatLieu
        self.MoTa = MoTa
        self.GiaNhap = GiaNhap
        self.GiaBan = GiaBan
        self.SoLuong = SoLuong
        self.db = Database()

    def get_all(self):
        query = """
        SELECT sp.MaSP, sp.TenSP, cl.TenCL as ChatLieu, sp.MoTa, sp.GiaNhap, sp.GiaBan, sp.SoLuong 
        FROM tblSanPham sp
        JOIN tblChatLieu cl ON sp.ChatLieu = cl.MaCL
        """
        return self.db.execute_query(query)

    def search_by_name_material(self, ten_sp, ten_cl):
        query = """
        SELECT sp.MaSP, sp.TenSP, cl.TenCL as ChatLieu, sp.MoTa, sp.GiaNhap, sp.GiaBan, sp.SoLuong 
        FROM tblSanPham sp
        JOIN tblChatLieu cl ON sp.ChatLieu = cl.MaCL
        WHERE sp.TenSP LIKE ? AND cl.TenCL LIKE ?
        """
        ten_sp_pattern = f'%{ten_sp}%'
        ten_cl_pattern = f'%{ten_cl}%'
        return self.db.execute_query(query, (ten_sp_pattern, ten_cl_pattern))

    def get_available_products(self):
        query = """
        SELECT sp.MaSP, sp.TenSP, cl.TenCL as ChatLieu, sp.MoTa, sp.GiaNhap, sp.GiaBan, sp.SoLuong 
        FROM tblSanPham sp
        JOIN tblChatLieu cl ON sp.ChatLieu = cl.MaCL
        WHERE sp.SoLuong > 0
        """
        return self.db.execute_query(query)

    def add_product(self, product_data):
        print("Starting add_product method")
        try:
            # Use a single transaction with OUTPUT clause to get the inserted ID
            insert_query = """
            INSERT INTO tblSanPham (TenSP, ChatLieu, MoTa, GiaNhap, GiaBan, SoLuong)
            OUTPUT INSERTED.MaSP
            VALUES (?, ?, ?, ?, ?, ?);
            """
            params = (
                product_data.get('TenSP'),
                product_data.get('ChatLieu'),
                product_data.get('MoTa', ''),
                product_data.get('GiaNhap'),
                product_data.get('GiaBan'),
                product_data.get('SoLuong')
            )
            print(f"Query parameters: {params}")

            conn = self.db.connect()
            if not conn:
                print("Failed to connect to database")
                return None
                
            cursor = conn.cursor()
            print("Executing query with OUTPUT clause")
            cursor.execute(insert_query, params)
            
            # Get the result from the OUTPUT clause
            row = cursor.fetchone()
            print(f"Output row: {row}")
            
            if row and row[0]:
                new_id = row[0]
                print(f"New ID: {new_id}")
                conn.commit()
                return new_id
            else:
                print("No ID returned from OUTPUT clause")
                conn.rollback()
                return None
                
        except Exception as e:
            print(f"Error in add_product: {e}")
            print(traceback.format_exc())
            if 'conn' in locals() and conn:
                conn.rollback()
            
            # Try alternative approach if OUTPUT clause fails
            return self._add_product_alternative(product_data)
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    def _add_product_alternative(self, product_data):
        """Alternative method to add product if the OUTPUT clause approach fails"""
        print("Trying alternative approach to add product")
        
        # First insert without getting ID
        insert_query = """
        INSERT INTO tblSanPham (TenSP, ChatLieu, MoTa, GiaNhap, GiaBan, SoLuong)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        
        # Then get the last inserted ID by other means
        get_id_query = """
        SELECT TOP 1 MaSP FROM tblSanPham 
        WHERE TenSP = ? AND ChatLieu = ? AND GiaNhap = ? AND GiaBan = ? AND SoLuong = ?
        ORDER BY MaSP DESC
        """
        
        params1 = (
            product_data.get('TenSP'),
            product_data.get('ChatLieu'),
            product_data.get('MoTa', ''),
            product_data.get('GiaNhap'),
            product_data.get('GiaBan'),
            product_data.get('SoLuong')
        )
        
        params2 = (
            product_data.get('TenSP'),
            product_data.get('ChatLieu'),
            product_data.get('GiaNhap'),
            product_data.get('GiaBan'),
            product_data.get('SoLuong')
        )
        
        conn = None
        try:
            conn = self.db.connect()
            if not conn:
                return None
                
            cursor = conn.cursor()
            
            # Insert the record
            cursor.execute(insert_query, params1)
            conn.commit()
            
            # Get the ID of the inserted record
            cursor.execute(get_id_query, params2)
            row = cursor.fetchone()
            
            if row and row[0]:
                return row[0]
            return None
            
        except Exception as e:
            print(f"Alternative method failed: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            if conn:
                conn.close()

    def update_product(self, product_id, product_data):
        query = """
        UPDATE tblSanPham
        SET TenSP = ?, ChatLieu = ?, MoTa = ?, GiaNhap = ?, GiaBan = ?, SoLuong = ?
        WHERE MaSP = ?
        """
        params = (
            product_data.get('TenSP'),
            product_data.get('ChatLieu'),
            product_data.get('MoTa'),
            product_data.get('GiaNhap'),
            product_data.get('GiaBan'),
            product_data.get('SoLuong'),
            product_id
        )
        return self.db.execute_query(query, params)

    def delete_product(self, product_id):
        query = "DELETE FROM tblSanPham WHERE MaSP = ?"
        return self.db.execute_query(query, (product_id,))


class ChatLieu:
    def __init__(self):
        self.db = Database()

    def get_all(self):
        query = "SELECT * FROM tblChatLieu"
        return self.db.execute_query(query)