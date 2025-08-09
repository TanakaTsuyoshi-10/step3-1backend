from sqlalchemy import create_engine
import os
from pathlib import Path
from dotenv import load_dotenv

# プロジェクトルート（このファイルが db_control/～ にある想定）
BASE_DIR = Path(__file__).resolve().parents[1]

# ローカルだけ .env を読む（Azure では App Service の環境変数を os.getenv で読む）
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# DB 環境変数
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME')

# 必須チェック
missing = [k for k,v in {
    "DB_USER": DB_USER, "DB_PASSWORD": DB_PASSWORD,
    "DB_HOST": DB_HOST, "DB_PORT": DB_PORT, "DB_NAME": DB_NAME
}.items() if not v]
if missing:
    raise EnvironmentError(f"Missing DB envs: {', '.join(missing)}")

# CA 証明書の絶対パス（デプロイ物に含める）
cert_path = BASE_DIR / "DigiCertGlobalRootCA.crt.pem"
if not cert_path.exists():
    raise FileNotFoundError(f"CA cert not found: {cert_path}")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"ssl": {"ca": str(cert_path)}},  # ← ここがポイント
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,  # 必要なら True
)