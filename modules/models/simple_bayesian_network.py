import networkx as nx

class TabularCPT:
    # TO DO
    # Class này có thể chỉnh sửa tuỳ ý
    def __init__(self, variable, variable_card, values, evidence=None, evidence_card=None):
        """
        :param variable: Tên nút (String)
        :param variable_card: Số trạng thái của nút (Int)
        :param values: Bảng xác suất (2D list hoặc Numpy array)
        :param evidence: Danh sách tên các nút cha (List of Strings)
        :param evidence_card: Danh sách số trạng thái của các nút cha (List of Ints)
        """
        self.variable = variable
        self.variable_card = variable_card
        self.values = values
        self.evidence = evidence or []
        self.evidence_card = evidence_card or []

    def __str__(self):
        """
        Pretty print CPT as a formatted table with borders.
        """
        import numpy as np
        
        if not self.evidence:
            # Single variable, no evidence
            values = np.array(self.values) if not isinstance(self.values, np.ndarray) else self.values
            
            # Calculate column widths
            col1_width = len(f"{self.variable}(state_name)") + 2
            col2_width = 10
            
            lines = []
            lines.append("+" + "-" * (col1_width + 2) + "+" + "-" * (col2_width + 2) + "+")
            
            for i in range(self.variable_card):
                var_str = f"{self.variable}(state_{i})"
                prob_str = f"{values[i]:.5f}"
                lines.append(f"| {var_str:<{col1_width}} | {prob_str:>{col2_width}} |")
                lines.append("+" + "-" * (col1_width + 2) + "+" + "-" * (col2_width + 2) + "+")
            
            return "\n".join(lines)
        else:
            # With evidence
            values = np.array(self.values) if not isinstance(self.values, np.ndarray) else self.values
            
            col1_width = 35
            col2_width = 10
            
            lines = []
            lines.append("+" + "-" * (col1_width + 2) + "+" + "-" * (col2_width + 2) + "+")
            
            total_evidence_states = 1
            for card in self.evidence_card:
                total_evidence_states *= card
            
            for ev_idx in range(total_evidence_states):
                # Calculate evidence state indices
                ev_states = []
                temp = ev_idx
                for card in reversed(self.evidence_card):
                    ev_states.insert(0, temp % card)
                    temp //= card
                
                # Format evidence state
                evidence_str = ", ".join([f"{self.evidence[i]}={ev_states[i]}" 
                                         for i in range(len(self.evidence))])
                
                values_for_ev = values[ev_idx] if total_evidence_states > 1 else values
                values_str = ", ".join([f"{val:.5f}" for val in values_for_ev])
                
                label = f"{self.variable}({evidence_str})"
                lines.append(f"| {label:<{col1_width}} | {values_str:>{col2_width}} |")
                lines.append("+" + "-" * (col1_width + 2) + "+" + "-" * (col2_width + 2) + "+")
            
            return "\n".join(lines)


class SimpleBayesianNetwork(nx.DiGraph):
    """
    Simple Bayesian Network kế thừa từ NetworkX DiGraph.
    """
    def __init__(self):
        super().__init__()
        self.cpds = {}  # {node_name: TabularCPT}

    def add_edge(self, u, v, **attrs):
        """
        Thêm cạnh và kiểm tra đồ thị có bị chu trình (cycles) hay không.
        Mạng Bayes bắt buộc phải là DAG (Directed Acyclic Graph).
        """
        super().add_edge(u, v, **attrs)
        if not nx.is_directed_acyclic_graph(self):
            self.remove_edge(u, v)
            raise ValueError(f"Lỗi: Thêm cạnh {u} -> {v} tạo ra chu trình. Mạng Bayes phải là DAG.")

    def add_cpds(self, *cpds):
        """
        Thêm các bảng phân phối xác suất (CPD) vào mạng.
        """
        for cpd in cpds:
            self.cpds[cpd.variable] = cpd

    def get_cpds(self, node=None):
        """
        Lấy CPD của một nút cụ thể, hoặc toàn bộ nếu không truyền tham số.
        """
        if node is None:
            return self.cpds
        return self.cpds.get(node)

    def check_model(self):
        """
        Kiểm tra tính hợp lệ của mô hình: 
        1. Phải là DAG.
        2. Mọi nút đều phải có CPD.
        3. Tổng xác suất của các trạng thái trong mỗi điều kiện phải bằng 1.
        """
        if not nx.is_directed_acyclic_graph(self):
            print("Lỗi: Mô hình không phải là đồ thị DAG.")
            return False
            
        for node in self.nodes:
            if node not in self.cpds:
                print(f"Lỗi: Nút '{node}' bị thiếu bảng CPT.")
                return False
                
            cpd = self.cpds[node]
            # Tính tổng xác suất dọc theo hàng (axis=-1)
            sums = np.sum(cpd.values, axis=-1)
            if not np.allclose(sums, 1.0):
                print(f"Lỗi: Tổng xác suất của nút '{node}' không bằng 1. Tổng hiện tại: {sums}")
                return False
                
        return True


