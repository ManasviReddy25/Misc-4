# Problem2: Largest Rectangle in histogram (https://leetcode.com/problems/largest-rectangle-in-histogram/)
# Time Complexity: O(n),Each index is pushed onto the stack once and popped at most once.
# Space Complexity: O(n),The stack can hold up to n indices in the worst case (heights sorted increasing).
# Approach:
# Use a stack to track indices of bars in increasing height order.
# For each bar, if the current bar is shorter than the bar on top of the stack, the top bar can't extend further right, so pop it and calculate its max area using the current index as the right boundary and the new stack top as the left boundary.
#After the loop, pop any bars left in the stack, using n as the right boundary since nothing shorter appeared after them.

       
class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        
        n = len(heights)
        result = 0
        stack = []
        stack.append(-1)  # fake left wall so width calculation never goes out of bounds

        for i in range(n):
            # pop while current bar is shorter than the bar at stack top
            while stack[-1] != -1 and heights[stack[-1]] > heights[i]:
                popped = stack.pop()                # index of the bar being closed off
                width = i - stack[-1] - 1            # distance between new top and current i
                result = max(result, heights[popped] * width)
            stack.append(i)  # current bar might extend further right, so keep it

        # clean up remaining bars, none of them found a shorter bar to their right
        while stack[-1] != -1:
            popped = stack.pop()
            width = n - stack[-1] - 1
            result = max(result, heights[popped] * width)

        return result
