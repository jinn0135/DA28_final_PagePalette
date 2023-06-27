from datetime import datetime
import csv

# 페이지 기본 폼에서 마지막 페이지를 설정해주면 url 리스트를 반환
def page_lists(endpage):
    time = datetime.today().strftime("%Y:%m:%d")
    url_form = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105#&date=%'+str(time)+'&page='
    return [url_form+str(page_num) for page_num in range(1, endpage+1)]

# 개별 기사들의 URL이 담긴 csv파일을 읽어들인 list 반환
def read_csv_file(file_path=None, today=True):
    """
    file_path를 지정할 경우 : 해당 파일을 읽어와 list로 반환
    file_path를 지정하지 않을 경우, 자동적으로 오늘 날짜에 해당하는 파일 읽어와 list로 반환
    """
    if file_path != None:
        today=False
    if today:
        yymmdd = datetime.today().strftime("%y%m%d")
        file_path = 'urls_'+yymmdd+'.csv'
    data = []
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data.append(row[0])
    data.remove('URL')
    print(file_path, "로부터 csv파일 불러오기 성공")
    print("총 URL 수 :", len(data))
    return data