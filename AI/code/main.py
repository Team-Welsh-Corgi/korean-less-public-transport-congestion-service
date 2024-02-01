import LSTM_Model_Test
import os
if __name__ == '__ main__':
    while True:
        check = None
        prepro_check = None
        print('원하는 설계를 입력하시오.')
        print('1. 전처리')
        print('2. 전처리 데이터 저장')
        print('3. 모델 설계 및 테스트')
        print('4. 모델 저장')

        check = int(input('>>'))

        if check == 1:
            print('전처리 과정을 선택하시오.')
            print('1. 출퇴근 시간을 포함한 전처리 데이터 만들기')
            print('2. 출퇴근 시간을 포함하지 않은 전처리 데이터 만들기')
            prepro_check = int(input('>>'))
