# 크롤링 공통 추상 클래스
# 크롤러 공통 인터페이스 정의(OOP 방식)

# abc : Abstract Base Class의 약자, 아래처럼 추상 클래스를 정의할 수 있음 
# -> 해당 클래스는 직접 사용하는 것이 아닌 상속을 통해 사용해야함
from abc import ABC, abstractmethod

class BaseCrawler(ABC):
    @abstractmethod # 자식 클래스가 반드시 구현해야 하는 메서드의 뼈대 선언
    def crawl(self, url: str) -> str:
        """
        주어진 URL에서 HTML 콘텐츠를 가져오는 메서드
        :param url: 크롤링할 웹 페이지의 URL
        :return: 해당 페이지의 HTML 콘텐츠
        """
        pass

    # @abstractmethod
    # def parse(self, html_content: str) -> dict:
    #     """
    #     HTML 콘텐츠를 파싱하여 필요한 정보를 추출하는 메서드
    #     :param html_content: 크롤링한 HTML 콘텐츠
    #     :return: 추출된 정보가 담긴 딕셔너리
    #     """
    #     pass