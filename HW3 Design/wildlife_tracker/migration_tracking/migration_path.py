from typing import Optional
from wildlife_tracker.habitat_management.habitat import Habitat


class MigrationPath:

    def __init__(self,
                 species: str,
                 path_id: int,
                 start_location: Habitat,
                 destination: Habitat,
                 duration: Optional[int] = None) -> None:
        self.species = species
        self.path_id = path_id
        self.start_location = start_location
        self.destination = destination
        self.duration = duration

    def get_migration_path_details(self) -> dict:
        pass

    def update_migration_path_details(self, **kwargs) -> None:
        pass
