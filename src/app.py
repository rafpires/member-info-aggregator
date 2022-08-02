
import logging
import requests

from enum import Enum
from flask import Flask, request


class MemberStruct(Enum):
    """
    This is the json structure we expected from the external APIs, as well the structure we return
    """
    DEDUCTIBLE = 'deductible'
    STOP_LOSS = 'stop_loss'
    OOPS_MAX = 'oop_max'


class AggregationStrategies(Enum):
    """
    Implemented Strategies
    """
    AVG = 'AVG'
    MIN = 'MIN'
    MAX = 'MAX'


def create_app():
    """
    The app factory pattern.

    :return: the Flask app
    """

    app = Flask(__name__)
    app.config.from_prefixed_env()

    def fetch(member_id):
        """
        The URLs configurated on the env var SOURCES_URL are queried for the member's info.

        :param member_id: the member id for which we are gathering information
        :return: data from the APIs which returned valid data
        """
        accessible_values = []

        sources_url = app.config.get("SOURCES_URL").split()
        timeout = int(app.config.get("SOURCES_URL_TIMEOUT"))

        for url in sources_url:
            url = url.replace('{member_id}', str(member_id))
            try:
                response = requests.get(url=f'{url}', timeout=timeout)
                data = response.json()
                assert MemberStruct.DEDUCTIBLE.value in data
                assert MemberStruct.STOP_LOSS.value in data
                assert MemberStruct.OOPS_MAX.value in data
                accessible_values.append(response.json())
            except Exception as ex:
                logging.warning(f'Failed to access members data from [{url}]. Reason: {ex=}')

        return accessible_values

    def aggregate(data_from_sources, aggregation_strategy):
        """
        Process the data received based on the aggregation strategy informed

        :param data_from_sources: a list of dictionaries
        :param aggregation_strategy: AVG, MIN and MAX so far
        :return: the aggregate data by each field
        """

        aggregated_data = {}

        if aggregation_strategy == AggregationStrategies.AVG.value:
            aggregated_data[MemberStruct.DEDUCTIBLE.value] =\
                round(sum(d[MemberStruct.DEDUCTIBLE.value] for d in data_from_sources) / len(data_from_sources))
            aggregated_data[MemberStruct.STOP_LOSS.value] =\
                round(sum(d[MemberStruct.STOP_LOSS.value] for d in data_from_sources) / len(data_from_sources))
            aggregated_data[MemberStruct.OOPS_MAX.value] =\
                round(sum(d[MemberStruct.OOPS_MAX.value] for d in data_from_sources) / len(data_from_sources))
        elif aggregation_strategy == AggregationStrategies.MIN.value:
            aggregated_data[MemberStruct.DEDUCTIBLE.value] =\
                min(d[MemberStruct.DEDUCTIBLE.value] for d in data_from_sources)
            aggregated_data[MemberStruct.STOP_LOSS.value] =\
                min(d[MemberStruct.STOP_LOSS.value] for d in data_from_sources)
            aggregated_data[MemberStruct.OOPS_MAX.value] =\
                min(d[MemberStruct.OOPS_MAX.value] for d in data_from_sources)
        elif aggregation_strategy == AggregationStrategies.MAX.value:
            aggregated_data[MemberStruct.DEDUCTIBLE.value] =\
                max(d[MemberStruct.DEDUCTIBLE.value] for d in data_from_sources)
            aggregated_data[MemberStruct.STOP_LOSS.value] =\
                max(d[MemberStruct.STOP_LOSS.value] for d in data_from_sources)
            aggregated_data[MemberStruct.OOPS_MAX.value] =\
                max(d[MemberStruct.OOPS_MAX.value] for d in data_from_sources)

        return aggregated_data

    @app.route("/members/<int:member_id>/", methods=['GET'])
    def member_info(member_id):
        default_aggregation_strategy = app.config.get("DEFAULT_AGGREGATION_STRATEGY")
        aggregation_strategy = request.args.get('aggregation_strategy', default=default_aggregation_strategy, type=str)

        if aggregation_strategy not in [ag.value for ag in AggregationStrategies]:
            return f'Unimplemented aggregation strategy: {aggregation_strategy}', 400

        data_from_sources = fetch(member_id)

        if data_from_sources:
            aggregated_data = aggregate(data_from_sources, aggregation_strategy)
            return aggregated_data
        else:
            return f'All sources are unavailable', 400

    return app
