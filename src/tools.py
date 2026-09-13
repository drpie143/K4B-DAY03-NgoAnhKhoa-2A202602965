"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Đã được định nghĩa mẫu sẵn cho Học viên tham khảo
    {
        "name": "academic_query",
        "description": "Tra cứu hồ sơ và thông tin học vụ của sinh viên VinUni bằng mã sinh viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần tra cứu (ví dụ: 'SV2026001')"
                }
            },
            "required": ["student_id"]
        }
    },
    
    # --------------------------------------------------------------------------
    # TODO 1.2: HỌC VIÊN HOÀN THIỆN TOOL SCHEMA CHO 'schedule_appointment'
    # 🎯 YÊU CẦU THIẾT KẾ SCHEMA (JSON SCHEMA STANDARD):
    # 1. Tool dùng để đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.
    # 2. Thiết kế các tham số (properties) để LLM trích xuất:
    #    - student_id (string): Mã sinh viên cần đặt lịch (ví dụ: 'SV2026001')
    #    - datetime_str (string): Thời gian hẹn (ví dụ: '14:00 15/09/2026')
    #    - advisor_name (string): Tên cố vấn học tập
    # 3. Khai báo danh sách các trường bắt buộc (required).
    # --------------------------------------------------------------------------
    {
        "name": "schedule_appointment",
        "description": "Đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần đặt lịch (ví dụ: 'SV2026001')"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian hẹn tư vấn (ví dụ: '14:00 15/09/2026')"
                },
                "advisor_name": {
                    "type": "string",
                    "description": "Tên cố vấn học tập phụ trách (ví dụ: 'PGS.TS Nguyễn Văn A')"
                }
            },
            "required": ["student_id", "datetime_str", "advisor_name"]
        }
    },

    # Tool 3: Hỗ trợ Chủ đề 2.3 Facilities Agent - Tra cứu phòng họp & thiết bị
    {
        "name": "room_query",
        "description": "Tra cứu thông tin phòng họp, sức chứa, trạng thái phòng và danh sách trang thiết bị đi kèm (máy chiếu, micro, bảng viết) bằng mã phòng.",
        "parameters": {
            "type": "object",
            "properties": {
                "room_id": {
                    "type": "string",
                    "description": "Mã định danh phòng họp cần tra cứu (ví dụ: 'ROOM-101', 'ROOM-102')"
                }
            },
            "required": ["room_id"]
        }
    },

    # Tool 4: Hỗ trợ Chủ đề 2.3 Facilities Agent - Đặt lịch phòng họp & mượn thiết bị
    {
        "name": "book_meeting_room",
        "description": "Tạo booking đặt phòng họp và đăng ký sử dụng trang thiết bị phòng họp cho nhân viên / sinh viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "room_id": {
                    "type": "string",
                    "description": "Mã phòng họp cần đặt (ví dụ: 'ROOM-101')"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian diễn ra cuộc họp (ví dụ: '14:00 15/09/2026')"
                },
                "booker_name": {
                    "type": "string",
                    "description": "Họ và tên người đặt phòng họp (ví dụ: 'Nguyễn Văn An')"
                },
                "purpose": {
                    "type": "string",
                    "description": "Mục đích cuộc họp hoặc nội dung sử dụng phòng (ví dụ: 'Họp rà soát tiến độ Sprint 3')"
                }
            },
            "required": ["room_id", "datetime_str", "booker_name"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "SV2026001": {
        "full_name": "Nguyễn Văn An",
        "class": "AI-K4",
        "gpa": 3.85,
        "email": "an.nv@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "PGS.TS Nguyễn Văn A"
    },
    "SV2026002": {
        "full_name": "Trần Thị Bình",
        "class": "AI-K4",
        "gpa": 3.60,
        "email": "binh.tt@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "TS. Lê Thị B"
    }
}

# Dữ liệu phòng họp & trang thiết bị (Phục vụ Facilities Agent)
MOCK_ROOMS = {
    "ROOM-101": {
        "room_name": "Phòng họp Sáng tạo 101",
        "capacity": 12,
        "equipment": ["Máy chiếu Full HD", "Bảng trắng từ tính", "Wifi tốc độ cao"],
        "status": "Sẵn sàng",
        "location": "Tầng 1 - Tòa nhà A"
    },
    "ROOM-102": {
        "room_name": "Hội trường Hội thảo 102",
        "capacity": 30,
        "equipment": ["Máy chiếu 4K Laser", "2 Micro không dây", "Hệ thống loa hội nghị", "Bảng thông minh tương tác"],
        "status": "Sẵn sàng",
        "location": "Tầng 1 - Tòa nhà B"
    }
}


def execute_academic_query(student_id: str) -> str:
    """Thực thi tra cứu học vụ theo mã sinh viên"""
    student = MOCK_DATABASE.get(student_id.strip().upper())
    if student:
        return json.dumps({
            "status": "SUCCESS",
            "student_id": student_id,
            "data": student
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu sinh viên có mã '{student_id}'"
        }, ensure_ascii=False)


def execute_schedule_appointment(student_id: str, datetime_str: str, advisor_name: str = "PGS.TS Nguyễn Văn A") -> str:
    """Thực thi đặt lịch hẹn tư vấn học vụ"""
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"BK-{student_id}-99",
        "student_id": student_id,
        "datetime": datetime_str,
        "advisor": advisor_name,
        "message": f"Đặt lịch thành công cho sinh viên {student_id} với {advisor_name} vào lúc {datetime_str}."
    }, ensure_ascii=False)


def execute_room_query(room_id: str) -> str:
    """Thực thi tra cứu tình trạng phòng họp và danh sách thiết bị"""
    room = MOCK_ROOMS.get(room_id.strip().upper())
    if room:
        return json.dumps({
            "status": "SUCCESS",
            "room_id": room_id,
            "data": room
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy thông tin phòng họp có mã '{room_id}' trong hệ thống tòa nhà."
        }, ensure_ascii=False)


def execute_book_meeting_room(room_id: str, datetime_str: str, booker_name: str, purpose: str = "Họp công việc") -> str:
    """Thực thi đặt phòng họp và mượn thiết bị"""
    room_key = room_id.strip().upper()
    if room_key not in MOCK_ROOMS:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không thể đặt phòng do mã phòng '{room_id}' không tồn tại trong hệ thống."
        }, ensure_ascii=False)
        
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"BK-{room_key}-2026",
        "room_id": room_key,
        "datetime": datetime_str,
        "booker": booker_name,
        "purpose": purpose,
        "message": f"Đặt phòng họp {room_key} thành công cho {booker_name} vào lúc {datetime_str} (Mục đích: {purpose})."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "academic_query": execute_academic_query,
    "schedule_appointment": execute_schedule_appointment,
    "room_query": execute_room_query,
    "book_meeting_room": execute_book_meeting_room
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
