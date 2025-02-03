import matplotlib.pyplot as plt

def plot_histogram(data_dict, title, top_k=30, figsize=(10, 5)):
    # Extract keys and values from the dictionary
    data_dict = dict(sorted(data_dict.items(), key=lambda x: x[1], reverse=True)[:top_k])

    categories = list(data_dict.keys())
    frequencies = list(data_dict.values())

    # Create a figure and axis
    plt.figure(figsize=figsize)
    # Plot the histogram
    plt.bar(categories, frequencies, color='skyblue')

    # Add labels and title
    plt.xlabel('Categories')
    plt.ylabel('Frequencies')
    plt.title('Histogram of ' + title)
    
    avg_len = sum([len(item) for item in categories]) / len(categories)  # Average length of the categories
    if avg_len > 1:
        plt.xticks(rotation=90)
    # Show the plot
    plt.show()
