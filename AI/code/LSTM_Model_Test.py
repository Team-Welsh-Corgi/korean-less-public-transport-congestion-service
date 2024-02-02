import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import time

from sklearn.model_selection import train_test_split
from keras.models import Model
from keras.layers import Input, Dense, LSTM, Bidirectional
from keras import backend as K


class Bus:
    def __init__(self):
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.model = None
        self.result = None

    # 버스 혼잡도 csv파일 전처리 과정
    def data_preprocessing(self, path, prepro_check):
        main_data = pd.read_csv('../data/' + os.listdir(path)[0], names=['계절', '시간', '버스', '정류장', '혼잡도',
                                                                         '평휴일', '이전휴일수', '이후휴일수'])
        for i in os.listdir(path)[1:]:
            temp_data = pd.read_csv(path + i, names=['계절', '시간', '버스', '정류장', '혼잡도',
                                                     '평휴일', '이전휴일수', '이후휴일수'])
            main_data = pd.concat([main_data, temp_data], axis=0, ignore_index=True)
            print(i + '파일을 읽는 중 입니다.')

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
        if self.data_check():
            print('전처리 완료')
            self.data_result()
        else:
            print('전처리 과정에서 문제가 발생했습니다.')

    def data_result(self):
        check_label = [0 for i in range(100)]
        for i in self.y_train:
            check_label[i] += 1
        for i in self.y_test:
            check_label[i] += 1

        print('총 데이터의 양: ' + str(len(self.X_train) + len(self.X_test)))
        print('학습용 데이터의 양: ' + str(len(self.X_train)))
        print('테스트용 데이터의 양' + str(len(self.X_test)))
        print('\n라벨링 개수')
        for i in range(len(check_label)):
            if check_label[i] == 0:
                continue
            print(str(i) + '번: ' + str(check_label[i]))

    def data_save(self):
        if self.data_check():
            print('데이터가 잘못 처리되었습니다.')
        else:
            time_now = time.strftime('%y%m%d_%h%M%S', time.localtime(time.time()))
            np.save('../data/preprocessing/X_train' + time_now, self.X_train)
            print('파일이 저장되었습니다.\n저장 위치: data/preprocessing/X_train' + time_now)
            np.save('../data/preprocessing/y_train' + time_now, self.y_train)
            print('파일이 저장되었습니다.\n저장 위치: data/preprocessing/y_train' + time_now)
            np.save('../data/preprocessing/X_test' + time_now, self.X_test)
            print('파일이 저장되었습니다.\n저장 위치: data/preprocessing/X_test' + time_now)
            np.save('../data/preprocessing/y_test' + time_now, self.y_test)
            print('파일이 저장되었습니다.\n저장 위치: data/preprocessing/y_test' + time_now)

    def data_check(self):
        if (len(self.X_train) == len(self.y_train)) | (len(self.X_test) == len(self.y_test)) | \
                (len(self.X_train) == 0) | (len(self.y_train) == 0) | \
                (len(self.X_test) == 0) | (len(self.y_test) == 0):
            return False
        return True

    # 모델 설계 과정
    def model_design(self):
        K.clear_session()
        xinput = Input(batch_shape=(None, self.X_train.shape[1], self.X_train.shape[2]))
        xlstm_1 = LSTM(len(self.X_train), return_sequences=True)(xinput)
        xlstm_2 = Bidirectional(LSTM(len(self.X_train)))(xlstm_1)
        xoutput = Dense(1)(xlstm_2)
        self.model = Model(xinput, xoutput)
        self.model.compile(loss='mse', optimizer='adam')
        self.model.summary()

    # 모델 학습
    def model_training(self):
        self.model.fit(self.X_train, self.y_train, epochs=1, batch_size=20, verbose=1)

    # 모델 결과 확인
    def model_result(self):
        self.result = self.model.predict(self.X_test, batch_size=1)
        self.show_result()

    def model_save(self):
        time_now = time.strftime('%y%m%d_%h%M%S', time.localtime(time.time()))
        self.model.save('../model' + time_now + '.h5')

    # 결과를 그래프로 변환
    def show_result(self):
        b_axis = np.arange(0, len(self.result[0:200]))
        plt.figure(figsize=(20, 8))
        plt.plot(b_axis, self.result[0:200], 'o-', color='red', label='Predicted')
        plt.plot(b_axis, self.y_test[0:200], 'o-', color='green', alpha=0.2, label='Actual')
        plt.legend()
        plt.show()

    # 한번에 다실행하는 클래스 사용하진 않지만 테스트용으로 남겨놨음
    def bus_main(self, path, prepro_check):
        self.data_preprocessing(path, prepro_check)
        self.model_design()
        self.model_training()
        self.model_result()
        self.show_result()
