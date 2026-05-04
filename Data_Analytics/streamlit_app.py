import streamlit as st
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from datasets import load_dataset
import pandas as pd
import os, sys

st.set_page_config(page_title="H&M Semantic Search", page_icon="🔍", layout="wide")
st.title("🛍️ H&M: Spark SQL vs Qdrant Semantic Search")

# 1. Khởi tạo Cache cho toàn bộ hệ thống
@st.cache_resource
def load_systems():
    # Khai báo token Hugging Face (Nên lấy từ file secrets để bảo mật)
    # Nếu không muốn dùng secrets, bạn có thể gán trực tiếp: hf_token = "hf_MãTokenCủaBạn..."
    hf_token = st.secrets["HF_TOKEN"] if "HF_TOKEN" in st.secrets else None
    
    # Khởi tạo Qdrant & AI Model (Đã thêm tham số token)
    qclient = QdrantClient(url="http://localhost:6333") 
    model = SentenceTransformer('BAAI/bge-small-en-v1.5', token=hf_token) 
    
    # Khởi tạo Spark (Ultra-Safe Mode)
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
    spark = SparkSession.builder \
        .appName("HM_Web_Demo") \
        .config("spark.driver.memory", "4g") \
        .getOrCreate()
        
    # Nạp dữ liệu vào Spark (Cũng truyền token vào load_dataset để tải data an toàn)
    dataset = load_dataset("Qdrant/hm_ecommerce_products", split="train", token=hf_token)
    pdf = dataset.to_pandas()[['article_id', 'prod_name', 'detail_desc', 'department_name']]
    pdf_clean = pdf.fillna("").astype(str)
    data_list = pdf_clean.values.tolist()
    
    schema = StructType([
        StructField("article_id", StringType(), True),
        StructField("prod_name", StringType(), True),
        StructField("detail_desc", StringType(), True),
        StructField("department_name", StringType(), True)
    ])
    
    df_spark = spark.createDataFrame(data_list, schema=schema)
    df_spark.createOrReplaceTempView("hm_products")
    df_spark.cache() # Lưu vào RAM để truy vấn siêu tốc
    
    return qclient, model, spark

with st.spinner("Đang nạp hệ thống: AI Model, Vector DB và Apache Spark... (Sẽ mất vài phút cho lần chạy đầu tiên)"):
    qdrant_client, embed_model, spark_session = load_systems()

collection_name = "Qdrant_Group10"

# 2. Giao diện nhập liệu
query_text = st.text_input("Nhập từ khóa tìm kiếm (Tiếng Anh):", placeholder="VD: outfit for sleeping...")

# 3. Chia đôi màn hình để so sánh
col_spark, col_qdrant = st.columns(2)

if query_text:
    # ---------------- BÊN TRÁI: SPARK SQL ----------------
    with col_spark:
        st.header("1️⃣ Truyền thống (Spark SQL)")
        st.code(f"SELECT * FROM hm_products \nWHERE LOWER(prod_name) LIKE '%{query_text.lower()}%' \nOR LOWER(detail_desc) LIKE '%{query_text.lower()}%'")
        
        # Thực thi câu lệnh SQL
        sql_query = f"""
            SELECT prod_name, department_name, detail_desc 
            FROM hm_products 
            WHERE LOWER(prod_name) LIKE '%{query_text.lower()}%' 
            OR LOWER(detail_desc) LIKE '%{query_text.lower()}%'
        """
        spark_result = spark_session.sql(sql_query)
        count = spark_result.count()
        
        if count == 0:
            st.error("❌ KẾT QUẢ: 0 SẢN PHẨM TÌM THẤY!")
            st.caption("Lý do: SQL truyền thống chỉ tìm khớp chuỗi ký tự chính xác. Không có sản phẩm nào miêu tả đúng dòng chữ này.")
        else:
            st.success(f"Tìm thấy {count} kết quả chứa từ khóa.")
            st.dataframe(spark_result.toPandas().head(3))

    # ---------------- BÊN PHẢI: QDRANT ----------------
    with col_qdrant:
        st.header("2️⃣ Hệ thống Mới (Qdrant)")
        st.code("model.encode(query) -> qdrant.query_points()")
        
        # Thêm hiệu ứng Loading cho AI và Qdrant
        with st.spinner("🧠 AI đang mã hóa Vector & Qdrant đang tính toán độ tương đồng..."):
            query_vector = embed_model.encode(query_text, normalize_embeddings=True).tolist()
            search_results = qdrant_client.query_points(
                collection_name=collection_name,
                query=query_vector,
                limit=3
            ).points
        
        if search_results:
            st.success(f"Tìm thấy top {len(search_results)} sản phẩm có độ tương đồng ngữ nghĩa cao nhất!")
            
            for i, hit in enumerate(search_results):
                # Tiêu đề của từng sản phẩm
                st.markdown(f"**Top {i+1}: {hit.payload.get('product_name', 'N/A')}** (Score: {hit.score:.4f})")
                
                # Tạo 2 cột nhỏ bên trong cột Qdrant để hiển thị ảnh bên trái, text bên phải
                col_img, col_info = st.columns([1, 2])
                
                with col_img:
                    img_url = hit.payload.get('image_url', None)
                    if img_url:
                        st.image(img_url, width="stretch")
                    else:
                        st.info("Không có hình ảnh")
                        
                with col_info:
                    st.write(f"**ID:** {hit.id}")
                    st.write(f"**Danh mục:** {hit.payload.get('department_name', 'N/A')}")
                    # Giới hạn mô tả ở 150 ký tự đầu tiên để tránh giao diện quá dài
                    desc = hit.payload.get('description', 'Không có mô tả')
                    st.write(f"> _{desc[:150]}..._")
                    
                st.divider()