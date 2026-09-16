// ============================================================================
// ĐỒ ÁN CHUYÊN NGÀNH KỸ THUẬT PHẦN MỀM - ĐẠI HỌC PHENIKAA
// Schema & Index Initialization Script cho MongoDB 7.0 (Document Model)
// Vị trí: data/schemas/mongodb_schema.js
// ============================================================================

const dbName = "social_benchmark";
const benchmarkDb = db.getSiblingDB(dbName);

// 1. Dọn dẹp dữ liệu cũ
benchmarkDb.users.drop();
benchmarkDb.follows.drop();
benchmarkDb.posts.drop();

// 2. Khởi tạo Collection 'users' với JSON Schema Validation
benchmarkDb.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["_id", "username", "email", "full_name", "created_at"],
      properties: {
        _id: { bsonType: ["long", "int", "double"], description: "ID định danh người dùng (Unique)" },
        username: { bsonType: "string", description: "Tên đăng nhập duy nhất" },
        email: { bsonType: "string", description: "Địa chỉ email hợp lệ" },
        full_name: { bsonType: "string", description: "Họ và tên hiển thị" },
        created_at: { bsonType: "date", description: "Thời điểm tạo tài khoản" }
      }
    }
  }
});

// 3. Khởi tạo Collection 'follows' (Quan hệ theo dõi có hướng)
benchmarkDb.createCollection("follows", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["follower_id", "followee_id", "created_at"],
      properties: {
        follower_id: { bsonType: ["long", "int", "double"], description: "ID người theo dõi" },
        followee_id: { bsonType: ["long", "int", "double"], description: "ID người được theo dõi" },
        created_at: { bsonType: "date", description: "Thời điểm thực hiện theo dõi" }
      }
    }
  }
});

// 4. Khởi tạo Collection 'posts' (Đặc trưng Document: Nhúng Comments và mảng Tags)
benchmarkDb.createCollection("posts", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["_id", "user_id", "content", "created_at"],
      properties: {
        _id: { bsonType: ["long", "int", "double"], description: "ID định danh bài viết" },
        user_id: { bsonType: ["long", "int", "double"], description: "ID người đăng bài" },
        content: { bsonType: "string", description: "Nội dung bài viết" },
        likes_count: { bsonType: "int", description: "Số lượt thích bài viết" },
        tags: {
          bsonType: "array",
          items: { bsonType: "string" },
          description: "Mảng danh sách các thẻ chủ đề (Tags)"
        },
        comments: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: ["comment_id", "user_id", "content", "created_at"],
            properties: {
              comment_id: { bsonType: ["long", "int", "double"] },
              user_id: { bsonType: ["long", "int", "double"] },
              content: { bsonType: "string" },
              created_at: { bsonType: "date" }
            }
          },
          description: "Mảng bình luận được nhúng trực tiếp (Embedded Comments)"
        },
        created_at: { bsonType: "date", description: "Thời điểm đăng bài" }
      }
    }
  }
});

// ============================================================================
// THIẾT KẾ CHỈ MỤC MONGODB (INDEXING STRATEGY)
// ============================================================================

// Chỉ mục duy nhất cho users
benchmarkDb.users.createIndex({ username: 1 }, { unique: true, name: "idx_users_username" });
benchmarkDb.users.createIndex({ email: 1 }, { unique: true, name: "idx_users_email" });

// Chỉ mục phục vụ truy vấn quan hệ Follows và đồ thị $graphLookup
benchmarkDb.follows.createIndex({ follower_id: 1, followee_id: 1 }, { unique: true, name: "idx_follows_compound" });
benchmarkDb.follows.createIndex({ followee_id: 1 }, { name: "idx_follows_followee" });

// Chỉ mục tối ưu tìm bài viết theo tác giả và sắp xếp thời gian
benchmarkDb.posts.createIndex({ user_id: 1, created_at: -1 }, { name: "idx_posts_user_created" });

// Multikey Index cho mảng tags (Tối ưu tuyệt đối cho truy vấn tổng hợp theo tag)
benchmarkDb.posts.createIndex({ tags: 1 }, { name: "idx_posts_tags_multikey" });

// Chỉ mục tìm kiếm bình luận theo người viết trong tài liệu nhúng
benchmarkDb.posts.createIndex({ "comments.user_id": 1 }, { name: "idx_posts_comments_user" });

print("✅ Đã khởi tạo thành công Schemas và Indexes cho MongoDB!");
