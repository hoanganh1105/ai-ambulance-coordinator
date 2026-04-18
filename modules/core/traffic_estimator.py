import pandas as pd
import numpy as np
import itertools

# Fallback
ROAD_TYPE_FALLBACK_FROM_OSMNX = {
    # Nhóm 1: Highway (Đường cao tốc, trục cực lớn)
    'motorway': 'highway',
    'motorway_link': 'highway',
    'trunk': 'highway',
    'trunk_link': 'highway',

    # Nhóm 2: Main road (Đường huyết mạch, đường tỉnh/thành)
    'primary': 'main road',
    'primary_link': 'main road',
    'secondary': 'main road',
    'secondary_link': 'main road',
    'tertiary': 'main road',
    'tertiary_link': 'main road',

    # Nhóm 3: Inner road (Đường dân cư, đường nhỏ)
    'residential': 'inner road',
    'living_street': 'inner road',
    'service': 'inner road',
    'unclassified': 'inner road',
    'road': 'inner road'
}

class TrafficEstimator:
    def __init__(self, model_name: str = "simpleBayesianNetwork"):
        self.model = TrafficEstimator.create_estimator_model(model_name)
        self.inference = None 
        # Mapping các trạng thái
        self.state_maps = {
            'time_of_day': ['Morning Peak', 'Afternoon', 'Evening Peak', 'Night'],
            'day_of_week': ['Weekday', 'Weekend'],
            'weather_condition': ['Clear', 'Rain', 'Fog', 'Heatwave'],
            'road_type': ['highway', 'main road', 'inner road'],
            'traffic_density_level': ['Low', 'Medium', 'High', 'Very High']
        }

    @classmethod
    def create_estimator_model(cls, name: str):
        """
        Chọn model.
        :param name: tên model
        :type name: str
        """
        if name == "simpleBayesianNetwork":
            try:
                from modules.models.simple_bayesian_network import SimpleBayesianNetwork
                return SimpleBayesianNetwork()
            except Exception as e:
                raise ImportError(f"TrafficEstimator.create_estimator_model(): {e}")
        elif name == "pgmpyBayesianNetwork":
            try:
                from pgmpy.models import DiscreteBayesianNetwork
                return DiscreteBayesianNetwork()
            except Exception as e:
                raise ImportError(f"TrafficEstimator.create_estimator_model(): {e}")
        raise ValueError(f"TrafficEstimator.create_estimator_model(): Unknown model name: {name}")

    def train(self, dataset_path: str):
        """
        Học dữ liệu từ dataset
        Dataset này đã được chuẩn hoá còn 5 cột chính
        (time_of_day, day_of_week, weather_condition, road_type và traffic_density_level)
        :param dataset_location: file path của dataset (.csv)
        :type dataset_location: str
        """
        df = pd.read_csv(dataset_path)
        df['road_type'] = df['road_type'].str.lower()
        parents = ['time_of_day', 'day_of_week', 'weather_condition', 'road_type']

        # KIỂM TRA XEM ĐANG DÙNG MODEL NÀO
        is_pgmpy = type(self.model).__name__ == 'DiscreteBayesianNetwork'

        if is_pgmpy:
            # HUẤN LUYỆN BẰNG THƯ VIỆN PGMPY
            from pgmpy.estimators import MaximumLikelihoodEstimator
            from pgmpy.inference import VariableElimination

            for p in parents:
                self.model.add_edge(p, 'traffic_density_level')
            
            self.model.fit(df, estimator=MaximumLikelihoodEstimator)
            self.inference = VariableElimination(self.model)
            print("Huấn luyện pgmpyBayesianNetwork hoàn tất!")

        else:
            # HUẤN LUYỆN BẰNG MÔ HÌNH TỰ CODE
            from modules.models.simple_bayesian_network import TabularCPT, SimpleInference
            cpds = []
            
            for p in parents:
                self.model.add_edge(p, 'traffic_density_level')

            # Tính CPT cho các nút gốc
            for var in parents:
                states = self.state_maps[var]
                counts = df[var].value_counts().reindex(states, fill_value=0)
                probs = (counts + 1) / (counts.sum() + len(states)) # Laplace Smoothing
                
                cpd = TabularCPT(
                    variable=var, 
                    variable_card=len(states), 
                    values=probs.values
                )
                cpds.append(cpd)

            # Tính CPT cho nút mục tiêu
            parent_cards = [len(self.state_maps[p]) for p in parents]
            target_states = self.state_maps['traffic_density_level']
            target_card = len(target_states)

            groupby_cols = parents + ['traffic_density_level']
            counts = df.groupby(groupby_cols).size().reset_index(name='count')

            evidence_combinations = list(itertools.product(
                self.state_maps['time_of_day'],
                self.state_maps['day_of_week'],
                self.state_maps['weather_condition'],
                self.state_maps['road_type']
            ))

            cpt_values = []
            for combo in evidence_combinations:
                subset = counts[
                    (counts['time_of_day'] == combo[0]) &
                    (counts['day_of_week'] == combo[1]) &
                    (counts['weather_condition'] == combo[2]) &
                    (counts['road_type'] == combo[3])
                ]
                
                row_probs = []
                total_count = subset['count'].sum()
                
                for t_state in target_states:
                    val = subset[subset['traffic_density_level'] == t_state]['count'].values
                    c = val[0] if len(val) > 0 else 0
                    prob = (c + 1) / (total_count + target_card) # Laplace Smoothing
                    row_probs.append(prob)
                    
                cpt_values.append(row_probs)

            traffic_cpd = TabularCPT(
                variable='traffic_density_level',
                variable_card=target_card,
                values=cpt_values,
                evidence=parents,
                evidence_card=parent_cards
            )
            cpds.append(traffic_cpd)

            # Nạp CPTs vào mạng Bayes
            self.model.add_cpds(*cpds)

            if not self.model.check_model():
                raise ValueError("Lỗi mô hình: Mạng Bayes tạo ra không hợp lệ.")

            self.inference = SimpleInference(self.model)
            print("Huấn luyện simpleBayesianNetwork hoàn tất!")


    def estimate_traffic_density_level(self, 
                                       time_of_day: str,
                                       day_of_week: str,
                                       weather_condition: str,
                                       road_type: str) -> float:
        """
        Docstring for traffic_density_level_estimate
        :param time_of_day: "Morning Peak" / "Afternoon" / "Evening Peak" / "Night"
        :type time_of_day: str
        :param day_of_week: "Weekday" / "Weekend"
        :type day_of_week: str
        :param weather_condition: "Clear" / "Rain" / "Fog" / "Heatwave"
        :type weather_condition: str
        :param road_type: "highway" / "main road" / "inner road"
        :type road_type: str
        :return: expected level value thuộc [0, 3] (do có 4 level)
        :rtype: float
        """
        if self.inference is None:
            raise RuntimeError("Mô hình chưa được huấn luyện. Hãy gọi hàm train() trước.")

        raw_road = road_type.lower()
        processed_road = ROAD_TYPE_FALLBACK_FROM_OSMNX.get(raw_road, raw_road)
        is_pgmpy = type(self.model).__name__ == 'DiscreteBayesianNetwork'

        evidence_str = {
            'time_of_day': time_of_day,
            'day_of_week': day_of_week,
            'weather_condition': weather_condition,
            'road_type': processed_road
        }

        for k, v in evidence_str.items():
            if v not in self.state_maps[k]:
                raise ValueError(f"Dữ liệu đầu vào không hợp lệ tại '{k}': {v}")

        if is_pgmpy:
            # DỰ ĐOÁN BẰNG PGMPY
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore") # Tắt cảnh báo FutureWarning của pgmpy
                res = self.inference.query(variables=['traffic_density_level'], evidence=evidence_str)
            
            state_names = res.state_names['traffic_density_level']
            probs = res.values
            mapping = {'Low': 0, 'Medium': 1, 'High': 2, 'Very High': 3}

            expected_level = 0.0
            for i, state in enumerate(state_names):
                expected_level += mapping[state] * probs[i]
            return expected_level

        else:
            # DỰ ĐOÁN BẰNG MÔ HÌNH TỰ CODE
            evidence_idx = {}
            for k, v in evidence_str.items():
                evidence_idx[k] = self.state_maps[k].index(v)
                
            result_cpt = self.inference.query(variables=['traffic_density_level'], evidence=evidence_idx)
            
            expected_level = 0.0
            for x, prob in enumerate(result_cpt.values):
                expected_level += x * prob
            return expected_level
