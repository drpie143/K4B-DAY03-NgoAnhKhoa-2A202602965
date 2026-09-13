# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Ngô Anh Khoa  
> **Mã Sinh Viên / Mã Học viên:** 2A202602965  
> **Chủ đề Lựa chọn:** 2.3: Trợ lý Đặt Phòng họp & Thiết bị (Facilities Agent) - Kiểm tra lịch phòng trống, thiết bị và tạo booking phòng họp  

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4 / 5 | Quy trình đặt phòng đòi hỏi nhiều bước suy luận nối tiếp: tiếp nhận nhu cầu cuộc họp (số lượng người, thiết bị máy chiếu/micro) -> tra cứu phòng trống thỏa mãn -> tiến hành tạo booking và gửi xác nhận. |
| **2. Tool Interaction** | 5 / 5 | Hệ thống bắt buộc phải kết nối với MCP Server để truy vấn cơ sở dữ liệu phòng họp thời gian thực (tránh trùng lịch giữa các phòng ban) và lưu thông tin booking vào hệ thống. |
| **3. Dynamic Decision** | 5 / 5 | Quyết định bước tiếp theo phụ thuộc hoàn toàn vào Observation của bước trước: Nếu phòng được yêu cầu đã kín lịch hoặc thiếu thiết bị, tác tử phải tự động chuyển hướng tìm phòng khác hoặc đề xuất khung giờ mới. |
| **4. Long Horizon Goal** | 4 / 5 | Tác tử cần duy trì mục tiêu xuyên suốt: đảm bảo người dùng có một phòng họp phù hợp nhất với đầy đủ trang thiết bị hoạt động tốt, đồng thời xử lý các tình huống phát sinh xuyên suốt phiên hội thoại. |
| **TỔNG ĐIỂM AGENTIC FIT** | **18 / 20** | *Tổng điểm 18/20 (> 12/20): Bài toán Quản lý Phòng họp & Thiết bị rất phù hợp để triển khai kiến trúc ReAct Agent.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật (Google Gemini 2.5 Flash kết nối qua MCP Server):

```json
[
  {
    "step": 1,
    "query": "Hãy đặt phòng họp ROOM-101 vào lúc 14:00 ngày 15/09/2026 cho nhân viên Nguyễn Văn An với mục đích 'Họp rà soát tiến độ Sprint 3'.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "book_meeting_room",
    "arguments": {
      "purpose": "Họp rà soát tiến độ Sprint 3",
      "booker_name": "Nguyễn Văn An",
      "room_id": "ROOM-101",
      "datetime_str": "14:00 15/09/2026"
    },
    "observation": {
      "status": "SUCCESS",
      "booking_id": "BK-ROOM-101-2026",
      "room_id": "ROOM-101",
      "datetime": "14:00 15/09/2026",
      "booker": "Nguyễn Văn An",
      "purpose": "Họp rà soát tiến độ Sprint 3",
      "message": "Đặt phòng họp ROOM-101 thành công cho Nguyễn Văn An vào lúc 14:00 15/09/2026 (Mục đích: Họp rà soát tiến độ Sprint 3)."
    },
    "latency_ms": 2412.56
  },
  {
    "step": 2,
    "query": "Hãy đặt phòng họp ROOM-101 vào lúc 14:00 ngày 15/09/2026 cho nhân viên Nguyễn Văn An với mục đích 'Họp rà soát tiến độ Sprint 3'.",
    "action_type": "FINAL_ANSWER",
    "thought": "Tổng hợp kết quả từ MCP Server thành công.",
    "output": "Đặt phòng họp ROOM-101 thành công cho Nguyễn Văn An vào lúc 14:00 15/09/2026 (Mục đích: Họp rà soát tiến độ Sprint 3).",
    "latency_ms": 10.0
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Google Gemini 2.5 Flash).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 4 lượt (`academic_query`, `book_meeting_room`, `room_query` x 2).
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
