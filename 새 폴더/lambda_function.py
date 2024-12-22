import pymysql
import requests

def lambda_handler(event, context):
    # 스포츠 데이터 API 호출
    api_url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {"x-apisports-key": "24fcd56d1900ce220d7906f9f2a9ed87"}  # API-FOOTBALL API 키
    response = requests.get(api_url, headers=headers)
    matches = response.json()

    # RDS 연결 정보
    rds_host = "sports-db-instance.<region>.rds.amazonaws.com"  # RDS 엔드포인트
    username = "admin"  # 사용자 이름
    password = "leesilla123!"  # 비밀번호
    db_name = "sports_db"  # 데이터베이스 이름

    try:
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
    
    except Exception as e:
        print(f"Error: {str(e)}")

    return {"statusCode": 200, "body": "Lambda executed successfully"}