import networkx as nx
import numpy as np
import itertools

class TabularCPT:
    def __init__(self, variable, variable_card, values, evidence=None, evidence_card=None):
        """
        :param variable: Tên nút (String)
        :param variable_card: Số trạng thái của nút (Int)
        :param values: Bảng xác suất (2D list hoặc Numpy array)
        :param evidence: Danh sách tên các nút cha (List of Strings)
        :param evidence_card: Danh sách số trạng thái của các nút cha (List of Ints)
        """
        self.variable = variable
        self.variable_card = variable_card
        # Đảm bảo values luôn là Numpy array để dễ tính toán
        self.values = np.array(values) 
        self.evidence = evidence or []
        self.evidence_card = evidence_card or []

    def __str__(self):
        """
        Pretty print CPT as a formatted table with borders.
        """
        if not self.evidence:
            values = self.values
            col1_width = len(f"{self.variable}(state_name)") + 2
            col2_width = 10
            lines = ["+" + "-" * (col1_width + 2) + "+" + "-" * (col2_width + 2) + "+"]
            
            for i in range(self.variable_card):
                var_str = f"{self.variable}(state_{i})"
                prob_str = f"{values[i]:.5f}"
                lines.append(f"| {var_str:<{col1_width}} | {prob_str:>{col2_width}} |")
                lines.append("+" + "-" * (col1_width + 2) + "+" + "-" * (col2_width + 2) + "+")
            return "\n".join(lines)
        else:
            values = self.values
            col1_width = 35
            col2_width = 10
            lines = ["+" + "-" * (col1_width + 2) + "+" + "-" * (col2_width + 2) + "+"]
            
            total_evidence_states = 1
            for card in self.evidence_card:
                total_evidence_states *= card
            
            for ev_idx in range(total_evidence_states):
                ev_states = []
                temp = ev_idx
                for card in reversed(self.evidence_card):
                    ev_states.insert(0, temp % card)
                    temp //= card
                
                evidence_str = ", ".join([f"{self.evidence[i]}={ev_states[i]}" for i in range(len(self.evidence))])
                values_for_ev = values[ev_idx] if total_evidence_states > 1 else values
                values_str = ", ".join([f"{val:.5f}" for val in values_for_ev])
                
                label = f"{self.variable}({evidence_str})"
                lines.append(f"| {label:<{col1_width}} | {values_str:>{col2_width}} |")
                lines.append("+" + "-" * (col1_width + 2) + "+" + "-" * (col2_width + 2) + "+")
            return "\n".join(lines)


