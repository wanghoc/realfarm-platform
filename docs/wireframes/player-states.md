# Thiết kế Wireframe: Player States & Digital Twin

**Task:** Bố cục UI thống nhất cho Dashboard và Luồng hành động của người chơi.
**Branch:** feat/1-wireframe-player-states

## 1. Ghi chú & Thắc mắc từ Docs
* Thiết kế tuân thủ nghiêm ngặt MVP, loại bỏ các giao diện điều khiển phần cứng trực tiếp, tập trung vào luồng "Gửi yêu cầu - Chờ hệ thống xử lý".
* Giao diện đã chốt phong cách Casual Farming Game với NPC thông báo. 

## 2. Luồng Thuê Đất (Lease Flow)
* **Danh sách lô canh tác (Grid View):** Phân biệt rõ UI của lô đất "Đã được thuê" (hiển thị cây trồng, data) và "Chưa thuê" (đất trống).
* **Popup Ký Hợp Đồng:** Khi bấm thuê tại lô đất trống, một Modal sẽ hiện ra cho phép người chơi xem thông tin vị trí, chọn giống cây trồng (Cà chua, Ớt chuông...) và xác nhận chi phí (Tiền vàng).
* **Xác nhận:** Sau khi bấm "Ký xác nhận", lô đất cập nhật thành "Đã được thuê" và bắt đầu thu thập dữ liệu IoT.

## 3. Luồng Trạng Thái Hành Động (Action States)
Thiết kế đã bao gồm sơ đồ luồng (flowchart) và UI phản hồi đầy đủ 5 trạng thái vòng đời của một action:
* **Accepted**: Yêu cầu hợp lệ, hệ thống vừa ghi nhận (Giao diện hiển thị trạng thái chờ/loading).
* **Scheduled**: Đã đưa vào lịch trình chờ xử lý.
* **Rejected**: Yêu cầu bị từ chối do vi phạm điều kiện, ví dụ: "Đất đang đủ ẩm" (Giao diện hiển thị cảnh báo đỏ kèm text giải thích từ NPC).
* **Expired**: Yêu cầu quá hạn do không thể thực thi.
* **Completed**: Thao tác đã thực hiện xong thành công.

**Link Figma:** https://www.figma.com/design/AOWdKr5204eYP9CUplYfTl/Untitled?node-id=9-74&t=0weTeIlPrghBwGvC-1
