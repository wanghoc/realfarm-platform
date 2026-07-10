# Tóm tắt dự án RealFarm

## Bài toán

Nhiều khách hàng muốn trải nghiệm trồng rau/cây nhưng không có đất, không có thời gian hoặc không đủ kiến thức để tự chăm sóc hằng ngày.

RealFarm cho phép khách hàng:

1. thuê một lô đất thật từ hệ thống;
2. chọn cây trồng trong danh mục được hỗ trợ;
3. theo dõi lô bằng giao diện nông trại 2D;
4. gửi một số yêu cầu chăm sóc;
5. xem dữ liệu, hình ảnh và bằng chứng thực hiện;
6. nhận toàn bộ nông sản hợp lệ của chu kỳ trồng thuộc lô đã thuê.

## Bản chất sản phẩm

Đây là dịch vụ canh tác có quản lý, được game hóa để tăng hứng thú. Người chơi không điều khiển cây và thiết bị một cách tuyệt đối.

Mỗi thao tác của người chơi đi qua quy trình:

```text
Người chơi gửi yêu cầu
→ Hệ thống kiểm tra an toàn và quy tắc canh tác
→ Tự động thực hiện hoặc tạo công việc cho nông dân
→ Ghi nhận kết quả và bằng chứng
→ Cập nhật lên giao diện nông trại
```

## MVP đề xuất

- Đăng ký/đăng nhập.
- Xem và thuê lô.
- Chọn cây trồng.
- Quản lý chu kỳ trồng.
- Digital Twin 2D bằng Phaser.
- Dữ liệu IoT cơ bản và bộ mô phỏng.
- Tưới tự động có giới hạn an toàn.
- Yêu cầu thao tác từ người chơi.
- Hàng đợi công việc cho nông dân.
- Ảnh bằng chứng và nhật ký chăm sóc.
- Ghi nhận thu hoạch.
- Xác định quyền sở hữu nông sản.
- Nhận tại vườn hoặc tạo yêu cầu giao hàng cơ bản.
- Truy xuất bằng QR ở mức cơ bản.

## Không thuộc MVP

- Game thế giới mở.
- Điều khiển thiết bị không giới hạn.
- Nhiều loại cây và nhiều trang trại.
- Thanh toán thật.
- Ứng dụng mobile native.
- Blockchain đa tổ chức.
- Ước lượng năng suất AI phức tạp.
- Phân loại nông sản tự động quy mô sản xuất.

## Thay đổi lớn so với đề xuất ban đầu

- Từ hệ thống quản lý nhà kính cho nhà vườn sang nền tảng B2C cho người thuê lô.
- Người tiêu dùng quét QR được thay bằng Người chơi/Khách hàng là tác nhân trung tâm.
- Bổ sung Nông dân/Nhân viên vận hành.
- Bổ sung thuê lô, gói dịch vụ, yêu cầu thao tác, work order, bằng chứng, quyền thu hoạch và giao nhận.
- Lệnh của người chơi không còn có ưu tiên cao nhất; an toàn và quy tắc canh tác được ưu tiên.
- Backend ưu tiên modular monolith thay vì tách nhiều microservice.
- Blockchain chuyển thành phần mở rộng, không chặn MVP.
- Web responsive/PWA được ưu tiên trước mobile native.
