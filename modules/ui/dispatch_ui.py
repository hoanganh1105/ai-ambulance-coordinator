import osmnx as ox
from ipyleaflet import Map, Marker, GeoData, Icon
import ipywidgets as widgets
from IPython.display import display, clear_output
from shapely.geometry import Point

def create_dispatch_interface(place_name: str, symptoms_vocab: list[str]):
    # ==========================================
    # 1. KHỞI TẠO DỮ LIỆU
    # ==========================================
    print(f"Đang tải dữ liệu bản đồ cho {place_name}...")
    boundary_gdf = ox.geocode_to_gdf(place_name)
    exact_polygon = boundary_gdf.iloc[0]['geometry']
    center_lat = boundary_gdf.iloc[0]['lat']
    center_lon = boundary_gdf.iloc[0]['lon']

    # BIẾN TRẠNG THÁI
    current_state = 'SELECTING_AMBULANCE' 
    is_map_active = True # Cờ thay thế cho remove_interaction
    
    ambulance_pos = None
    patients_list = []
    
    current_selected_pos = None
    current_patient_symptoms = [] # Lưu danh sách triệu chứng đang nhập dở

    # ==========================================
    # 2. XÂY DỰNG GIAO DIỆN BẢN ĐỒ
    # ==========================================
    m = Map(center=(center_lat, center_lon), zoom=14)
    geo_data = GeoData(geo_dataframe=boundary_gdf, 
                       style={'color': 'red', 'fillOpacity': 0.05, 'weight': 2})
    m.add_layer(geo_data)

    cursor_marker = Marker(location=(0,0), draggable=False, opacity=0)
    m.add_layer(cursor_marker)

    # ==========================================
    # 3. XÂY DỰNG GIAO DIỆN ĐIỀU KHIỂN
    # ==========================================
    status_label = widgets.HTML(value="<b>BƯỚC 1:</b> Click bản đồ để CHỌN VỊ TRÍ XE CỨU THƯƠNG")
    error_label = widgets.Label(value="", style={'text_color': 'red'})
    log_area = widgets.Output(layout={'border': '1px solid black', 'height': '150px', 'overflow_y': 'auto'})
    
    # -- Giao diện chọn triệu chứng (MỚI) --
    symptom_input = widgets.Combobox(
        options=symptoms_vocab,
        placeholder='Gõ để tìm triệu chứng...',
        description='Triệu chứng:',
        ensure_option=True,
        layout={'width': '300px'}
    )
    btn_add_symptom = widgets.Button(description="Thêm TC", button_style='info', layout={'width': '80px'})
    symptoms_display = widgets.HTML(value="<i>Chưa có triệu chứng nào</i>")
    
    # Cụm UI triệu chứng (Ẩn ở bước chọn xe)
    symptom_ui = widgets.VBox([
        widgets.HBox([symptom_input, btn_add_symptom]),
        symptoms_display
    ])
    symptom_ui.layout.visibility = 'hidden'

    # -- Nút chức năng --
    btn_confirm = widgets.Button(description="Chốt Xe Cứu Thương", button_style='success')
    btn_finish = widgets.Button(description="Kết Thúc & Trả Kết Quả", button_style='warning')
    btn_finish.layout.visibility = 'hidden'

    # ==========================================
    # 4. LOGIC SỰ KIỆN
    # ==========================================
    def log_message(msg):
        with log_area:
            print(msg)

    def handle_map_click(**kwargs):
        nonlocal current_selected_pos
        if not is_map_active: return # Ngăn click nếu đã kết thúc
        
        if kwargs.get('type') == 'click':
            lat, lon = kwargs.get('coordinates')
            clicked_point = Point(lon, lat)
            
            if exact_polygon.contains(clicked_point):
                current_selected_pos = (lat, lon)
                cursor_marker.location = (lat, lon)
                cursor_marker.opacity = 0.5
                error_label.value = ""
                btn_confirm.disabled = False
            else:
                error_label.value = "Lỗi: Điểm bạn chọn nằm ngoài ranh giới!"
                btn_confirm.disabled = True

    def handle_add_symptom(b):
        val = symptom_input.value.strip()
        if val and val not in current_patient_symptoms:
            current_patient_symptoms.append(val)
            # Cập nhật dòng hiển thị
            badges = " | ".join([f"<b>{tc}</b>" for tc in current_patient_symptoms])
            symptoms_display.value = f"Đã thêm: {badges}"
        symptom_input.value = "" # Xóa trắng ô nhập để gõ tiếp

    def handle_confirm_click(b):
        nonlocal current_state, ambulance_pos, current_selected_pos, current_patient_symptoms
        
        if not current_selected_pos:
            error_label.value = "Bạn chưa chọn vị trí trên bản đồ!"
            return
            
        if current_state == 'SELECTING_AMBULANCE':
            ambulance_pos = current_selected_pos
            log_message(f"🚑 Đã chốt Xe Cứu Thương tại: {ambulance_pos}")
            m.add_layer(Marker(location=ambulance_pos, title="Ambulance"))
            
            # Chuyển form sang Bệnh nhân
            current_state = 'SELECTING_PATIENT'
            status_label.value = "<b>BƯỚC 2:</b> Chọn tọa độ BN -> Nhập các triệu chứng -> Bấm Thêm Bệnh Nhân"
            btn_confirm.description = "Thêm Bệnh Nhân"
            btn_finish.layout.visibility = 'visible'
            symptom_ui.layout.visibility = 'visible'
            
        elif current_state == 'SELECTING_PATIENT':
            if not current_patient_symptoms:
                error_label.value = "Vui lòng nhập ít nhất 1 triệu chứng trước khi thêm bệnh nhân!"
                return
                
            # Tạo object Patient (gọi class bạn đã định nghĩa ở ngoài)
            patient_id = len(patients_list) + 1
            new_patient = Patient(id=patient_id, symptoms=current_patient_symptoms.copy(), position=current_selected_pos)
            patients_list.append(new_patient)
            
            log_message(f"🤒 BN #{patient_id} tại {current_selected_pos} | TC: {current_patient_symptoms}")
            
            # Đánh dấu lên bản đồ
            red_icon = Icon(icon_url='https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png', icon_size=[25, 41], icon_anchor=[12, 41])
            m.add_layer(Marker(location=current_selected_pos, icon=red_icon, title=f"Patient {patient_id}"))
            
            # Reset form cho bệnh nhân tiếp theo
            current_patient_symptoms.clear()
            symptoms_display.value = "<i>Chưa có triệu chứng nào</i>"

        # Reset trỏ chuột bản đồ sau mỗi lần chốt
        current_selected_pos = None
        cursor_marker.opacity = 0
        # btn_confirm.disabled = True
        error_label.value = ""

    def handle_finish_click(b):
        nonlocal current_state, is_map_active
        current_state = 'DONE'
        is_map_active = False # Khóa bản đồ thay vì dùng remove_interaction
        
        status_label.value = "<b style='color:green;'>HOÀN TẤT!</b> Dữ liệu đã được lưu."
        cursor_marker.opacity = 0
        btn_confirm.disabled = True
        btn_finish.disabled = True
        symptom_input.disabled = True
        btn_add_symptom.disabled = True

    # Liên kết sự kiện
    m.on_interaction(handle_map_click)
    btn_add_symptom.on_click(handle_add_symptom)
    btn_confirm.on_click(handle_confirm_click)
    btn_finish.on_click(handle_finish_click)

    # ==========================================
    # 5. HIỂN THỊ
    # ==========================================
    clear_output()
    control_panel = widgets.VBox([
        status_label,
        error_label,
        symptom_ui,
        widgets.HBox([btn_confirm, btn_finish]),
        widgets.HTML("<b>Nhật ký hoạt động:</b>"),
        log_area
    ])
    
    display(widgets.VBox([m, control_panel]))
    
    return ambulance_pos, patients_list