class SimpleBayesianNetwork(nx.DiGraph):
    """
    Simple Bayesian Network kế thừa từ NetworkX DiGraph.
    """
    def __init__(self):
        super().__init__()
        self.cpds = {}  # {node_name: TabularCPT}

    def add_edge(self, u, v, **attrs):
        """
        Thêm cạnh và kiểm tra đồ thị có bị chu trình (cycles) hay không.
        Mạng Bayes bắt buộc phải là DAG (Directed Acyclic Graph).
        """
        super().add_edge(u, v, **attrs)
        if not nx.is_directed_acyclic_graph(self):
            self.remove_edge(u, v)
            raise ValueError(f"Lỗi: Thêm cạnh {u} -> {v} tạo ra chu trình. Mạng Bayes phải là DAG.")

    def add_cpds(self, *cpds):
        """
        Thêm các bảng phân phối xác suất (CPD) vào mạng.
        """
        for cpd in cpds:
            self.cpds[cpd.variable] = cpd

    def get_cpds(self, node=None):
        """
        Lấy CPD của một nút cụ thể, hoặc toàn bộ nếu không truyền tham số.
        """
        if node is None:
            return self.cpds
        return self.cpds.get(node)

    def check_model(self):
        """
        Kiểm tra tính hợp lệ của mô hình: 
        1. Phải là DAG.
        2. Mọi nút đều phải có CPD.
        3. Tổng xác suất của các trạng thái trong mỗi điều kiện phải bằng 1.
        """
        if not nx.is_directed_acyclic_graph(self):
            print("Lỗi: Mô hình không phải là đồ thị DAG.")
            return False
            
        for node in self.nodes:
            if node not in self.cpds:
                print(f"Lỗi: Nút '{node}' bị thiếu bảng CPT.")
                return False
                
            cpd = self.cpds[node]
            # Tính tổng xác suất dọc theo hàng (axis=-1)
            sums = np.sum(cpd.values, axis=-1)
            if not np.allclose(sums, 1.0):
                print(f"Lỗi: Tổng xác suất của nút '{node}' không bằng 1. Tổng hiện tại: {sums}")
                return False
                
        return True


class SimpleInference:
    """
    Module suy diễn (Inference) bằng phương pháp Duyệt toàn bộ (Enumeration).
    """
    def __init__(self, model: SimpleBayesianNetwork):
        self.model = model
        if not self.model.check_model():
            raise ValueError("Mô hình không hợp lệ. Vui lòng kiểm tra lại đồ thị hoặc các bảng CPT.")

    def query(self, variables, evidence=None):
        """
        Tính xác suất hậu nghiệm P(Query | Evidence).
        """
        evidence = evidence or {}
        all_vars = list(self.model.nodes)
        var_cards = {var: self.model.get_cpds(var).variable_card for var in all_vars}
        
        # 1. Khởi tạo tất cả các "thế giới có thể xảy ra" (All possible worlds)
        ranges = [range(var_cards[v]) for v in all_vars]
        all_worlds = list(itertools.product(*ranges))
        
        # 2. Lọc bỏ các thế giới vi phạm Evidence (Quan sát thực tế)
        valid_worlds = []
        for world in all_worlds:
            world_dict = dict(zip(all_vars, world))
            match_evidence = all(world_dict[k] == v for k, v in evidence.items())
            if match_evidence:
                valid_worlds.append(world_dict)
                
        # 3. Hàm tính xác suất kết hợp (Joint Probability) của một thế giới
        def get_joint_prob(world_dict):
            p = 1.0
            for var in all_vars:
                cpd = self.model.get_cpds(var)
                var_state = world_dict[var]
                
                if not cpd.evidence:
                    val = cpd.values[var_state]
                else:
                    # Tra cứu ma trận đa chiều bằng cách tính chỉ số (index)
                    ev_idx = 0
                    multiplier = 1
                    for i in reversed(range(len(cpd.evidence))):
                        ev_name = cpd.evidence[i]
                        ev_state = world_dict[ev_name]
                        ev_card = cpd.evidence_card[i]
                        ev_idx += ev_state * multiplier
                        multiplier *= ev_card
                    val = cpd.values[ev_idx][var_state]
                p *= val
            return p

        # 4. Gom nhóm và tính tổng xác suất (Marginalization) cho biến truy vấn
        query_var = variables[0] # Trong phiên bản đơn giản này, ta hỗ trợ query 1 biến
        query_card = var_cards[query_var]
        posterior_probs = np.zeros(query_card)
        
        for world_dict in valid_worlds:
            prob = get_joint_prob(world_dict)
            q_state = world_dict[query_var]
            posterior_probs[q_state] += prob
            
        # 5. Chuẩn hóa (Normalization) để tổng xác suất bằng 1
        total_prob = np.sum(posterior_probs)
        if total_prob > 0:
            posterior_probs = posterior_probs / total_prob
            
        # Trả về kết quả dưới dạng một TabularCPT mới
        return TabularCPT(variable=query_var, variable_card=query_card, values=posterior_probs)