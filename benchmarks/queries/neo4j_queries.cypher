// UC-01: Single Insert – Đăng ký tài khoản
// CREATE (u:User {id: $id, username: $username, email: $email, full_name: $full_name, created_at: datetime()})

// UC-02: Point Read – Xem trang cá nhân
// MATCH (u:User {id: $user_id}) RETURN u

// UC-03: Read + Relationships – Bài viết + bình luận
// MATCH (p:Post {id: $post_id})
// OPTIONAL MATCH (c:Comment)-[:ON_POST]->(p)
// OPTIONAL MATCH (u:User)-[:WROTE]->(c)
// RETURN p, collect({comment: c, author: u}) AS comments

// UC-04: Aggregation – Thống kê bài viết theo Tag
// MATCH (t:Tag)<-[:TAGGED_WITH]-(p:Post)
// RETURN t.name AS tag, count(p) AS post_count
// ORDER BY post_count DESC

// UC-05: 1-hop Traversal – Danh sách đang theo dõi
// MATCH (u:User {id: $user_id})-[:FOLLOWS]->(f:User)
// RETURN f.id, f.username

// UC-06: 2-hop Traversal – Gợi ý theo dõi (FOAF)
// MATCH (u:User {id: $user_id})-[:FOLLOWS]->()-[:FOLLOWS]->(foaf:User)
// WHERE NOT (u)-[:FOLLOWS]->(foaf) AND u <> foaf
// RETURN foaf.id, foaf.username, count(*) AS mutual_count
// ORDER BY mutual_count DESC
// LIMIT 10

// UC-07: Shortest Path – Chuỗi kết nối ngắn nhất (tối đa 4-hop)
// MATCH p = shortestPath(
//   (src:User {id: $src_user_id})-[:FOLLOWS*..4]->(dst:User {id: $dst_user_id})
// )
// RETURN [n IN nodes(p) | n.id] AS path, length(p) AS hops
