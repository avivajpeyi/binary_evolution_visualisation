import numpy as np
from typing import Tuple


def convert_to_scientific_notation(number: float) -> Tuple[float, float]:
    """Get scientific notation of a number """
    b = int(np.log10(np.fabs(number)))
    a = number / 10 ** b
    return a, b
