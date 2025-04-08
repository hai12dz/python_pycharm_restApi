from flask import Flask, request, jsonify, send_from_directory
from models import SanPham, ChatLieu
from flask_cors import CORS  # You'll need to install this: pip install flask-cors

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Endpoint lấy thông tin của toàn bộ sản phẩm
@app.route('/api/products', methods=['GET'])
def get_all_products():
    try:
        san_pham = SanPham()
        products = san_pham.get_all()
        return jsonify({
            'success': True,
            'data': products,
            'count': len(products)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Endpoint lấy thông tin sản phẩm theo tên và chất liệu (tìm kiếm gần đúng)
@app.route('/api/products/search', methods=['GET'])
def search_products():
    try:
        ten_sp = request.args.get('ten_sp', '')
        ten_cl = request.args.get('ten_cl', '')

        san_pham = SanPham()
        products = san_pham.search_by_name_material(ten_sp, ten_cl)

        return jsonify({
            'success': True,
            'data': products,
            'count': len(products)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Endpoint lấy danh sách sản phẩm tồn kho (số lượng > 0)
@app.route('/api/products/available', methods=['GET'])
def get_available_products():
    try:
        san_pham = SanPham()
        products = san_pham.get_available_products()

        return jsonify({
            'success': True,
            'data': products,
            'count': len(products)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Endpoint thêm sản phẩm mới
@app.route('/api/products', methods=['POST'])
def add_product():
    try:
        product_data = request.json
        
        # Log the incoming data for debugging
        print(f"Incoming product data: {product_data}")

        # Kiểm tra dữ liệu đầu vào
        required_fields = ['TenSP', 'ChatLieu', 'GiaNhap', 'GiaBan', 'SoLuong']
        for field in required_fields:
            if field not in product_data:
                return jsonify({
                    'success': False,
                    'error': f'Thiếu trường dữ liệu: {field}'
                }), 400

        san_pham = SanPham()
        new_id = san_pham.add_product(product_data)

        if new_id:
            return jsonify({
                'success': True,
                'message': 'Thêm sản phẩm thành công',
                'MaSP': new_id
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Không thể thêm sản phẩm'
            }), 500
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"Exception in add_product: {e}")
        print(error_traceback)
        
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': error_traceback
        }), 500


# Endpoint cập nhật thông tin sản phẩm
@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        product_data = request.json

        # Kiểm tra dữ liệu đầu vào
        required_fields = ['TenSP', 'ChatLieu', 'GiaNhap', 'GiaBan', 'SoLuong']
        for field in required_fields:
            if field not in product_data:
                return jsonify({
                    'success': False,
                    'error': f'Thiếu trường dữ liệu: {field}'
                }), 400

        san_pham = SanPham()
        rows_affected = san_pham.update_product(product_id, product_data)

        if rows_affected > 0:
            return jsonify({
                'success': True,
                'message': 'Cập nhật sản phẩm thành công'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Không tìm thấy sản phẩm với ID: {product_id}'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Endpoint xóa sản phẩm
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        san_pham = SanPham()
        rows_affected = san_pham.delete_product(product_id)

        if rows_affected > 0:
            return jsonify({
                'success': True,
                'message': 'Xóa sản phẩm thành công'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Không tìm thấy sản phẩm với ID: {product_id}'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Endpoint lấy danh sách chất liệu (API bổ sung)
@app.route('/api/materials', methods=['GET'])
def get_all_materials():
    try:
        chat_lieu = ChatLieu()
        materials = chat_lieu.get_all()
        return jsonify({
            'success': True,
            'data': materials,
            'count': len(materials)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Serve static files
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run(debug=True, port=5000)