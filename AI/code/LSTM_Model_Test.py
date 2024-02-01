import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from keras.models import Model
from keras.layers import Input, Dense, LSTM, Bidirectional
from keras import backend as K


class Bus:
    def __init__(self):
        pass

    # 버스 혼잡도 csv파일 전처리 과정
    def normal_data_preprocessing(self, path, prepro_check):
        main_data = pd.read_csv('../data/' + os.listdir(path)[0], names=['계절', '시간', '버스', '정류장', '혼잡도',
                                                                         '평휴일', '이전휴일수', '이후휴일수'])
        for i in os.listdir(path)[1:]:
            # 경기도 버스 csv 파일을 거르기 위한 if문
            if 'G' not in i:
                # 종종 csv 파일에 공백이 있는경우가 있는데 그러면 오류 나와서 이를 해결하기위해 만듦
                try:
                    temp_data = pd.read_csv(path + i, names=['계절', '시간', '버스', '정류장', '혼잡도',
                                                             '평휴일', '이전휴일수', '이후휴일수'])
                    main_data = pd.concat([main_data, temp_data], axis=0, ignore_index=True)
                except:
                    continue

        main_data = main_data.astype('int32')

        if prepro_check == 1:
            idx = main_data[((main_data['시간'] >= 700) & (main_data['시간'] <= 1000)) |
                            ((main_data['시간'] >= 1630) & (main_data['시간'] <= 2000))].index
            main_data.drop(idx, inplace=True)

        y = main_data['혼잡도']
        del main_data['혼잡도']

        # numpy array형식으로 변경 후 LSTM 모델 형식에 맞게 reshape
        X = np.array(main_data)
        X = X.reshape(len(X), len(X[0]), 1)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, random_state=777)

    # 모델 설계 과정
    def model_design(self):
        K.clear_session()
        xInput = Input(batch_shape=(None, self.X_train.shape[1], self.X_train.shape[2]))
        xLstm_1 = LSTM(10, return_sequences=True)(xInput)
        xLstm_2 = Bidirectional(LSTM(10))(xLstm_1)
        xOutput = Dense(1)(xLstm_2)
        self.model = Model(xInput, xOutput)
        self.model.compile(loss='mse', optimizer='adam')

    # 모델 학습
    def model_training(self):
        self.model.fit(self.X_train, self.y_train, epochs=1, batch_size=20, verbose=1)

    # 모델 결과 확인
    def model_result(self):
        self.result = self.model.predict(self.X_test, batch_size=1)
        self.show_result()

    # 결과를 그래프로 변환
    def show_result(self):
        b_axis = np.arange(0, len(self.result[0:200]))
        plt.figure(figsize=(20, 8))
        plt.plot(b_axis, self.result[0:200], 'o-', color='red', label='Predicted')
        plt.plot(b_axis, self.y_test[0:200], 'o-', color='green', alpha=0.2, label='Actual')
        plt.legend()
        plt.show()

    # class
    def bus_main(self, path, prepro_check):
        self.data_preprocessing(path, prepro_check)
        self.model_design()
        self.model_training()
        self.model_result()
        self.show_result()