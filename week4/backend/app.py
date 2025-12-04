from flask import Flask, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Rutgers123456",
    "database": "test",
    "port": 3306,
    "charset": "utf8mb4"
}


def get_conn():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        port=DB_CONFIG["port"],
        charset=DB_CONFIG["charset"],
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/ping")
def ping():
    return {"msg": "pong"}

@app.route("/api/chart/rating_distribution")
def rating_distribution():
    sql = """
        SELECT 
          CASE 
            WHEN rating_avg < 2 THEN '0-2'
            WHEN rating_avg < 4 THEN '2-4'
            WHEN rating_avg < 6 THEN '4-6'
            WHEN rating_avg < 8 THEN '6-8'
            ELSE '8-10'
          END AS bucket,
          COUNT(*) AS count
        FROM movies
        WHERE rating_avg IS NOT NULL
        GROUP BY bucket
        ORDER BY bucket;
    """

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
    finally:
        conn.close()

    buckets = [row["bucket"] for row in rows]
    counts  = [row["count"]  for row in rows]

    option = {
        "title": {"text": "评分分布(rating_avg)"},
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category", "data": buckets},
        "yAxis": {"type": "value"},
        "series": [{
            "type": "bar",
            "data": counts
        }]
    }
    return jsonify(option)

@app.route("/api/chart/movies_per_year")
def movies_per_year():
    sql = """
        SELECT year, COUNT(*) AS count
        FROM movies
        WHERE year IS NOT NULL
        GROUP BY year
        ORDER BY year;
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
    finally:
        conn.close()

    years = [row["year"] for row in rows]      #x轴年份
    counts = [row["count"] for row in rows]    #y轴数量

    option = {
        "title": {"text": "按年份统计电影数量"},
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category", "data": years},
        "yAxis": {"type": "value"},
        "series": [{
            "name": "电影数量",
            "type": "line",
            "data": counts
        }]
    }
    return jsonify(option)



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
