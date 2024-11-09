import math
from typing import List


def lse(nums: List[float]) -> float:
    """Log sum exp"""
    largest = None
    if len(nums) == 0:
        raise Exception("LSE: Empty sequence")
    if len(nums) == 1:
        return nums[0]
    t = type(nums[0])
    if t == int or t == float:
        largest = max(*nums)
        return largest + math.log(sum(math.exp(z - largest) for z in nums))
