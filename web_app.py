# Render/Gunicorn で使う入口。更新スレッドはワーカー内で一度だけ起動する。
import threading
from app import app, update_loop, DEMO_MODE

if not DEMO_MODE:
    threading.Thread(target=update_loop, name="bus-fetcher", daemon=True).start()
