import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from IPython.display import clear_output

# CONSTANTS
K = 10
MAX_ITERATIONS = 100
DATA = pd.read_csv('Data_Assets/train_clean.csv')


class KMeans:
    def __init__(self, data, k=10):
        self.num_centroids = k
        self.classes = {}

        for i in range(self.num_centroids):
            self.classes[i] = i

        self.train_songs = data
        self.features = ['Danceability', 'Energy', 'Mode', 'Speechiness', 'Acousticness',
                         'Liveness', 'Valence', 'Tempo', 'Duration', 'Time Signature']
        self.train_songs = self.train_songs.dropna(subset=self.features)
        self.train_data = self.train_songs[self.features].copy()
        print("Shape of train_data in __init__:", self.train_data.shape)  # Debugging line

        try:
            self.centroids = pd.read_csv('centroids.csv')
            print("Centroids loaded from CSV with shape:", self.centroids.shape)  # Debugging line
        except FileNotFoundError:
            print("centroids.csv not found. Initializing random centroids...")  # Debugging line
            self.centroids = self.random_centroids()

        self.old_centroids = pd.DataFrame()
        self.labels = self.get_labels()
        self.iteration = 1

    def random_centroids(self):
        print("Shape of train_data in random_centroids:", self.train_data.shape)  # Debugging line
        centroids = self.train_data.sample(n=self.num_centroids, random_state=42)
        print("Random centroids initialized with shape:", centroids.shape)  # Debugging line
        return centroids.reset_index(drop=True)

    def get_labels(self):
        if self.centroids.empty:
            print("Error: self.centroids is empty. Cannot compute labels.")
            return pd.Series()  # Return an empty Series safely

        print("Shape of centroids in get_labels:", self.centroids.shape)  # Debugging line
        distances = self.centroids.apply(
            lambda x: np.sqrt(((self.train_data - x) ** 2).sum(axis=1)), axis=1
        )
        labels = distances.idxmin(axis=1)
        print("Length of labels: ", len(labels))  # Debugging line
        return labels

    def new_centroids(self):
        if self.labels is None or self.labels.empty:
            print("Error: self.labels is empty. Cannot compute new centroids.")
            return pd.DataFrame()  # Return an empty DataFrame safely

        try:
            # Compute mean per cluster
            centroids = self.train_data.groupby(self.labels).mean()

            # Handle empty clusters
            if len(centroids) < self.num_centroids:
                missing_clusters = set(range(self.num_centroids)) - set(centroids.index)
                for cluster in missing_clusters:
                    # Reinitialize the centroid for the empty cluster
                    new_centroid = self.train_data.sample(n=1, random_state=42).iloc[0]
                    centroids.loc[cluster] = new_centroid

            print("New centroids computed with shape:", centroids.shape)  # Debugging line
            return centroids.sort_index()  # Ensure centroids are in the correct order
        except Exception as e:
            print(f"Error computing new centroids: {e}")
            return pd.DataFrame()

    def run(self):
        while self.iteration < MAX_ITERATIONS and not self.centroids.equals(self.old_centroids):
            print(f"Iteration: {self.iteration}")  # Debugging line
            self.old_centroids = self.centroids
            self.labels = self.get_labels()

            if self.labels.empty:
                print("Error: self.labels is empty. Exiting loop.")
                break

            self.centroids = self.new_centroids()
            if self.centroids.empty:
                print("Error: self.centroids is empty. Exiting loop.")
                break

            print(f"Plotting clusters at iteration {self.iteration}...")  # Debugging line
            self.plot_clusters()
            self.iteration += 1

        print("Finished running K-Means. Saving centroids to centroids.csv.")  # Debugging line
        if not self.centroids.empty:
            self.centroids.to_csv('centroids.csv', index=False)
        else:
            print("Error: self.centroids is empty. Cannot save to CSV.")

    def plot_clusters(self):
        if self.centroids.empty:
            print("Error: self.centroids is empty. Cannot plot clusters.")
            return

        if self.labels.empty or len(self.labels) != len(self.train_data):
            print("Error: self.labels is invalid. Cannot plot clusters.")
            return

        pca = PCA(n_components=2)
        data_2d = pca.fit_transform(self.train_data)
        centroids_2d = pca.transform(self.centroids)

        clear_output(wait=True)
        if self.iteration % 5 == 0:
            plt.title(f'Iteration: {self.iteration}')
            plt.scatter(x=data_2d[:, 0], y=data_2d[:, 1], c=self.labels, cmap='viridis')
            plt.scatter(x=centroids_2d[:, 0], y=centroids_2d[:, 1], c='red', marker='X', s=200)
            plt.show()
        else:
            pass

kmeans = KMeans(DATA, K)
kmeans.run()