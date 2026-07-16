## Summary
Thêm bản vẽ wireframe cho màn hình Digital Twin và luồng trạng thái hành động (Action States) theo định hướng Casual Farming Game.

## Related task
Closes #1

## Changes
- Thêm tài liệu thiết kế: `docs/wireframes/player-states.md`.
- Thiết kế layout Plot Card: Kết hợp mô phỏng 2D, thông số cảm biến thật và camera.
- Vẽ luồng phản hồi hành động:Yêu cầu(request) Đang xử lý (Submitted), Từ chối (Rejected),đang xử lý(Progress), Hoàn thành (Completed).

## Business rules affected
- Tuân thủ quy tắc: Không giả định hành động thành công khi chưa có phản hồi từ backend. Mọi thao tác đều phải đi qua trạng thái chờ hoặc bị từ chối kèm lý do.


## Screenshots or evidence
**Figma:** https://www.figma.com/design/AOWdKr5204eYP9CUplYfTl/Untitled?node-id=2-2&t=ZOYjX9rmfq704seF-1

## Migrations / environment changes
None. 
## Risks and follow-up
None