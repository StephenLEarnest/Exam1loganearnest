import math
import random
import copy

#Ai helped write this code
def truncated_lognormal_sample(mu, sigma, dmin, dmax, n):
    """
    Generates N random samples from a truncated log-normal distribution.
    """
    samples = []
    while len(samples) < n:
        sample = math.exp(random.gauss(mu, sigma))
        if dmin <= sample <= dmax:
            samples.append(sample)
    return samples


def generate_samples(mu, sigma, dmin, dmax, num_samples=11, sample_size=100):
    """
    Generates multiple samples and computes their means and variances.
    """
    sample_means = []
    sample_variances = []

    for _ in range(num_samples):
        sample = truncated_lognormal_sample(mu, sigma, dmin, dmax, sample_size)
        mean = sum(sample) / sample_size
        variance = sum((x - mean) ** 2 for x in sample) / (sample_size - 1)
        sample_means.append(mean)
        sample_variances.append(variance)

    print(f"Sample Means: {sample_means}")
    print(f"Sample Variances: {sample_variances}")

    return sample_means, sample_variances


def t_test(mean_a, var_a, mean_b, var_b, n, alpha=0.05):
    """
    Performs a one-sided t-test to compare two suppliers' gravel sizes.
    """
    t_stat = (mean_a - mean_b) / math.sqrt((var_a / n) + (var_b / n))
    critical_value = 1.798  # Corrected critical value for df=20 at alpha=0.05 (one-sided)

    print(f"\nResults:")
    print(f"Supplier A - Mean: {mean_a:.4f}, Variance: {var_a:.4f}")
    print(f"Supplier B - Mean: {mean_b:.4f}, Variance: {var_b:.4f}")
    print(f"t-statistic: {t_stat:.4f}, Critical Value: {critical_value}")

    if t_stat > critical_value:
        print("Reject null hypothesis: samplingmeanA = samplingmeanB")
        print("Accept alternative hypothesis: samplingmeanA > samplingmeanB")
    else:
        print("Fail to reject null hypothesis: No significant difference in gravel size.")


def main():
    """
    Simulates an industrial-scale gravel sieving process and performs a t-test.
    """
    print("Enter the parameters for the feedstock that is common to both company A and company B:")
    mu = float(input("Enter the mean of ln(D) (default ln(2.0) = 0.693, where D is in inches):") or 0.693)
    sigma = float(input("Enter the standard deviation of ln(D) (default 1.0):") or 1.0)

    print("\nEnter parameters for company A sieving and sampling operations:")
    dmax_a = float(input("Enter the Large aperture size (default 1.0):") or 1.0)
    dmin_a = float(input("Enter the Small aperture size (default 0.375):") or 0.375)
    num_samples_a = int(input("Enter the number of samples (default 11):") or 11)
    sample_size_a = int(input("Enter the number of items in each sample (default 100):") or 100)

    print("\nEnter parameters for company B sieving and sampling operations:")
    dmax_b = float(input("Enter the Large aperture size (default 0.875):") or 0.875)
    dmin_b = float(input("Enter the Small aperture size (default 0.375):") or 0.375)
    num_samples_b = int(input("Enter the number of samples (default 11):") or 11)
    sample_size_b = int(input("Enter the number of items in each sample (default 100):") or 100)

    means_a, vars_a = generate_samples(mu, sigma, dmin_a, dmax_a, num_samples_a, sample_size_a)
    means_b, vars_b = generate_samples(mu, sigma, dmin_b, dmax_b, num_samples_b, sample_size_b)

    mean_a, var_a = sum(means_a) / len(means_a), sum(vars_a) / len(vars_a)
    mean_b, var_b = sum(means_b) / len(means_b), sum(vars_b) / len(vars_b)

    print(f"\nFinal Computed Means and Variances:")
    print(f"Supplier A - Mean: {mean_a:.4f}, Variance: {var_a:.4f}")
    print(f"Supplier B - Mean: {mean_b:.4f}, Variance: {var_b:.4f}")

    t_test(mean_a, var_a, mean_b, var_b, sample_size_a)

    if input("\nWould you like to run the test again? (yes/no): ").strip().lower() == "yes":
        main()


if __name__ == "__main__":
    main()



