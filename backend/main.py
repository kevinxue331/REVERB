from Fingerprint import Fingerprint
from FingerprintComparator import FingerprintComparator
from utils import displayTimestamp, seconds

# TEST CASES

clarity1 = Fingerprint("./media/clarity1.wav")
clarity2 = Fingerprint("./media/clarity2.wav")
clarity1trim = Fingerprint("./media/clarity1trim.wav")
clarity2trim = Fingerprint("./media/clarity2trim.wav")
stay = Fingerprint("./media/stay.wav")
lebron = Fingerprint("./media/lebron.wav")
clarity1full = Fingerprint("./media/clarity1full.wav", 407)

# Create FingerprintComparator Instances for Cross Correlation and Comparisons
comparator_clarity_full = FingerprintComparator(clarity2, clarity1full)

cross_correlation = comparator_clarity_full.crossCorrelate()
max_correlation = max(cross_correlation)
offsetSeconds = seconds(comparator_clarity_full.getBestOffset(cross_correlation))
print(f"Max Correlation (clarity1full vs clarity2): {max_correlation}")
print(displayTimestamp(clarity2, clarity1full, offsetSeconds))
