"""
给定两个大小分别为 m 和 n 的正序（从小到大）数组 nums1 和 nums2。请你找出并返回这两个正序数组的 中位数 。
算法的时间复杂度应该为 O(log (m+n)) 。
示例 1：
输入：nums1 = [1,3], nums2 = [2]
输出：2.00000
解释：合并数组 = [1,2,3] ，中位数 2
示例 2：

输入：nums1 = [1,2], nums2 = [3,4]
输出：2.50000
解释：合并数组 = [1,2,3,4] ，中位数 (2 + 3) / 2 = 2.5

"""

from typing import List
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        nums = sorted(nums1 + nums2)
        n = len(nums)
        if n == 0:
            return 0.0
        mid = n // 2
        if n % 2 == 1:
            return float(nums[mid])
        return (nums[mid - 1] + nums[mid]) / 2.0

if __name__ == '__main__':
    solution = Solution()
    nums1 =  [1,5,6,9]
    nums2  =  [2,3,7]
    print(solution.findMedianSortedArrays(nums1, nums2))

