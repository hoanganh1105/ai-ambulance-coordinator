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

    @classmethod
    def create_map_model(cls, place_name: str, model_name: str):
        if model_name == "simpleStreetMap":
            try:
                from modules.models.simple_street_graph import graph_from_place
                return graph_from_place(place_name, "drive")
            except ImportError:
                raise ImportError("MapRouter.create_map_model(): Trouble importing models.simple_street_map")
        elif model_name == "osmnxStreetMap":
            try:
                import osmnx
                return osmnx.graph_from_place(place_name, network_type="drive")
            except ImportError:
                raise ImportError("MapRouter.create_map_model(): Trouble importing osmnx")
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
    
    def optimal_path(self, origin: tuple[float], target: tuple[float]) -> list[tuple[float]]:
        """
        :param origin: Toạ độ điểm xuất phát
        :type origin: tuple[float]
        :param target: Toạ độ điểm kết thúc
        :type target: tuple[float]
        :return: optimal path theo toạ độ
        :rtype: list[tuple[float]]
        """
        # TO DO
        u = self.nearest_node(origin)
        v = self.nearest_node(target)
        
        print(f"Nearest nodes: source={u}, target={v}")
        
        if hasattr(self.model, '_node'):
            def h(node_id, target_id):
                node_coord = self.model._node[node_id]
                target_coord = self.model._node[target_id]
                return euclidean_distance(
                    (node_coord['y'], node_coord['x']), 
                    (target_coord['y'], target_coord['x'])
                )
            
            node_route = self.searcher(self.model, u, v, heuristic=h, weight='length')
        else:
            node_route = self.searcher(self.model, u, v, weight='length')
            
        if not node_route: 
            return []

        return [(self.model._node[node]['y'], self.model._node[node]['x']) for node in node_route]
    
    def show_map(self, org: tuple[float] = None, dests: list[tuple[float]] = None, route: list[tuple[float]] = None):
        """
        Hiển thị bản đồ.
        Nếu org != None thì hightlight org trên bản đồ.
        Nếu dests != None thì highlight các điểm thuộc dests trên bản đồ.
        Nếu route != None thì hightlight route trên bản đồ.
        
        :param org: Toạ độ hiện tại của xe cứu thương
        :type org: tuple[float]
        :param dests: Toạ độ của các bệnh nhân
        :type dests: list[tuple[float]]
        :param route: route theo toạ độ
        :type route: list[tuple[float]]
        """
        # TO DO
        import matplotlib.pyplot as plt
        if self.model_name == "simpleStreetMap":
            self.plotter(self.model, route=None) 
            ax = plt.gca()

            if route and len(route) > 1:
                lons = [pt[1] for pt in route]
                lats = [pt[0] for pt in route]
                ax.plot(lons, lats, color='red', linewidth=4, alpha=1, zorder=3, label='Path')

            if org:
                ax.scatter(org[1], org[0], c='#00FF00', s=200, edgecolors='white', zorder=5)

            if dests:
                for d in dests:
                    ax.scatter(d[1], d[0], c='#FF0000', s=150, marker='X', edgecolors='white', zorder=5)

            handles, labels = ax.get_legend_handles_labels()
            unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
            ax.legend(*zip(*unique), loc='upper right')
            
            plt.show()
        else:
            node_route = None
            if route and len(route) > 1:
                node_route = [self.nearest_node(pt) for pt in route]
            self.plotter(self.model, route=node_route, node_size=15)
            plt.show()
        
    
    def available_coordinates(self) -> list[tuple[float]]:
        """
        :return: Trả về tất cả toạ độ các node có trên map
        :rtype: list[tuple[float]]
        """
        # TO DO
        coords = [(node['y'], node['x']) for node in self.model._node.values()]
        return coords


    def nearest_node(self, point: tuple[float]) -> tuple[float]:
        """
        Trả về toạ độ điểm gần nhất theo khoảng cách chim bay
        :param point: toạ độ
        :type point: tuple[float]
        :return: toạ độ node gần nhất trong map
        :rtype: tuple[float]
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


def euclidean_distance(p1: tuple[float], p2: tuple[float]) -> float:
    """
    :param p1: Điểm thứ nhất
    :type p1: tuple[float]
    :param p2: Điểm thứ hai
    :type p2: tuple[float]
    :return: khoảng cách euclid
    :rtype: float
    """
    # TO DO
    from geopy.distance import geodesic
    return geodesic(p1, p2).meters

    