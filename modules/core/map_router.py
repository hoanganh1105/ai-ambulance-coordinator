class MapRouter:
    def __init__(self, place_name: str = "Delhi, India", model_name: str = "simpleStreetMap"):
        """
        Initialize MapRouter with specified place and model.
        Internally calls create_map_model(), create_searcher(), create_plotter().
        
        :param place_name: Tên khu vực (e.g., 'Delhi, India')
        :type place_name: str
        :param model_name: Tên model ('simpleStreetMap' hoặc 'osmnxStreetMap')
        :type model_name: str
        """
        self.model_name = model_name
        self.place = place_name
        self.model = self.create_map_model(place_name, model_name)
        self.searcher = self.create_searcher(model_name)
        self.plotter = self.create_plotter(model_name)
        self.add_edges_attribute("weight", lambda data: data.get("length"))
        def fix_highway_type(data):
            road_type = data.get("highway")
            if isinstance(road_type, list):
                return road_type[0]
            if not isinstance(road_type, str):
                return "unclassified"
            return road_type
        self.add_edges_attribute("highway", fix_highway_type)

    @classmethod
    def create_map_model(cls, place_name: str, model_name: str):
        if model_name == "simpleStreetMap":
            try:
                from modules.models.simple_street_graph import graph_from_place
                return graph_from_place(place_name, "drive")
            except ImportError:
                raise ImportError("MapRouter.create_map_model(): Trouble importing models.simple_street_map")
        # elif model_name == "osmnxStreetMap":
        #     try:
        #         import osmnx
        #         return osmnx.graph_from_place(place_name, network_type="drive")
        #     except ImportError:
        #         raise ImportError("MapRouter.create_map_model(): Trouble importing osmnx")
        raise ValueError(f"MapRouter.create_map_model(): Unknown model name: {model_name}")
    
    @classmethod
    def create_searcher(cls, model_name: str):
        if model_name == "simpleStreetMap":
            try:
                from modules.models.simple_search_algorithm import simple_astar
                return simple_astar
            except ImportError:
                raise ImportError("MapRouter.create_map_model(): Trouble importing models.simple_search_algorithm")
        elif model_name == "osmnxStreetMap":
            try:
                from networkx import astar_path
                return astar_path
            except ImportError:
                raise ImportError("MapRouter.create_map_model(): Trouble importing networkx")
        raise ValueError(f"MapRouter.get_searcher(): Unknown model name: {model_name}")
    
    @classmethod
    def create_plotter(cls, model_name: str):
        if model_name == "simpleStreetMap":
            try:
                from modules.models.simple_street_graph import plot_graph_route
                return plot_graph_route
            except ImportError:
                raise ImportError("MapRouter.get_plotter(): Trouble importing models.simple_street_graph")
        elif model_name == "osmnxStreetMap":
            try:
                from osmnx.plot import plot_graph_route
                return plot_graph_route
            except ImportError:
                raise ImportError("MapRouter.get_plotter(): Trouble importing osmnx")
        raise ValueError(f"MapRouter.get_plotter(): Unknown model name: {model_name}")
    
    def optimal_path(self, origin: tuple[float, float], target: tuple[float, float]) -> tuple[list[tuple[float, float]], int]:
        """
        :param origin: Toạ độ điểm xuất phát
        :type origin: tuple[float, float]
        :param target: Toạ độ điểm kết thúc
        :type target: tuple[float, float]
        :return: optimal path theo toạ độ
        :rtype: list[tuple[float, float]]
        """
        # TO DO
        u = self._nearest_node(origin)
        v = self._nearest_node(target)
        
        print(f"Nearest nodes: source={u}, target={v}")
        
        if hasattr(self.model, '_node'):
            def h(node_id, target_id):
                node_coord = self.model._node[node_id]
                target_coord = self.model._node[target_id]
                return euclidean_distance(
                    (node_coord['y'], node_coord['x']), 
                    (target_coord['y'], target_coord['x'])
                )
            
            node_route = self.searcher(self.model, u, v, heuristic=h, weight='weight')
        else:
            node_route = self.searcher(self.model, u, v, weight='weight')
            
        if not node_route: 
            return []

        return [(self.model._node[node]['y'], self.model._node[node]['x']) for node in node_route], self._shortest_length_of(node_route)
    
    def show_map(self, org: tuple[float, float] = None, dests: list[tuple[float, float]] = None, route: list[tuple[float, float]] = [], show_density: bool = False):
            """
            Hiển thị bản đồ.
            Dùng self.plotter để vẽ nền, sau đó vẽ đè heatmap và các icon lên trên.
            """
            import matplotlib.pyplot as plt
            import matplotlib.colors as mcolors

            # ==========================================
            # 1. GỌI SELF.PLOTTER ĐỂ VẼ NỀN (Lớp dưới cùng)
            # ==========================================

            # Nếu route có, convert sang node id cho osmnx vẽ luôn
            node_route = [self._nearest_node(pt) for pt in route] if route and len(route) > 1 else None
            self.plotter(self.model, route=node_route, node_size=15, show=False, close=False)
                
            ax = plt.gca() # Lấy bức tranh đang vẽ dở để chuẩn bị vẽ đè

            # ==========================================
            # 2. VẼ ĐÈ MÀU MẬT ĐỘ (Nếu show_density = True)
            # ==========================================
            if show_density:
                cmap = mcolors.LinearSegmentedColormap.from_list("density", ["#00FF00", "#FFFF00", "#FFA500", "#FF0000"])
                norm = mcolors.Normalize(vmin=0.0, vmax=3.0)
                nodes = self.model._node if hasattr(self.model, '_node') else self.model.nodes

                for u, v, data in self.model.edges(data=True):
                    x = [nodes[u]['x'], nodes[v]['x']]
                    y = [nodes[u]['y'], nodes[v]['y']]
                    
                    d_level = float(data.get('density_level', 0.0))
                    d_level = max(0.0, min(3.0, d_level))
                    
                    # Vẽ đè lên với zorder=2 (nền của plotter là 1), cho nét to hơn 1 tí để che nét cũ
                    ax.plot(x, y, color=cmap(norm(d_level)), linewidth=1.5, alpha=0.8, zorder=2)

            # ==========================================
            # 3. VẼ ĐÈ LỚP OVERLAYS (Xe, Bệnh nhân, Tuyến đường)
            # ==========================================
            # Vẽ đè Xe cứu thương
            if org:
                ax.scatter(org[1], org[0], c='#00FF00', s=200, edgecolors='white', zorder=5, label='Ambulance')

            # Vẽ đè Bệnh nhân
            if dests:
                for i, d in enumerate(dests):
                    lbl = 'Patient' if i == 0 else "" # Tránh lặp chữ Patient trong Legend
                    ax.scatter(d[1], d[0], c='#FF0000', s=150, marker='X', edgecolors='white', zorder=5, label=lbl)

            # Gom và dọn dẹp Legend
            handles, labels = ax.get_legend_handles_labels()
            if labels:
                unique_legend = dict(zip(labels, handles))
                ax.legend(unique_legend.values(), unique_legend.keys(), loc='upper right')

            # Triển lãm bản đồ cuối cùng
            plt.show()
        
    
    def available_coordinates(self) -> list[tuple[float, float]]:
        """
        :return: Trả về tất cả toạ độ các node có trên map
        :rtype: list[tuple[float, float]]
        """
        # TO DO
        coords = [(node['y'], node['x']) for node in self.model._node.values()]
        return coords


    def _nearest_node(self, point: tuple[float, float]) -> int:
        """
        Trả về toạ độ điểm gần nhất theo khoảng cách chim bay
        :param point: toạ độ
        :type point: tuple[float, float]
        :return: id node gần nhất trong map
        :rtype: int
        """
        # TO DO
        import osmnx as ox
        if not hasattr(self.model, '_node'):
            return ox.distance.nearest_node(self.model, X=point[1], Y=point[0])

        best_node = None
        min_dist = float('inf')
        for node_id, data in self.model._node.items():
            dist = ((data['x'] - point[1])**2 + (data['y'] - point[0])**2)**0.5
            if dist < min_dist:
                min_dist = dist
                best_node = node_id
        return best_node
    
    def _shortest_length_of(self, route: list[int]):
        total_sum = 0
        for i in range(len(route) - 1):
            u, v = route[i], route[i+1]
            
            edges = self.model._adj[u][v]
            shortest = min(attr["length"] for attr in edges.values())
            
            total_sum += shortest

        return total_sum

    def add_edges_attribute(self, attr: str, func):
        """
        Lặp qua các cạnh và thêm attr cho từng cạnh.
        Truyền data của cạnh cho func để nhận lại value tương ứng cho attr.
        Nếu attr đã tồn tại thì ghi đè.
        
        :param attr: Tên attribute muốn thêm
        :type attr: str
        :param func: Hàm nhận dict (edge data) và return value cho attribute
        :type func: Callable[[dict], Any]
        """
        # TO DO
        for u, v, key, data in self.model.edges(keys=True, data=True):
            self.model._adj[u][v][key][attr] = func(data)


def euclidean_distance(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """
    :param p1: Điểm thứ nhất
    :type p1: tuple[float, float]
    :param p2: Điểm thứ hai
    :type p2: tuple[float, float]
    :return: khoảng cách euclid
    :rtype: float
    """
    # TO DO
    from geopy.distance import geodesic
    return geodesic(p1, p2).meters

    