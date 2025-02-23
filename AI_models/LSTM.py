# Import libraries
import numpy as np
from AI_models.k_means_classification import KMeans
import pandas as pd
import json

# constants
NUM_FEATURES = 10  # 10 features
LEN_HISTORY = 50  # number of LSTM cells unrolled
np.random.seed(0)

# Initiate an object for training
k_means = KMeans(pd.read_csv("/Users/charlie/PycharmProjects/A-Level-NEA-LSTM/AI_models/Data_Assets/train_clean.csv", skiprows=1),
                 k=10)

"""
Features used in example data:
Danceability
Energy
Mode
Speechiness
Accousticness
Liveness
Valence
Tempo / 1000
Duration m_s / 1000000
Time Signature
"""

params = {'wf1': np.random.random((NUM_FEATURES, 1)),
          'wf2': np.random.random((NUM_FEATURES, 1)),
          'bf1': np.zeros((NUM_FEATURES, 1)),
          'wi1': np.random.random((NUM_FEATURES, 1)),
          'wi2': np.random.random((NUM_FEATURES, 1)),
          'wi3': np.random.random((NUM_FEATURES, 1)),
          'wi4': np.random.random((NUM_FEATURES, 1)),
          'bi1': np.zeros((NUM_FEATURES, 1)),
          'bi2': np.random.random((NUM_FEATURES, 1)),
          'wo1': np.random.random((NUM_FEATURES, 1)),
          'wo2': np.random.random((NUM_FEATURES, 1)),
          'bo1': np.zeros((NUM_FEATURES, 1)),
          'woa1': np.random.random((NUM_FEATURES, 1)),
          'boa1': np.zeros((NUM_FEATURES, 1))}


# Formatting csv file
def format_data(data):
    new_data = []
    data = pd.DataFrame.to_numpy(data)
    for i in data:
        _ = np.reshape(i, (12, 1))
        temp1 = np.delete(_, [0, 1])
        temp1 = np.reshape(temp1, (10, 1))
        temp1[7] /= 1000
        temp1[8] /= 1000000
        temp1 = temp1.astype(float)
        new_data.append(temp1)
    return new_data


DATA = pd.read_csv("/Users/charlie/PycharmProjects/A-Level-NEA-LSTM/AI_models/Data_Assets/train_clean.csv", skiprows=1)
DATA = format_data(DATA)


