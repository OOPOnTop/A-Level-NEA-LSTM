import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from IPython.display import clear_output

# CONSTANTS
K = 10
MAX_ITERATIONS = 100
DATA = pd.read_csv("/Users/charlie/PycharmProjects/A-Level-NEA-LSTM/AI_models/Data_Assets/train_clean.csv")

class KMeans:
    def __init__(self, data, k=10):
        self.num_centroids = k
        self.classes = {}

        for i in range(self.num_centroids):
            self.classes[i] = i

        self.train_songs = data
        self.features = ["Danceability", "Energy", "Mode", "Speechiness", "Acousticness",
                         "Liveness", "Valence", "Tempo", "Duration", "Time Signature"]
        self.train_songs = self.train_songs.dropna(
            subset=self.features)
        self.train_data = self.train_songs[self.features].copy()
        try:
            self.centroids = pd.read_csv('centroids.csv')
        except FileNotFoundError:
            self.centroids = self.random_centroids()
        self.old_centroids = pd.DataFrame()
        self.labels = self.get_labels()
        self.iteration = 1

    def random_centroids(self):
        """centroids = []
        for i in range(self.num_centroids):
            centroid = self.train_data.apply(
                lambda x: float(x.sample())
            )
            centroids.append(centroid)
        return pd.concat(centroids, axis=1)"""
        centroids = self.train_data.sample(n=self.num_centroids, random_state=42)
        return centroids.reset_index(drop=True)

    def get_labels(self):
        if self.centroids.empty:
            return pd.Series()
        distances = self.centroids.apply(
            lambda x: np.sqrt(((self.train_data - x) ** 2).sum(axis=1)), axis=1
        )
        labels = distances.idxmin(axis=1)
        return labels

    def get_label(self, data_point):
        distances = []
        nearest_cluster = 0
        centroids = pd.DataFrame.to_numpy(self.centroids)
        for i in range(self.num_centroids):
            distance = 0
            for j in range(len(data_point)):
                distance += (np.abs((data_point[j][0] - centroids[i][j]))) ** 2

            distance = np.sqrt(distance)
            distances.append(distance)
            nearest_cluster = distances.index(min(distances)) + 1

        return nearest_cluster

    def new_centroids(self):
        """centroids = (self.train_data.groupby(self.labels)).apply(
            lambda x: np.exp(np.log(x).mean()).T
        )
        return centroids"""
        if self.labels is None or self.labels.empty:
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

            return centroids.sort_index()  # Ensure centroids are in the correct order
        except Exception as e:
            return pd.DataFrame()

    def run(self):
        while self.iteration < MAX_ITERATIONS and not self.centroids.equals(self.old_centroids):
            print(f"Iteration: {self.iteration}")  # Debugging line
            self.old_centroids = self.centroids
            self.labels = self.get_labels()

            if self.labels.empty:
                break

            self.centroids = self.new_centroids()
            if self.centroids.empty:
                break

            print(f"Plotting clusters at iteration {self.iteration}...")  # Debugging line
            self.plot_clusters()
            self.iteration += 1

        print("Finished running K-Means. Saving centroids to centroids.csv.")  # Debugging line
        if not self.centroids.empty:
            self.centroids = self.centroids.T
            self.centroids.to_csv('/Users/charlie/PycharmProjects/A-Level-NEA-LSTM/AI_models/centroids.csv', index=False)
        else:
            print("Error: self.centroids is empty. Cannot save to CSV.")

    def plot_clusters(self):
        if self.centroids.empty:
            return

        if self.labels.empty or len(self.labels) != len(self.train_data):
            return

        pca = PCA(n_components=2)
        data_2d = pca.fit_transform(self.train_data)

        if not self.centroids.empty:
            centroids_2d = pca.transform(self.centroids.T)
        else:
            return  # Exit the function if centroids are empty

        clear_output(wait=True)
        if self.iteration % 5 == 0:
            plt.title(f'Iteration: {self.iteration}')
            plt.scatter(x=data_2d[:, 0], y=data_2d[:, 1], c=self.labels)
            plt.scatter(x=centroids_2d[:, 0], y=centroids_2d[:, 1])
            plt.show()
        else:
            pass

"""kmeans = KMeans(DATA, K)
kmeans.run()"""