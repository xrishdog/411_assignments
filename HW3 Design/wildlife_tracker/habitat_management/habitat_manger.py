from typing import Any, List

from wildlife_tracker.animal_management.animal import Animal
from wildlife_tracker.habitat_management.habitat import Habitat


class HabitatManager:

    def __init__(self) -> None:
        self.habitats: dict[int, Habitat] = {}

    def assign_animals_to_habitat(habitat_id: int, animals: List[Animal]) -> None:
        pass

    def create_habitat(habitat_id: int, geographic_area: str, size: int, environment_type: str) -> Habitat:
        pass

    def get_animals_in_habitat(self, habitat_id: int) -> List[Animal]:
        pass

    def get_habitat_by_id(self, habitat_id: int) -> Habitat:
        pass

    def get_habitat_details(self, habitat_id: int) -> dict:
        pass

    def get_habitats_by_geographic_area(self, geographic_area: str) -> List[Habitat]:
        pass

    def get_habitats_by_size(self, size: int) -> List[Habitat]:
        pass

    def get_habitats_by_type(self, environment_type: str) -> List[Habitat]:
        pass

    def remove_habitat(self, habitat_id: int) -> None:
        pass

    def update_habitat_details(self, habitat_id: int, **kwargs: dict[str, Any]) -> None:
        pass
