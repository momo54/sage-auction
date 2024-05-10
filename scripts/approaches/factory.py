from typing import Dict, List

from approaches.approach import Approach
from approaches.sage import SaGe


class ApproachFactory():

    @staticmethod
    def types() -> List[str]:
        return [
            "sage"]

    @staticmethod
    def create(approach: str, config: Dict[str, str]) -> Approach:
        if approach == "sage":
            return SaGe(approach, config)
        raise Exception(f"The approach named {approach} does not exist...")
