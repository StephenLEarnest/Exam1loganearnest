import math
import random
import copy

# Ai helped write this code
def truncated_lognormal_sample(mu, sigma, dmin, dmax, n):
    """
    Generates N random samples from a truncated log-normal distribution.
    The function draws values from a log-normal distribution, then discards
    any values outside the specified range [dmin, dmax].

    Parameters:
    mu (float): Mean of the natural logarithm of the rock diameter.
    sigma (float): Standard deviation of the natural logarithm of the rock diameter.
    dmin (float): Minimum rock diameter allowed after sieving.
    dmax (float): Maximum rock diameter allowed after sieving.
    n (int): Number of samples to generate.

    Returns:
    list: List of N samples following the truncated log-normal distribution.
    """
    samples = []
    while len(samples) < n:
        sample = math.exp(random.gauss(mu, sigma))  # Generate log-normal sample
        if dmin <= sample <= dmax:
            samples.append(sample)
    return samples


def generate_samples(mu, sigma, dmin, dmax, num_samples=11, sample_size=100):
    """
    Generates multiple samples from the truncated log-normal distribution
    and calculates their means and variances. Each sample consists of a fixed
    number of rock sizes, and the statistics of each sample are computed.

    Parameters:
    mu (float): Mean of the natural logarithm of the rock diameter.
    sigma (float): Standard deviation of the natural logarithm of the rock diameter.
    dmin (float): Minimum rock diameter allowed after sieving.
    dmax (float): Maximum rock diameter allowed after sieving.
    num_samples (int): Number of independent samples to generate (default 11).
    sample_size (int): Number of observations per sample (default 100).

    Returns:
    list: List of sample means.
    list: List of sample variances.
    """
    sample_means = []
    sample_variances = []

    for _ in range(num_samples):
        sample = truncated_lognormal_sample(mu, sigma, dmin, dmax, sample_size)
        mean = sum(sample) / sample_size
        variance = sum((x - mean) ** 2 for x in sample) / (sample_size - 1)
        sample_means.append(mean)
        sample_variances.append(variance)

    return sample_means, sample_variances


def main():
    """
    Simulates an industrial-scale gravel sieving process by generating samples
    from a truncated log-normal distribution and reporting statistical properties.

    The program collects user inputs for the distribution parameters and sieve
    aperture limits, then generates multiple samples of rock diameters. It computes
    the mean and variance for each sample, as well as the overall mean and variance
    of the sample means.

    Assumptions:
    - Rocks are spherical.
    - The initial gravel sizes follow a log-normal distribution with parameters (mu, sigma).
    - Sieving truncates the distribution between Dmin and Dmax.
    """
    # User inputs with defaults
    mu = float(input("Enter the mean of ln(D) (default 0):") or 0)
    sigma = float(input("Enter the standard deviation of ln(D) (default 1):") or 1)
    dmin = float(input("Enter the minimum rock diameter (Dmin) (default 0.375):") or 0.375)
    dmax = float(input("Enter the maximum rock diameter (Dmax) (default 1):") or 1)

    # Generate samples
    sample_means, sample_variances = generate_samples(mu, sigma, dmin, dmax)

    # Calculate mean and variance of the sample means
    mean_of_means = sum(sample_means) / len(sample_means)
    variance_of_means = sum((x - mean_of_means) ** 2 for x in sample_means) / (len(sample_means) - 1)

    # Display results
    for i, (mean, var) in enumerate(zip(sample_means, sample_variances), 1):
        print(f"Sample {i}: Mean = {mean:.4f}, Variance = {var:.4f}")

    print(f"\nOverall mean of sample means: {mean_of_means:.4f}")
    print(f"Variance of sample means: {variance_of_means:.4f}")


if __name__ == "__main__":
    main()
