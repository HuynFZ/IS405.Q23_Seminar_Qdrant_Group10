import streamlit as st
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Cấu hình giao diện trang web
st.set_page_config(page_title="H&M Semantic Search", page_icon="🔍", layout="wide")

st.title("🛍️ H&M E-commerce: Semantic Search Demo")
st.markdown("Hệ thống tìm kiếm thông minh dựa trên Vector Database (Qdrant) và Sentence Transformers.")

# 1. Khởi tạo và Cache Model AI & Qdrant Client để tối ưu tốc độ
@st.cache_resource
def load_systems():
    # Kết nối Qdrant [cite: 85]
    qclient = QdrantClient(url="http://localhost:6333") 
    
    # Tải mô hình AI chuyển đổi văn bản thành vector [cite: 88, 90]
    model = SentenceTransformer('BAAI/bge-small-en-v1.5') 
    return qclient, model

with st.spinner("Đang khởi tạo hệ thống và tải mô hình AI..."):
    qdrant_client, embed_model = load_systems()

collection_name = "Qdrant_Group10" # [cite: 86]

# 2. Tạo Form tìm kiếm
with st.form("search_form"):
    query_text = st.text_input("Nhập mô tả sản phẩm bạn muốn tìm kiếm (Tiếng Anh):", 
                               placeholder="VD: A warm winter coat for extreme cold weather...") # [cite: 61]
    
    # Cho phép người dùng tuỳ chỉnh số lượng kết quả
    top_k = st.slider("Số lượng kết quả trả về:", min_value=1, max_value=10, value=3)
    
    submitted = st.form_submit_button("🔍 Tìm kiếm Sản phẩm")

# 3. Xử lý logic tìm kiếm khi bấm nút
if submitted and query_text:
    with st.spinner("Đang trích xuất Vector và tìm kiếm trong Qdrant..."):
        # Chuyển đổi câu truy vấn thành Vector 384 chiều [cite: 59, 127]
        query_vector = embed_model.encode(query_text, normalize_embeddings=True).tolist() # [cite: 128]
        
        # Truy vấn vào Qdrant
        search_results = qdrant_client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=top_k
        ).points # [cite: 129, 130, 131, 132]
        
        # 4. Hiển thị kết quả
        if search_results:
            st.success(f"Tìm thấy {len(search_results)} sản phẩm phù hợp nhất với mô tả!")
            
            # Hiển thị dưới dạng thẻ (cards) sử dụng columns của Streamlit
            for i, hit in enumerate(search_results):
                with st.container():
                    st.markdown(f"### Top {i+1}: {hit.payload.get('product_name', 'N/A')} (Score: {hit.score:.4f})") # [cite: 134, 136]
                    
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        # Nếu ETL của bạn có trường image_url[cite: 15], Streamlit có thể hiển thị ảnh trực tiếp
                        img_url = hit.payload.get('image_url', None)
                        if img_url:
                            st.image(img_url, use_container_width=True)
                        else:
                            st.info("Không có hình ảnh")
                            
                    with col2:
                        st.write(f"**Mã SP (ID):** {hit.id}") # [cite: 135]
                        st.write(f"**Danh mục:** {hit.payload.get('department_name', 'N/A')}") # [cite: 137]
                        st.write(f"**Mô tả chi tiết:**")
                        st.write(f"> {hit.payload.get('description', 'Không có mô tả')}") # [cite: 13, 140]
                    st.divider()
        else:
            st.warning("Không tìm thấy sản phẩm nào.")