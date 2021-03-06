"""Directive class definitions."""

from typing import Final

from ..base import Named
from ..census import Query
from ..models import (DirectiveData, DirectiveTierData,
                      DirectiveTreeCategoryData, DirectiveTreeData)
from ..proxy import InstanceProxy, SequenceProxy
from ..types import CensusData

from .objective import Objective


class DirectiveTreeCategory(Named, cache_size=10, cache_ttu=300.0):
    """A directive category.

    Directive tree category are the topmost directive categorisation,
    e.g. "Infantry".
    """

    collection = 'directive_tree_category'
    data: DirectiveTreeCategoryData
    id_field = 'directive_tree_category_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> DirectiveTreeCategoryData:
        return DirectiveTreeCategoryData.from_census(data)

    def trees(self) -> SequenceProxy['DirectiveTree']:
        """Return the trees in the category.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        query = Query(
            DirectiveTree.collection, service_id=self._client.service_id)
        query.add_term(field='directive_tree_id', value=self.id).limit(50)
        return SequenceProxy(DirectiveTree, query, client=self._client)


class DirectiveTree(Named, cache_size=30, cache_ttu=60.0):
    """A tree of directives.

    Directive trees are a chain of related directive, e.g.
    "Heavy Assault".
    """

    collection = 'directive_tree'
    data: DirectiveTreeData
    id_field = 'directive_tree_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> DirectiveTreeData:
        return DirectiveTreeData.from_census(data)

    def category(self) -> InstanceProxy[DirectiveTreeCategory]:
        """Return the category of the directive tree.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(DirectiveTreeCategory.collection,
                      service_id=self._client.service_id)
        query.add_term(field=DirectiveTreeCategory.id_field,
                       value=self.data.directive_tree_category_id)
        return InstanceProxy(DirectiveTreeCategory, query, client=self._client)

    def directives(self) -> SequenceProxy['Directive']:
        """Return the list of directives in this category.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        query = Query(Directive.collection, service_id=self._client.service_id)
        query.add_term(field='directive_tree_id', value=self.id).limit(400)
        return SequenceProxy(Directive, query, client=self._client)

    def tiers(self) -> SequenceProxy['DirectiveTier']:
        """Return the list of directive tiers in this category.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        query = Query(
            DirectiveTier.collection, service_id=self._client.service_id)
        query.add_term(field='directive_tree_id', value=self.id).limit(4)
        return SequenceProxy(DirectiveTier, query, client=self._client)


class DirectiveTier(Named, cache_size=30, cache_ttu=60.0):
    """A directive tier.

    Container for related directives, e.g. "Combat Medic: Adept".
    """

    collection = 'directive_tier'
    data: DirectiveTierData
    id_field = 'directive_tier_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> DirectiveTierData:
        return DirectiveTierData.from_census(data)

    def directives(self) -> SequenceProxy['Directive']:
        """Return the list of directives in this tier.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        query = Query(Directive.collection, service_id=self._client.service_id)
        query.add_term(field='directive_tier_id', value=self.id).limit(100)
        return SequenceProxy(Directive, query, client=self._client)

    def tree(self) -> InstanceProxy[DirectiveTree]:
        """Return the tree of the directive.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(
            DirectiveTree.collection, service_id=self._client.service_id)
        query.add_term(
            field=DirectiveTree.id_field, value=self.data.directive_tree_id)
        return InstanceProxy(DirectiveTree, query, client=self._client)


class Directive(Named, cache_size=30, cache_ttu=60.0):
    """A directive a character may complete."""

    collection = 'directive'
    data: DirectiveData
    id_field = 'directive_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> DirectiveData:
        return DirectiveData.from_census(data)

    def objectives(self) -> SequenceProxy[Objective]:
        """Return the objectives for this directive.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        # NOTE: This table is being treated as a single set mapping to multiple
        # objectives via their common group. This is a guess. I was not able to
        # find any directives with multiple objectives associated.
        collection: Final[str] = 'objective_set_to_objective'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(
            field='objective_set_id', value=self.data.objective_set_id)
        join = query.create_join(Objective.collection)
        join.set_fields('objective_group_id')
        join.set_list(True)
        return SequenceProxy(Objective, query, client=self._client)

    def tier(self) -> InstanceProxy[DirectiveTier]:
        """Return the tier of the directive.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(
            DirectiveTier.collection, service_id=self._client.service_id)
        query.add_term(
            field=DirectiveTier.id_field, value=self.data.directive_tier_id)
        return InstanceProxy(DirectiveTier, query, client=self._client)

    def tree(self) -> InstanceProxy[DirectiveTree]:
        """Return the tree of the directive.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(
            DirectiveTree.collection, service_id=self._client.service_id)
        query.add_term(
            field=DirectiveTree.id_field, value=self.data.directive_tree_id)
        return InstanceProxy(DirectiveTree, query, client=self._client)
