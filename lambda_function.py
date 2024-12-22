import pymysql
import requests
from requests.exceptions import RequestException

def lambda_handler(event, context):
    try:
        print("Requesting data from the API...")
        api_url = "https://v3.football.api-sports.io/fixtures?live=all"
        headers = {"x-apisports-key": "24fcd56d1900ce220d7906f9f2a9ed87"}  # API-FOOTBALL API 키
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # 상태 코드가 200이 아니면 예외 발생
        matches = response.json()

        print("API response received: ", matches)

        # RDS 연결 정보 설정
        rds_host = "sports-db-instance.ap-northeast-2.rds.amazonaws.com"  # RDS 엔드포인트
        username = "admin"  # 사용자 이름
        password = "leesilla123!"  # 비밀번호
        db_name = "sports_db"  # 데이터베이스 이름

        # RDS 연결
        connection = pymysql.connect(
            host=rds_host,
            user=username,
            password=password,
            database=db_name,
            port=3306
        )
        print("Connected to RDS successfully!")
        cursor = connection.cursor()

        # 데이터 삽입/업데이트
        for match in matches['response']:
            fixture = match['fixture']
            teams = match['teams']
            goals = match['goals']
            status = fixture['status']['long']

            cursor.execute("""
                INSERT INTO matches (match_id, home_team, away_team, score_home, score_away, status, start_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                score_home=%s, score_away=%s, status=%s
            """, (
                fixture['id'], teams['home']['name'], teams['away']['name'],
                goals['home'], goals['away'], status, fixture['date'],
                goals['home'], goals['away'], status
            ))

        connection.commit()
        cursor.close()
        connection.close()
        print("Data updated successfully!")

    except RequestException as e:
        # API 호출에서 오류 발생 시 처리
        print(f"API call failed: {str(e)}")

    except pymysql.MySQLError as e:
        # MySQL 연결 오류 처리
        print(f"Database connection error: {str(e)}")

    except Exception as e:
        # 다른 일반적인 오류 처리
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    lambda_handler(None, None)  # 테스트를 위한 직접 호출
