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

    @classmethod
    def create_estimator_model(cls, name: str):
        """
        Chọn model.
        :param name: tên model
        :type name: str
        """
        if name == "simpleBayesianNetwork":
            try:
                from models.simple_bayesian_network import SimpleBayesianNetwork
                return SimpleBayesianNetwork()
            except:
                raise ImportError("TrafficEstimator.create_estimator_model(): Trouble importing models.simple_bayesian_network")
        elif name == "pgmpyBayesianNetwork":
            try:
                from pgmpy.models import DiscreteBayesianNetwork
                return DiscreteBayesianNetwork()
            except:
                raise ImportError("TrafficEstimator.create_estimator_model(): Trouble importing models.simple_bayesian_network")
        raise ValueError(f"TrafficEstimator.create_estimator_model(): Unknown model name: {name}")

    def train(self, dataset_path:str):
        """
        Học dữ liệu từ dataset
        Dataset này đã được chuẩn hoá còn 5 cột chính
        (time_of_day, day_of_week, weather_condition, road_type và traffic_density_level)
        
        :param dataset_location: file path của dataset (.csv)
        :type dataset_location: str
        """

    def estimate_traffic_density_level(time_of_day: str,
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
        :param road_type: loại đường
        :type road_type: str
        :return: expected level value thuộc [0, 3] (do có 4 level)
        :rtype: float
        """