class LSTM:
    def __init__(self, net_input):
        """
       Initialises Network and input data and desired outputs

        self.input -- input data for all cells
        self.s_t_states -- short term states for every timestep
        self.l_t_states -- long term states for every timestep
        self.pred_states -- prediction states for every timestep
        self.predict -- output vector of predicted values at timestep

        self.l_t_next -- next long term state
        self.s_t_next -- next short term state

        self.cache -- tuple of values needed for back prop
        self.caches  -- list of all cell values needed for back prop

        self.loss -- Error for network

        self.''':
           w'' -- a weight matrix
           b'' -- a bias constant
           'f' -- forget gate phase
           'i' -- input gate phase
           'o' -- output gate phase
           'oa' -- output answer phase

       :param net_input:
       """
        self.input = net_input
        self.input_train = [k_means.get_label(i) for i in self.input]
        self.output_train = self.input_train

        self.init_s_t = np.random.random((NUM_FEATURES, 1))
        self.s_t_states = np.zeros((LEN_HISTORY, NUM_FEATURES, 1))
        self.l_t_states = np.zeros((LEN_HISTORY, NUM_FEATURES, 1))
        self.pred_states = np.zeros((LEN_HISTORY, NUM_FEATURES, 1))
        self.predict = None

        self.l_t_next = np.zeros((NUM_FEATURES, 1))
        self.s_t_next = self.init_s_t

        self.cache = None
        self.caches = []

        self.loss = None

        # Instantiate weights and biases
        try:
            with open('LSTM_weights.json', 'r') as f:
                self.params = {k: np.array(v) for k, v in json.load(f).items()}
        except FileNotFoundError:
            self.params = {'wf1': params['wf1'],
                           'wf2': params['wf2'],
                           'bf1': params['bf1'],
                           'wi1': params['wi1'],
                           'wi2': params['wi2'],
                           'wi3': params['wi3'],
                           'wi4': params['wi4'],
                           'bi1': params['bi1'],
                           'bi2': params['bi2'],
                           'wo1': params['wo1'],
                           'wo2': params['wo2'],
                           'bo1': params['bo1'],
                           'woa1': params['woa1'],
                           'boa1': params['boa1']}

        self.LSTM_cells = {}
        for i in range(len(self.input)):
            cell = LSTMCell(self.input[i], self.input)
            self.LSTM_cells['cell' + str(i)] = cell

    def cross_entropy(self, predict, target, epsilon=1e-8) -> float:
        """
        Used in calculating loss
        :param predict: model prediction
        :param target: Desired outcome
        :param epsilon: Constant
        :return: Loss
        """
        predict = np.clip(predict, epsilon, 1 - epsilon)
        return (-np.log(predict) * target).sum(axis=1).mean()

    def forward_propagate(self) -> any:
        """
        Algorithm that makes predictions for a given input
        :return: Predictions
        """
        for idx, cell in enumerate(self.LSTM_cells):
            if idx == 0:
                self.s_t_next, self.l_t_next, self.predict, self.cache = np.random.random((NUM_FEATURES, 1)), \
                    np.random.random(
                        (NUM_FEATURES, 1)), np.random.random(
                    (NUM_FEATURES, 1)), \
                    np.zeros((NUM_FEATURES, 1))
                self.LSTM_cells[cell].s_t_prev = np.random.random((NUM_FEATURES, 1))
                self.LSTM_cells[cell].l_t_prev = np.random.random((NUM_FEATURES, 1))

            else:
                self.LSTM_cells[cell].s_t_prev = self.LSTM_cells['cell' + str(idx - 1)].s_t_prev
                self.LSTM_cells[cell].l_t_prev = self.LSTM_cells['cell' + str(idx - 1)].l_t_prev

            i = list(self.LSTM_cells.keys()).index(cell)
            self.s_t_next, self.l_t_next, self.predict, self.cache = self.LSTM_cells[cell].forward_propagate()
            self.predict[7] *= 1000
            self.predict[8] *= 1000000
            self.s_t_states[i] = self.s_t_next
            self.l_t_states[i] = self.l_t_next
            self.pred_states[i] = self.predict
            self.caches.append(self.cache)

        self.caches = (self.caches, self.input)
        return self.pred_states, self.s_t_states, self.l_t_states, self.caches

    def get_prediction(self) -> np.array:
        return self.forward_propagate()[0][-1]

    def train(self, h, c) -> any:
        """
        Main training loop that aims to optimize parameters
        :param: h -> intitial short term state
        :param: c -> intitial long term state
        :return:
        """
        self.pred_states = []
        self.caches = []
        self.loss = 0

        self.LSTM_cells['cell0'].s_t_prev = np.random.random((NUM_FEATURES, 1))
        self.LSTM_cells['cell0'].l_t_prev = np.random.random((NUM_FEATURES, 1))

        i = 0
        for x, y_true in zip(self.input_train, self.output_train):
            if i >= 1:
                self.LSTM_cells['cell' + str(i)].s_t_prev = self.LSTM_cells['cell' + str(i - 1)].s_t_next
                self.LSTM_cells['cell' + str(i)].l_t_prev = self.LSTM_cells['cell' + str(i - 1)].l_t_next
            self.s_t_next, self.l_t_next, predict, cache = self.LSTM_cells['cell' + str(i)].forward_propagate()
            self.loss += self.cross_entropy(predict, y_true)

            self.pred_states.append(predict)
            self.caches.append(cache)
            i += 1
        self.loss /= np.array(self.input_train).shape[0]

        dh_next = np.zeros_like(h)
        dc_next = np.zeros_like(c)
        grads = {
            'Wf': np.zeros_like(self.params['wf1']),
            'Wi': np.zeros_like(self.params['wi1']),
            'Wc': np.zeros_like(self.params['wi3']),
            'Wo': np.zeros_like(self.params['wo1']),
            'Wy': np.zeros_like(self.params['woa1']),
            'bf': np.zeros_like(self.params['bf1']),
            'bi': np.zeros_like(self.params['bi1']),
            'bc': np.zeros_like(self.params['bi2']),
            'bo': np.zeros_like(self.params['bo1']),
            'by': np.zeros_like(self.params['boa1'])
        }

        i = 0
        for predict, y_true, cache in reversed(list(zip(self.pred_states, self.output_train, self.caches))):
            grad, dh_next, dc_next = self.LSTM_cells['cell' + str(i)].back_propagate(predict, y_true, dh_next, dc_next,
                                                                                     cache)
            i += 1
            for k in grads.keys():
                grads[k] += grad[k]

        with open('LSTM_weights.json', 'w') as f:
            json.dump({k: v.tolist() for k, v in self.params.items()}, f)

        return grads, 'loss: ', self.loss

    def train_epochs(self, n) -> float:
        """
        Trains the network for n iterations
        :param n: number of epochs
        :return: loss
        """
        for i in range(n):
            print(self.train(np.ones((NUM_FEATURES, 1)), np.zeros((NUM_FEATURES, 1))))
        return self.loss


