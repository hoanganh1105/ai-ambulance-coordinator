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
    Nodes là các biến ngẫu nhiên, edges thể hiện sự phụ thuộc giữa các biến này.
    """
    def __init__(self):
        """
        Initialize Bayesian Network.
        """
        super().__init__()
        self.cpds = {}  # {node_name: TabularCPT}

    def add_edge(self, u, v, **attrs):
        """
        Add edge from u to v and check DAG property (no cycles).
        :param u: Parent node
        :param v: Child node
        :param attrs: Edge attributes
        """
        # TO DO - kiểm tra DAG trước khi add
        super().add_edge(u, v, **attrs)

    def add_cpds(self, *cpds):
        """
        Add TabularCPT objects to network.
        :param cpds: Variable number of TabularCPT objects
        """
        # TO DO

    def get_cpds(self, node):
        """
        Return CPT of a node.
        :param node: Node name
        :return: TabularCPT object or None
        """
        # TO DO

    def check_model(self):
        """
        Validate model: all nodes have CPDs, probabilities sum to 1, DAG property.
        :return: True if valid, False otherwise
        """
        # TO DO


class SimpleInference:
    """
    Suy diễn trên SimpleBayesianNetwork.
    """
    def __init__(self, model: SimpleBayesianNetwork):
        """
        :param model: SimpleBayesianNetwork instance
        """
        # TO DO

    def query(self, variables, evidence=None) -> TabularCPT:
        """
        Compute posterior probability using inference.
        :param variables: List of nodes to query
        :type variables: list[str]
        :param evidence: Known evidence as {node: state}
        :type evidence: dict
        :return: TabularCPT with posterior distribution
        :rtype: TabularCPT
        """
        # TO DO