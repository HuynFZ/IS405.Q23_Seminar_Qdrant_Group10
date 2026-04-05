from pyspark.sql import SparkSession
from qdrant_client import QdrantClient
import os
import sys

# --- THUỐC GIẢI LỖI ĐƯỜNG DẪN PYTHON TRÊN WINDOWS ---
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

print("\n--- ĐANG KIỂM TRA HỆ THỐNG CỦA THÁI ---")

# 1. Kiểm tra PySpark
try:
    spark = SparkSession.builder \
        .appName("Test_Thai_Env") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()
    print(f"✅ 1. PySpark: Khởi tạo THÀNH CÔNG! (Version: {spark.version})")
except Exception as e:
    print(f"❌ 1. PySpark: LỖI khởi tạo. Chi tiết: {e}")
# 2. Test Qdrant Docker của Huy
try:
    client = QdrantClient(url="http://localhost:6333")
    collections = client.get_collections()
    print("✅ Kết nối Qdrant THÀNH CÔNG!")
    print("Các Collection hiện có:", collections)
except Exception as e:
    print("❌ Lỗi Qdrant:", e)