# Problem1: Online Election (https://leetcode.com/problems/online-election/)
# Time Complexity:O(n)+ O(log n)
# Constructor: O(n) we loop through all n votes exactly once, doing O(1) work per vote (dict get/set)
# q(t): O(log n) binary search over the times array, so it cuts the search space in half each step
# Space Complexity: O(n)
# countmap can hold up to n distinct people, one entry each
# leadermap holds exactly one entry per vote, so n entries
# Approach:
# We cannot recompute the leader from scratch for every query, that would be too slow.
# So instead, while processing the votes once, we record who is leading right after each vote.
# This gives us a map from "time of a vote" to "who was leading at that moment".
# For a query time that falls between two votes, the leader has not changed since the last vote,
# so we binary search for the closest earlier (or equal) recorded time and use that leader.

class TopVotedCandidate:

    def __init__(self, persons: list[int], times: list[int]):
        self.persons = persons
        self.times = times
        self.countmap = {}          # tracks how many votes each person has so far
        self.leadermap = {}         # maps a vote time to who is leading right after that vote
        leader = 0                  # placeholder leader before any votes are counted

        for i in range(len(persons)):
            person = persons[i]                     # who this vote was for
            time = times[i]                         # when this vote was cast

            self.countmap[person] = self.countmap.get(person, 0) + 1
            # add one to this person's vote count, default to 0 if first vote for them

            if self.countmap[person] >= self.countmap.get(leader, 0):
                # using >= (not >) makes sure that on a tie, the newest voter becomes leader,
                # which matches the rule that ties go to the most recent vote
                leader = person

            self.leadermap[time] = leader
            # lock in who is leading at this exact time, so q() can look it up later

    def q(self, t: int) -> int:

        if t in self.leadermap:
            return self.leadermap[t]
            # exact match, we already know the leader at this precise time

        low, high = 0, len(self.times) - 1
        while low <= high:
            mid = (low + high) // 2

            if self.times[mid] > t:
                high = mid - 1
                # mid's time is after our query time, so the answer must be to the left
            else:
                low = mid + 1
                # mid's time is at or before our query time, it could be the answer,
                # but a later time might also work, so keep searching right

        return self.leadermap[self.times[high]]
        # when the loop ends, high always sits on the last index whose time is <= t
        # that is the most recent vote before our query time, so its leader is the answer


# Your TopVotedCandidate object will be instantiated and called as such:
# obj = TopVotedCandidate(persons, times)
# param_1 = obj.q(t)