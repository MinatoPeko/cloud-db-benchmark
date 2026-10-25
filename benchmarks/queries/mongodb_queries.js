// UC-01: Single Insert – Đăng ký tài khoản
// db.users.insertOne({_id: <id>, username: <username>, email: <email>, full_name: <full_name>, created_at: new Date()})

// UC-02: Point Read – Xem trang cá nhân
// db.users.findOne({_id: <user_id>})

// UC-03: Read – Đọc bài viết + embedded comments (1 truy vấn duy nhất nhờ document model)
// db.posts.findOne({_id: <post_id>})

// UC-04: Aggregation – Thống kê bài viết theo Tag
[
  { "$unwind": "$tags" },
  { "$group": { "_id": "$tags", "post_count": { "$sum": 1 } } },
  { "$sort": { "post_count": -1 } },
  { "$project": { "_id": 0, "tag": "$_id", "post_count": 1 } }
]

// UC-05: 1-hop – Danh sách đang theo dõi
// db.follows.find({follower_id: <user_id>}, {followee_id: 1, _id: 0})

// UC-06: 2-hop – Gợi ý theo dõi (FOAF via $graphLookup)
[
  { "$match": { "follower_id": "<user_id>" } },
  {
    "$graphLookup": {
      "from": "follows",
      "startWith": "$followee_id",
      "connectFromField": "followee_id",
      "connectToField": "follower_id",
      "as": "foaf",
      "maxDepth": 1,
      "restrictSearchWithMatch": {}
    }
  },
  { "$unwind": "$foaf" },
  { "$group": { "_id": "$foaf.followee_id", "mutual_count": { "$sum": 1 } } },
  { "$sort": { "mutual_count": -1 } },
  { "$limit": 10 }
]

// UC-07: Deep Traversal – Chuỗi kết nối ($graphLookup maxDepth 3 = 4-hop)
[
  { "$match": { "follower_id": "<src_user_id>" } },
  {
    "$graphLookup": {
      "from": "follows",
      "startWith": "$followee_id",
      "connectFromField": "followee_id",
      "connectToField": "follower_id",
      "as": "path",
      "maxDepth": 3,
      "depthField": "depth"
    }
  },
  { "$unwind": "$path" },
  { "$match": { "path.followee_id": "<dst_user_id>" } },
  { "$sort": { "path.depth": 1 } },
  { "$limit": 1 }
]
