from abc import ABC, abstractmethod
from typing import List, Optional
import json
import numpy as np
from pydantic import Field
from swarmauri.core.vectors.IVector import IVector
from swarmauri.core.ComponentBase import ComponentBase, ResourceTypes

class VectorBase(IVector, ComponentBase):
    data: List[float]
    resource: Optional[str] =  Field(default=ResourceTypes.VECTOR.value, frozen=True)

    def to_numpy(self) -> np.ndarray:
        """
        Converts the vector into a numpy array.

        Returns:
            np.ndarray: The numpy array representation of the vector.
        """
        return np.array(self.data)
        
    def __len__(self):
        return len(self.data)
