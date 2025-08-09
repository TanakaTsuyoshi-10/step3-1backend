from sqlalchemy import create_engine
import os
import platform

print("platform:", platform.uname())

main_path = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(main_path, "CRM.db")
print("db_path:", db_path)

engine = create_engine(f"sqlite:///{db_path}", echo=True)