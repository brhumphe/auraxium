"""Objective class definitions."""

from ..base import Cached
from ..census import Query
from ..models import ObjectiveData, ObjectiveTypeData
from ..proxy import InstanceProxy
from ..types import CensusData


class ObjectiveType(Cached, cache_size=10, cache_ttu=60.0):
    """A type of objective.

    This class mostly specifies the purpose of any generic parameters.
    """

    collection = 'objective_type'
    data: ObjectiveTypeData
    id_field = 'objective_type_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> ObjectiveTypeData:
        return ObjectiveTypeData.from_census(data)


class Objective(Cached, cache_size=10, cache_ttu=60.0):
    """A objective presented to a character."""

    collection = 'objective'
    data: ObjectiveData
    id_field = 'objective_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> ObjectiveData:
        return ObjectiveData.from_census(data)

    def type(self) -> InstanceProxy[ObjectiveType]:
        """Return the objective type of this objective."""
        query = Query(
            ObjectiveType.collection, service_id=self._client.service_id)
        query.add_term(
            field=ObjectiveType.id_field, value=self.data.objective_type_id)
        return InstanceProxy(ObjectiveType, query, client=self._client)
