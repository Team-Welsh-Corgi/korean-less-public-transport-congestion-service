import LSTM_Model_Test


LMT = LSTM_Model_Test.Bus()
while True:
    prepro_check = None
    print('원하는 설계를 입력하시오.')
    print('1. 전처리')
    print('2. 전처리 데이터 저장')
    print('3. 모델 설계 및 테스트')
    print('4. 모델 저장')
    print('5. 종료')

    check = int(input('>> '))

    if check == 1:
        print('1. 서울버스')
        print('2. 경기버스')
        path_check = int(input('>> '))
        if path_check == 1:
            path = '../data/seoul/'
        elif path_check == 2:
            path = '../data/gyeonggi/'
        else:
            print('잘못 입력했습니다.')
            continue

        print('전처리 과정을 선택하시오.(data 폴더안에 서울과 경기도 위치에 따라 csv 파일을 넣어주세요.)')
        print('1. 출퇴근 시간을 포함하지 않은 전처리 데이터 만들기')
        print('2. 출퇴근 시간을 포함한 전처리 데이터 만들기')
        prepro_check = int(input('>> '))

        if prepro_check != 1 | prepro_check != 2:
            print('잘못 입력했습니다.')
            continue

        print('전처리를 시작합니다.')
        LMT.data_preprocessing(path=path, prepro_check=prepro_check)
    elif check == 2:
        LMT.data_save()
    elif check == 3:
        print('모델 설계를 시작합니다.')
        LMT.model_design()
        LMT.model_training()
        LMT.model_result()
    elif check == 4:
        LMT.model_save()
    elif check == 5:
        break
    else:
        print('잘못 입력했습니다.')
