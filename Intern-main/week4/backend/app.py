from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
CORS(app)

# ====== 配置区 ======
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Rutgers123456",
    "database": "test",
    "port": 3306,
    "charset": "utf8mb4"
}

#校验JWT的秘钥
SECRET_KEY = "sjdkshf289ryw79f0gahbnao47t69PHFBAIDHfsaavhoaBFJBIbfkBJBJBJKFBAL"

# ====== 数据库连接函数 ======
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


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        
        if not auth.startswith("Bearer "):
            return jsonify({"code": 401, "msg": "未登录"}), 401

        token = auth.split(" ", 1)[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"code": 401, "msg": "登录已过期"}), 401
        except Exception:
            return jsonify({"code": 401, "msg": "无效 token"}), 401

        
        request.user = {
            "id": payload["user_id"],
            "username": payload["username"]
        }
        return f(*args, **kwargs)
    return wrapper



@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not username or not email or not password:
        return jsonify({"code": 400, "msg": "缺少必填字段"}), 400

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM users WHERE username=%s OR email=%s",
                (username, email)
            )
            row = cur.fetchone()
            if row:
                return jsonify({"code": 409, "msg": "用户名或邮箱已存在"}), 409

            password_hash = generate_password_hash(password)

            cur.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, password_hash)
            )
            conn.commit()
            user_id = cur.lastrowid
    finally:
        conn.close()

    return jsonify({"code": 200, "msg": "注册成功", "user_id": user_id})


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"code": 400, "msg": "缺少必填字段"}), 400

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, password_hash FROM users WHERE username=%s",
                (username,)
            )
            row = cur.fetchone()
    finally:
        conn.close()

    if not row or not check_password_hash(row["password_hash"], password):
        return jsonify({"code": 401, "msg": "用户名或密码错误"}), 401

    payload = {
        "user_id": row["id"],
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return jsonify({"code": 200, "msg": "登录成功", "token": token})


@app.route("/api/me")
@login_required
def me():
    return jsonify({
        "code": 200,
        "user": request.user
    })


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

    years = [row["year"] for row in rows]      # x轴年份
    counts = [row["count"] for row in rows]    # y轴数量

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
