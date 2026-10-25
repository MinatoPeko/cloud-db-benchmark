-- UC-01: Single Insert – Đăng ký tài khoản
INSERT INTO users (id, username, email, full_name, created_at)
VALUES (:id, :username, :email, :full_name, NOW())
ON CONFLICT DO NOTHING;

-- UC-02: Point Read – Xem trang cá nhân
SELECT id, username, email, full_name, created_at
FROM users
WHERE id = :user_id;

-- UC-03: Read with Join – Đọc bài viết + bình luận
SELECT p.id, p.content, p.likes_count, p.created_at,
       c.id AS comment_id, c.user_id AS commenter_id, c.content AS comment_content
FROM posts p
LEFT JOIN comments c ON c.post_id = p.id
WHERE p.id = :post_id;

-- UC-04: Aggregation – Thống kê bài viết theo Tag
SELECT t.name, COUNT(pt.post_id) AS post_count
FROM tags t
JOIN post_tags pt ON pt.tag_id = t.id
GROUP BY t.name
ORDER BY post_count DESC;

-- UC-05: 1-hop Traversal – Danh sách đang theo dõi
SELECT followee_id
FROM follows
WHERE follower_id = :user_id;

-- UC-06: 2-hop Traversal – Gợi ý theo dõi (FOAF)
SELECT f2.followee_id, COUNT(*) AS mutual_count
FROM follows f1
JOIN follows f2 ON f2.follower_id = f1.followee_id
WHERE f1.follower_id = :user_id
  AND f2.followee_id <> :user_id
  AND f2.followee_id NOT IN (
      SELECT followee_id FROM follows WHERE follower_id = :user_id
  )
GROUP BY f2.followee_id
ORDER BY mutual_count DESC
LIMIT 10;

-- UC-07: Deep Traversal – Đường đi ngắn nhất (BFS đệ quy, tối đa 4-hop)
WITH RECURSIVE path_cte AS (
    SELECT follower_id, followee_id, 1 AS depth,
           ARRAY[follower_id] AS visited
    FROM follows
    WHERE follower_id = :src_user_id
    UNION ALL
    SELECT p.follower_id, f.followee_id, p.depth + 1,
           p.visited || f.followee_id
    FROM path_cte p
    JOIN follows f ON f.follower_id = p.followee_id
    WHERE p.depth < 4
      AND NOT (f.followee_id = ANY(p.visited))
)
SELECT visited || ARRAY[followee_id] AS path, depth
FROM path_cte
WHERE followee_id = :dst_user_id
ORDER BY depth
LIMIT 1;
