# Danh sách Keyword Demo & Kịch bản Benchmarking
**Đề tài:** Xây dựng hệ thống tìm kiếm sản phẩm thương mại điện tử thông minh (H&M Dataset)

Tài liệu này tổng hợp các bộ từ khóa (Query) dùng để demo sự khác biệt giữa tìm kiếm truyền thống (Spark SQL) và tìm kiếm ngữ nghĩa (Qdrant Vector Search).

---

## 1. Thông tin hệ thống tham chiếu
* **Dataset:** H&M Ecommerce Products (~106.000 dòng)[cite: 5, 8].
* **Model AI:** BAAI/bge-small-en-v1.5 (Vector 384 chiều)[cite: 14, 40].
* **Công nghệ so sánh:** Spark SQL (Keyword-based) vs. Qdrant (Semantic-based)[cite: 44, 63].

---

## 2. Các bộ Keyword Demo đề xuất

### Nhóm A: Từ đồng nghĩa & Từ lóng (Synonyms & Slang)
*Mục tiêu: Chứng minh AI hiểu các cách gọi khác nhau của cùng một loại sản phẩm.*

| STT | Truy vấn (Query) | Kết quả mong đợi (Qdrant) | Giải thích cho Demo |
|:---:|:---|:---|:---|
| 1 | `shades to protect eyes from the sun` | Sunglasses / Eyewear | Người dùng không gõ "glass", AI vẫn hiểu mục đích bảo vệ mắt là dùng kính râm. |
| 2 | `pullover with a hood` | Hoodie / Sweatshirt | Hiểu "pullover with a hood" chính là định nghĩa của áo Hoodie. |
| 3 | `denim bottoms` | Jeans / Denim shorts | Hiểu "bottoms" là đồ mặc phía dưới (quần) làm từ vải denim. |

### Nhóm B: Ngữ cảnh & Sự kiện (Occasion & Event)
*Mục tiêu: Chứng minh AI có "kiến thức nền" về phong cách ăn mặc theo hoàn cảnh.*

| STT | Truy vấn (Query) | Kết quả mong đợi (Qdrant) | Giải thích cho Demo |
|:---:|:---|:---|:---|
| 1 | `outfit for sleeping` | Pyjamas / Sleep bag / Nightwear | Chứng minh thực tế: Trả về đồ ngủ dù tên SP không chứa chữ "outfit". |
| 2 | `attire for a formal business meeting` | Blazer / Suit / Oxford shirt | AI hiểu môi trường công sở cần các loại áo vest, sơ mi trang trọng. |
| 3 | `clothes for a summer beach party` | Swimwear / Linen shirt / Shorts | Tự động gợi ý các sản phẩm phù hợp với mùa hè và đi biển. |

### Nhóm C: Tính năng & Cảm giác (Functionality & Vibe)
*Mục tiêu: Chứng minh khả năng quét sâu vào mô tả sản phẩm (Detail Description).*

| STT | Truy vấn (Query) | Kết quả mong đợi (Qdrant) | Giải thích cho Demo |
|:---:|:---|:---|:---|
| 1 | `waterproof layer for a rainy day` | Raincoat / Shell jacket | Tìm các SP có thuộc tính "water-repellent" hoặc "windproof"[cite: 27]. |
| 2 | `breathable fabric for heavy sweating` | Sports T-shirt / Running top | Tìm các SP có mô tả "fast-drying", "functional fabric"[cite: 34]. |
| 3 | `stretchy bottoms for yoga class` | Leggings / Tights | Tìm kiếm dựa trên đặc tính co giãn của chất liệu vải. |

---
