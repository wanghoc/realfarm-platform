I. TỔNG QUAN KIẾN TRÚC & QUY TẮC CHUNG (GLOBAL RULES)
Yêu cầu dev frontend thiết lập bộ khung theo tiêu chuẩn Single-Page Game thay vì website truyền thống.

Layout tổng: width: 100vw; height: 100vh; overflow: hidden;. KHÔNG có thanh cuộn (scrollbar).

Base Container: Đặt position: relative để làm gốc tọa độ cho toàn bộ các UI Layer bên trong.

Tương tác chuẩn game:

Disable bôi đen văn bản: user-select: none;

Disable kéo thả ảnh gốc của trình duyệt: draggable="false"

Chặn thao tác zoom trình duyệt ngoài ý muốn trên mobile (nếu có responsive).

II. CẤU TRÚC 4 LỚP (LAYERS ARCHITECTURE)
Giao diện phân tầng theo z-index từ thấp đến cao để quản lý không gian 3 chiều.

1. Layer 1: Môi trường 2D & Đối tượng tương tác (z-index: 10)
Đây là lớp không gian mô phỏng nông trại (Viewport).

Bản đồ nền (Map Background): Đồ họa 2D góc nhìn từ trên xuống (Top-down hoặc Isometric). Hỗ trợ thao tác kéo thả chuột (Drag to pan) để di chuyển góc nhìn.

Lô Đất (Plots Grid):

Là các vùng có thể click (Clickable Zones).

Hover state: Khi rê chuột vào lô đất, hiển thị viền highlight (glow) nhẹ.

Nhãn Thông Số (Floating Labels):

Ghim cố định tọa độ vào từng Lô Đất bằng position: absolute và transform: translate.

Hiển thị: Mã lô (C-01), Trạng thái đất (Trống / Đang trồng), Icon Cảm biến (Nhiệt độ, Độ ẩm) và Thanh tiến độ (Progress bar).

Dữ liệu cập nhật real-time.

2. Layer 2: Hệ thống HUD - Heads-Up Display (z-index: 50)
Lớp giao diện cố định trên màn hình (Fixed/Absolute), không di chuyển khi kéo bản đồ.

Top-Left (Player Info): Cụm thẻ bo góc bo tròn, nền bán trong suốt chứa Avatar người chơi, Tên nông trại, Số dư Tiền Vàng (hiệu ứng số nhảy khi được cộng/trừ tiền).

Top-Right (System Controls):

Minimap (Bản đồ thu nhỏ): Hình vuông/tròn bo góc, hiển thị vị trí hiện tại của Camera trên tổng thể nông trại.

Các nút công cụ nhỏ: Cài đặt (Settings), Toàn màn hình (Fullscreen).

Bottom-Right (Action Skills HUD): Cụm điều khiển hành động chính.

Thiết kế dạng nút tròn to (giống nút chưởng trong Genshin/Mobile Legends).

Gồm các nút: [💧 Tưới Nước], [💊 Bón Phân].

Behavior (Rất quan trọng):

Default: Nút bị mờ (opacity 0.5, grayscale), click không có tác dụng.

Active: Chỉ khi người chơi Click chọn 1 Lô Đất ở Layer 1, cụm nút mới sáng màu lên (opacity 1.0), có viền sáng, sẵn sàng tương tác.

3. Layer 3: NPC & Hệ thống Cảnh báo (z-index: 70)
Vị trí: Cố định ở góc Dưới - Trái (Bottom-Left).

Hình ảnh NPC (Half-body): Chỉ hiển thị từ bụng trở lên, có animation trượt từ mép trái màn hình vào (slide-in-left) khi xuất hiện.

Hộp thoại (Dialog Box):

Style: Áp dụng Glassmorphism. Trắng bán trong suốt (background: rgba(255,255,255,0.7) hoặc tối tương tự tùy nền), viền mờ, blur nền đằng sau: backdrop-filter: blur(12px).

Nội dung: Text chạy từng chữ (Typewriter effect) hoặc hiện ra ngay lập tức. Dùng để báo cáo tình trạng IoT (VD: "Đất đang khô, cần tưới!").

Có nút ▼ nhấp nháy để người chơi click đọc câu thoại tiếp theo hoặc tắt hộp thoại.

4. Layer 4: Modals, Popups & Overlays (z-index: 100)
Lớp cao nhất để gián đoạn trải nghiệm, ép người chơi focus vào một thao tác.

Background Overlay: Phủ đen toàn màn hình, opacity: 0.6, click ra ngoài để đóng (hoặc tùy cấu hình).

Popup Luồng Thuê Đất (Lease Flow):

Modal bảng gỗ ở chính giữa.

Chứa danh sách (Grid/List) các loại hạt giống có thể trồng.

Nút Call-to-action to, rõ ràng: [Ký Hợp Đồng].

Popup Live Camera:

Chia đôi màn hình hoặc mở Modal lớn: 1 bên là số liệu mô phỏng (Digital Twin), 1 bên là khung hình iFrame/Video stream từ camera thực tế tại vườn để đối chiếu.

III. ANIMATION & TƯƠNG TÁC (INTERACTION STATES)
Tích hợp cơ chế phản hồi theo 5 trạng thái vòng đời của 1 hành động theo AGENTS.md:

Khi user bấm nút Tưới (Accepted): Nút hiển thị loader vòng tròn chờ xử lý.

Bị từ chối (Rejected): Nút rung lên (Shake animation), text hiển thị màu đỏ báo lỗi.

Hoàn thành (Completed): Hiển thị icon dấu tick xanh, popup chữ "Thành công" bay lên khỏi nút (Floating text animation).

Các transition cơ bản nên đặt transition: all 0.2s ease-in-out để cảm giác bấm nút mượt mà, không bị giật cứng.