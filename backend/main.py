from Fingerprint import Fingerprint
from FingerprintComparator import FingerprintComparator
from utils import formatSeconds

# TEST CASES

clarity1 = Fingerprint("./media/clarity1.wav")
clarity2 = Fingerprint("./media/clarity2.wav")
clarity1trim = Fingerprint("./media/clarity1trim.wav")
clarity2trim = Fingerprint("./media/clarity2trim.wav")
stay = Fingerprint("./media/stay.wav")
lebron = Fingerprint("./media/lebron.wav")
clarity1full = Fingerprint("./media/clarity1full.wav", 407)

# Create FingerprintComparator Instances for Cross Correlation and Comparisons
comparator_clarity = FingerprintComparator(clarity1, clarity2)
comparator_clarity_trim = FingerprintComparator(clarity1trim, clarity2trim)
comparator_stay = FingerprintComparator(clarity1, stay)
comparator_lebron = FingerprintComparator(clarity1, lebron)
comparator_clarity_full = FingerprintComparator(clarity2, clarity1full)

cross_correlation = comparator_clarity_full.crossCorrelate()
max_correlation = max(cross_correlation)
offsetSeconds = comparator_clarity_full.offsetToSeconds(cross_correlation)
print(f"Max Correlation (clarity1full vs clarity2): {max_correlation}")
print(comparator_clarity_full.displayTimestamp(offsetSeconds))

# Benchmarks
# print("Comparisons:")
# print("===================================")

# # Test Case 1: Same song, different recordings, not aligned
# print("Same song, different recordings, not aligned")
# print(f"Correlation (clarity1 vs clarity2): {comparator_clarity.correlate()}")
# print("\n")

# # Test Case 2: Same song, different recordings, manually aligned
# print("Same song, different recordings, manually aligned")
# print(f"Correlation (clarity1trim vs clarity2trim): {comparator_clarity_trim.correlate()}")
# print("\n")

# # Test Case 3: Same song, different recordings, cross-correlation aligned
# print("Same song, different recordings, cross correlation aligned")
# cross_correlation = comparator_clarity.crossCorrelate()
# max_correlation = max(cross_correlation)
# timestamp = comparator_clarity.generateTimestamp(cross_correlation)
# print(f"Max Correlation (clarity1 vs clarity2): {max_correlation}")
# print(f"clarity2 is {timestamp} seconds off from clarity1")
# print("\n")

# # Test Case 4: Same songs
# print("Same songs")
# print(f"Correlation (clarity1 vs clarity1): {FingerprintComparator(clarity1, clarity1).correlate()}")
# print("\n")

# # Test Case 5: Different songs
# print("Different songs")
# print(f"Correlation (clarity1 vs stay): {comparator_stay.correlate()}")
# print(f"Correlation (clarity2 vs stay): {FingerprintComparator(clarity2, stay).correlate()}")
# print("\n")

# # Test Case 6: Lebron James audio
# print("Lebron James")
# print(f"Correlation (lebron vs clarity1): {comparator_lebron.correlate()}")
# print(f"Correlation (lebron vs clarity2): {FingerprintComparator(lebron, clarity2).correlate()}")
# print(f"Correlation (lebron vs stay): {FingerprintComparator(lebron, stay).correlate()}")