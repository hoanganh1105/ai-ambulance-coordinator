class SimpleStreetGraph:
    """
    A minimal directed multigraph for modeling states with spatial coordinates.
    """
    def __init__(self):
        """
        Internal data structures:
        - self._node: {node_id: {attributes}}
        {attributes} ít nhất phải có 'x' and 'y' (toạ độ)
        node_id phải là int
        - self._adj: {u: {v: {key: {attributes}}}}
        {attributes} ít nhất phải có 'length' và 'highway'
        u, v là id của node, key phải là int
        """
        self._node = {}
        self._adj = {} 
        # Có thể định nghĩa thêm các attribute khác.

    # ---------- Data Ingestion ----------
    def add_node(self, n: int, **attrs):
        """
        Thêm node.
        :param n: node muốn thêm vào.
        :type n: int
        :param attrs: attribute của node
        """
        # TO DO
        if n not in self._node:
            self._node[n] = attrs
            self._adj[n] = {}

    def add_edge(self, u: int, v: int, key: int = None, **attrs):
        """
        Thêm cạnh.
        :param u: cạnh bắt đầu
        :type u: int
        :param v: cạnh kết thúc
        :type v: int
        :param key: key của cạnh. Nếu đã tồn tại thì ghi đè, nếu là None thì tạo cạnh với key mới.
        :type key: int
        :param attrs: attribute của cạnh
        """
        # TO DO
        if u not in self._node:
            raise ValueError(f"Node {u} does not exist.")
        elif v not in self._node:
            raise ValueError(f"Node {v} does not exist.")

        if u not in self._adj:
            self._adj[u] = {}
        if v not in self._adj[u]:
            self._adj[u][v] = {}
        
        if key is None:
            key = len(self._adj[u][v])
        self._adj[u][v][key] = attrs
            

    # ---------- Other ----------
    # Có thể định nghĩa thêm property, method...
    @property
    def nodes(self):
        """
        Trả về generator các node.
        Mimic NetworkX MultiDiGraph.nodes()
        :return: generator trả về (node_id, {attributes})
        :rtype: generator
        """
        for node_id, attrs in self._node.items():
            yield (node_id, attrs)
        
    def edges(self, nbunch=None, keys=False, data=False):
        """
        Generator trả về edges.
        Mimic NetworkX MultiDiGraph.edges()
        
        :param nbunch: node hoặc list node để query edges từ. Nếu None thì return tất cả edges.
        :type nbunch: int or list[int]
        :param keys: Nếu True thì include key trong output
        :type keys: bool
        :param data: Nếu True thì include edge attributes trong output
        :type data: bool
        :return: generator trả về edges
        
        Examples:
            G.edges()  # (u, v), (u, v), ...
            G.edges(keys=True)  # (u, v, key), (u, v, key), ...
            G.edges(data=True)  # (u, v, {attrs}), (u, v, {attrs}), ...
            G.edges(keys=True, data=True)  # (u, v, key, {attrs}), ...
        """
        if nbunch is None:
            nbunch = self._adj
        
        for u in nbunch:
            if u in self._adj:
                for v in self._adj[u]:
                    for key in self._adj[u][v]:
                        if keys and data:
                            yield (u, v, key, self._adj[u][v][key])
                        elif keys:
                            yield (u, v, key)
                        elif data:
                            yield (u, v, self._adj[u][v][key])
                        else:
                            yield (u, v)
    


def graph_from_place(place_name: str, network_type: str='drive') -> SimpleStreetGraph:
    """
    Create SimpleStreetMap from OSM place name (mimics osmnx.graph_from_place)
    by converting the Multigraph returned by osmnx.graph_from_place into an instance of this class

    :param place_name: Name of place (e.g., 'Manhattan, New York')
    :type place_name: str
    :param network_type: 'drive', 'walk', 'bike', 'all'
    :type network_type: str
    :return: SimpleStreetGraph
    :rtype: SimpleStreetGraph
    """
    # TO DO
    import osmnx as ox
    G = ox.graph_from_place(place_name, network_type=network_type)
    simple_graph = SimpleStreetGraph()
    for node_id, data in G.nodes(data=True):
        simple_graph.add_node(node_id, **data)
    
    for u, v, key, data in G.edges(keys=True, data=True):
        attrs = {
            'length': data.get('length', 1), 
            'highway': data.get('highway', 'unclassified')
        }
        for attr_key, attr_value in data.items():
            if attr_key not in attrs:
                attrs[attr_key] = attr_value
        simple_graph.add_edge(u, v, key, **attrs)

    return simple_graph

def plot_graph_route(G: SimpleStreetGraph, route: list[int] = None, route_color: str = 'r', route_linewidth: float = 4, node_size: float = 15):
    """
    Hiển thị bản đồ, background màu #111111, cạnh màu #999999
    :param G: Đồ thị đường đi
    :type G: SimpleStreetGraph
    :param route: đường đi dạng list id của các node
    :type route: list[int]
    :param route_color: màu sắc highlight route
    :type route_color: str
    :param route_linewidth: độ dày route
    :type route_linewidth: float
    :param node_size: kích thước node
    :type node_size: float
    """
    # TO DO
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='#111111')
    ax.set_facecolor('#111111')
    
    for u, v, data in G.edges(data=True):
        x = [G._node[u]['x'], G._node[v]['x']]
        y = [G._node[u]['y'], G._node[v]['y']]
        ax.plot(x, y, color='#999999', linewidth=0.5, alpha=0.5, zorder=1)
    
    if route and len(route) > 1:
        route_x = [G._node[node]['x'] for node in route]
        route_y = [G._node[node]['y'] for node in route]
        ax.plot(route_x, route_y, color=route_color, linewidth=route_linewidth, alpha=1, zorder=2)
    
    if node_size > 0:
        node_x = [data['x'] for data in G._node.values()]
        node_y = [data['y'] for data in G._node.values()]
        ax.scatter(node_x, node_y, color='#555555', s=node_size, alpha=0.3, zorder=1)
    
    ax.set_axis_off()