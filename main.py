from modules.core.map_router import MapRouter
import os
import sys

# Thiết lập path để import được các modules
root_path = os.path.dirname(os.path.abspath(__file__))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

def main():
    print("--- Đang khởi tạo MapRouter (Simple Street Map) ---")
    # Khởi tạo router cho khu vực Delhi
    router = MapRouter(place_name="Delhi, India", model_name="simpleStreetMap")
    
    # 1. Lấy danh sách toạ độ khả dụng
    coords = router.available_coordinates()
    if not coords:
        print("Không tìm thấy dữ liệu bản đồ!")
        return
    
    print(f"Số lượng node trên bản đồ: {len(coords)}")
    
    # 2. Giả định toạ độ xuất phát (Ambulance) và đích (Patient)
    origin_coords = coords[100] # Lấy một điểm ở giữa danh sách để test rõ hơn
    target_coords = coords[-100] 
    
    print(f"Vị trí org: {origin_coords}")
    print(f"Vị trí target: {target_coords}")

    # 3. Tìm đường đi tối ưu
    print("\n--- Đang tìm đường đi tối ưu... ---")
    try:
        # SỬA LỖI TẠI ĐÂY: optimal_path trả về (path_coords, distance)
        path_coords, distance = router.optimal_path(origin_coords, target_coords)
        print(f"Tìm thấy đường đi với {len(path_coords)} toạ độ.")
        print(f"Tổng chiều dài quãng đường: {distance:.2f} meters")
    except Exception as e:
        print(f"Lỗi khi tìm đường: {e}")
        path_coords = []

    # 4. Hiển thị bản đồ với đường đi được tìm thấy
    print("\n--- Đang hiển thị bản đồ ---")
    router.show_map(
        org=origin_coords, 
        dests=[target_coords], 
        route=path_coords,
        show_density=True
    )

if __name__ == "__main__":
    main()