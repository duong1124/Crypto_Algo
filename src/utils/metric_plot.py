from typing import List, Dict
import numpy as np
import matplotlib.pyplot as plt

def plot_performance_metrics(metrics: List[Dict[str, float]], algorithm_names: List[str]):
    """Plot performance metrics for different algorithms."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Plot encryption/decryption times
    enc_times = [m['encryption_time'] for m in metrics]
    dec_times = [m['decryption_time'] for m in metrics]
    
    x = np.arange(len(algorithm_names))
    width = 0.35
    
    ax1.bar(x - width/2, enc_times, width, label='Encryption')
    ax1.bar(x + width/2, dec_times, width, label='Decryption')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('Encryption/Decryption Performance')
    ax1.set_xticks(x)
    ax1.set_xticklabels(algorithm_names)
    ax1.legend()
    
    # Plot throughput
    throughput = [m['throughput'] for m in metrics]
    ax2.bar(algorithm_names, throughput)
    ax2.set_ylabel('Throughput (bytes/second)')
    ax2.set_title('Algorithm Throughput')
    
    plt.tight_layout()
    plt.show()

def save_metrics_to_file(metrics: Dict[str, float], filename: str):
    """Save performance metrics to a file."""
    with open(filename, 'w') as f:
        for key, value in metrics.items():
            f.write(f"{key}: {value}\n")

def load_metrics_from_file(filename: str) -> Dict[str, float]:
    """Load performance metrics from a file."""
    metrics = {}
    with open(filename, 'r') as f:
        for line in f:
            key, value = line.strip().split(': ')
            metrics[key] = float(value)
    return metrics 