class LSTMCell:
    def __init__(self, cell_input, net_input):
        """
       Initialise instance of class

       self.t_x  -- a matrix of features and values for input
       self.forget_gate -- vector output from forget gate
       self.input_gate -- vector output from input gate
       self.output_gate -- vector output from output gate
       self.candidate_l_t -- candidate value for long term state
       self.l_t_prev -- previous long term state
       self.s_t_prev -- previous short term state

       self.ds_next -- gradient of next short term state
       self.dl_next -- gradient of next long term state

       """
        self.params = params
        self.predict = None
        self.cache = []
        self.s_t_next = [[] for i in range(NUM_FEATURES)]
        self.l_t_next = [[] for i in range(NUM_FEATURES)]
        self.t_x = cell_input
        self.forget_gate = None
        self.input_gate = None
        self.output_gate = None
        self.candidate_l_t = np.zeros((NUM_FEATURES, 1))
        self.l_t_prev = None
        self.s_t_prev = None

        self.ds_next = None
        self.dl_next = None

    def softmax(self, x) -> np.array:
        return np.exp(x) / sum(np.exp(x))

    def sigmoid(self, x) -> np.array:
        return (np.exp(x)) / (np.exp(x) + 1)

    def derivative_sigmoid(self, x) -> np.array:
        return self.sigmoid(x) * (1 - self.sigmoid(x))

    def tanh(self, x) -> np.array:
        return np.tanh(x)

    def derivative_tanh(self, x) -> np.array:
        return 1 - (np.tanh(x)) ** 2

    def forward_propagate(self) -> any:
        """
       Updates long term and short term memory states
       One LSTM cell from unrolled net
       :return prediction and cache used for back prop:
       """
        self.s_t_prev = self.s_t_prev + self.t_x

        self.forget_gate = self.sigmoid((self.s_t_prev * self.params['wf1']) +
                                        (self.t_x * self.params['wf2']) + self.params['bf1'])
        self.input_gate = self.sigmoid((self.s_t_prev * self.params['wi1']) +
                                       (self.t_x * self.params['wi2']) + self.params['bi1'])
        self.candidate_l_t = self.tanh((self.s_t_prev * self.params['wi3']) +
                                       (self.t_x * self.params['wi4']) + self.params['bi2'])
        self.l_t_next = self.forget_gate * self.l_t_prev + self.input_gate * self.candidate_l_t
        self.output_gate = self.sigmoid((self.s_t_prev * self.params['wo1']) +
                                        (self.t_x * self.params['wo2']) + self.params['bo1'])
        self.s_t_next = self.output_gate * self.tanh(self.l_t_next)

        self.predict = self.softmax((self.s_t_next * self.params['woa1']) + self.params['boa1'])

        stuff = [self.s_t_next, self.l_t_next, self.s_t_prev, self.l_t_prev, self.forget_gate, self.input_gate,
                 self.candidate_l_t, self.output_gate, self.t_x, self.predict]

        for i in stuff:
            self.cache.append(i)

        return self.s_t_next, self.l_t_next, self.predict, self.cache

    def back_propagate(self, prob, y_train, dh_next, dc_next, cache) -> any:
        """
        Calculates derivatives for optimization and loss function
        :param: prob -> prediction
        :param: y_train -> expected outcome
        :param: dh_next -> next short term mem derivative
        :param: dc_next -> next long term mem derivative
        :param: cache -> Cache variable from forward propagation on cell
        :return: dict, arr, arr
        """
        # Unpack cache variable
        s_t_next = cache[0]
        l_t_next = cache[1]
        l_t_prev = cache[3]
        forget_gate = cache[4]
        input_gate = cache[5]
        candidate_l_t = cache[6]
        output_gate = cache[7]
        t_x = cache[8]

        # Softmax loss grad
        dy = prob
        for i in dy[1:y_train]:
            i[0] -= 1

        # Hidden to output grad
        dWy = s_t_next.T @ dy[:, 0]
        dby = dy

        dh = dy[:, 0].T @ self.params['woa1'] + dh_next

        # Grad for st before last multiply with lt
        dho = self.tanh(l_t_next) * dh
        dho = self.derivative_sigmoid(output_gate) * dho

        # Grad for lt in last multiply with st
        dc = output_gate * dh * self.derivative_tanh(l_t_next)
        dc = dc + dc_next

        # Grad for forget gate in computation of lt mem
        dhf = l_t_prev * dc
        dhf = self.derivative_sigmoid(forget_gate) * dhf

        # Grad for input gate in computation of lt mem
        dhi = candidate_l_t * dc
        dhi = self.derivative_sigmoid(input_gate) * dhi

        # Grad for candidate lt in computation of lt mem
        dhc = input_gate * dc
        dhc = self.derivative_tanh(candidate_l_t) * dhc

        # Gate grads
        dWf = (np.array(t_x).T * dhf[:, 0]).T
        dbf = dhf
        dXf = dhf.T @ self.params['wf1'][:, 0]

        dWi = (np.array(t_x).T * dhi[:, 0]).T
        dbi = dhi
        dXi = dhi.T @ self.params['wi1'][:, 0]

        dWo = (np.array(t_x).T * dho[:, 0]).T
        dbo = dho
        dXo = dho.T @ self.params['wo1'][:, 0]

        dWc = (np.array(t_x).T * dhc[:, 0]).T
        dbc = dhc
        dXc = dhc.T @ self.params['wi3'][:, 0]

        dX = dXo + dXc + dXi + dXf
        dh_next = dX[:NUM_FEATURES]
        dc_next = forget_gate * dc

        grad = dict(Wf=dWf, Wi=dWi, Wc=dWc, Wo=dWo, Wy=dWy, bf=dbf, bi=dbi, bc=dbc, bo=dbo, by=dby)

        return grad, dh_next, dc_next



"""example_data = [[[0.854], [0.564], [1], [0.0485], [0.0171], [0.0849], [0.53940], [0.134071], [0.2345960], [4]],
                [[0.382], [0.814], [1], [0.0406], [0.0011], [0.101], [0.34140], [0.116454], [0.251733], [4]]]

Lstm = LSTM(DATA)
Lstm.train_epochs(50)"""
