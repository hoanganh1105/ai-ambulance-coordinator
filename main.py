from modules.core.map_router import MapRouter
import os
import sys
root_path = os.path.dirname(os.path.abspath(__file__))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

def main():
    print("--- Đang khởi tạo MapRouter (Simple Street Map) ---")
    router = MapRouter(place_name="Delhi, India", model_name="simpleStreetMap")
    
    # 1. Lấy danh sách toạ độ khả dụng để chọn điểm test
    coords = router.available_coordinates()
    if not coords:
        print("Không tìm thấy dữ liệu bản đồ!")
        return
    
    print(f"Số lượng node trên bản đồ: {len(coords)}")
    
    # 2. Giả định toạ độ xuất phát (Ambulance) và đích (Patient)
    # Lấy đại 2 điểm từ danh sách node để đảm bảo chúng tồn tại trên map
    origin_coords = coords[0]
    target_coords = coords[-1] 
    
    print(f"Vị trí org: {origin_coords}")
    print(f"Vị trí target: {target_coords}")

    # 3. Tìm đường đi tối ưu
    print("\n--- Đang tìm đường đi tối ưu... ---")
    try:
        path = router.optimal_path(origin_coords, target_coords)
        print(f"Tìm thấy đường đi với {len(path)} toạ độ.")
    except Exception as e:
        print(f"Lỗi khi tìm đường: {e}")
        path = None

    # 4. Hiển thị bản đồ với đường đi được tìm thấy
    print("\n--- Đang hiển thị bản đồ ---")
    router.show_map(
        org=origin_coords, 
        dests=[target_coords], 
        route=path
    )

if __name__ == "__main__":
    main()