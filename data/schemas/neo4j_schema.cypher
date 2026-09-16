// ============================================================================
// ĐỒ ÁN CHUYÊN NGÀNH KỸ THUẬT PHẦN MỀM - ĐẠI HỌC PHENIKAA
// Schema Constraints & Indexes Initialization Script cho Neo4j 5.x (Property Graph Model)
// Vị trí: data/schemas/neo4j_schema.cypher
// ============================================================================

// 1. RÀNG BUỘC TOÀN VẸN VÀ TÍNH DUY NHẤT (UNIQUENESS CONSTRAINTS)
// Lưu ý: Trong Neo4j, việc tạo Constraint tự động kích hoạt tạo B-Tree Index cho thuộc tính đó

// Ràng buộc duy nhất cho định danh và tên đăng nhập User
CREATE CONSTRAINT c_user_id IF NOT EXISTS 
FOR (u:User) REQUIRE u.id IS UNIQUE;

CREATE CONSTRAINT c_user_username IF NOT EXISTS 
FOR (u:User) REQUIRE u.username IS UNIQUE;

// Ràng buộc duy nhất cho ID bài viết
CREATE CONSTRAINT c_post_id IF NOT EXISTS 
FOR (p:Post) REQUIRE p.id IS UNIQUE;

// Ràng buộc duy nhất cho ID bình luận
CREATE CONSTRAINT c_comment_id IF NOT EXISTS 
FOR (c:Comment) REQUIRE c.id IS UNIQUE;

// Ràng buộc duy nhất cho tên thẻ Tag
CREATE CONSTRAINT c_tag_name IF NOT EXISTS 
FOR (t:Tag) REQUIRE t.name IS UNIQUE;

// ============================================================================
// 2. CHỈ MỤC TÌM KIẾM BỔ SỢ (SCHEMA INDEXES)
// ============================================================================

// Chỉ mục tìm kiếm theo họ tên hiển thị người dùng
CREATE INDEX idx_user_full_name IF NOT EXISTS 
FOR (u:User) ON (u.full_name);

// Chỉ mục sắp xếp bài viết theo thời gian tạo
CREATE INDEX idx_post_created_at IF NOT EXISTS 
FOR (p:Post) ON (p.created_at);

// ============================================================================
// 3. ĐẶC TẢ CẤU TRÚC ĐỈNH VÀ CẠNH (REFERENCE PATTERNS)
// ============================================================================
// Nodes (Đỉnh):
//   (:User {id: Long, username: String, email: String, full_name: String, created_at: DateTime})
//   (:Post {id: Long, content: String, likes_count: Integer, created_at: DateTime})
//   (:Comment {id: Long, content: String, created_at: DateTime})
//   (:Tag {name: String})
//
// Relationships (Cạnh liên kết - Index-Free Adjacency):
//   (:User)-[:FOLLOWS {created_at: DateTime}]->(:User)
//   (:User)-[:AUTHORED]->(:Post)
//   (:User)-[:WROTE]->(:Comment)
//   (:Comment)-[:ON_POST]->(:Post)
//   (:Post)-[:TAGGED_WITH]->(:Tag)
