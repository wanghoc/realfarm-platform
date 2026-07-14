# Kế hoạch chi tiết 16 tuần — RealFarm

> Tài liệu tiếng Việt dành riêng cho nhóm (theo `AGENTS.md` mục 5: business explanation có thể viết tiếng Việt). Đây là bản chia nhỏ theo từng ngày của [`10_ROADMAP_16_WEEKS.md`](10_ROADMAP_16_WEEKS.md), gắn với phân công trong `team_roles` (memory) và các quy tắc trong `AGENTS.md`, `02_BUSINESS_RULES.md`, `03_ARCHITECTURE.md`.

## Quy ước

- **Thái** — Frontend/Game (`apps/web`, React + Phaser).
- **Học** — Backend Core: Commerce & Lifecycle (`auth, users, farms, plots, leases, crop_catalog, crop_cycles, harvests, deliveries`).
- **Khoa** — Backend Realtime: Policy & IoT (`telemetry, automation, player_actions, work_orders, care_logs, incidents` + `apps/gateway`, `apps/simulator`, `apps/firmware`).
- **Bảo** — AI + Infra/DevOps (`apps/ai-service`, Docker, DB, CI, `packages/contracts/schemas`).
- Thứ 7 mỗi tuần dùng để demo/tổng kết nội bộ. Chủ nhật là buffer (dự phòng lỗi phát sinh, không giao task mới).
- Khi một người "hỗ trợ", nghĩa là việc chính do người kia chủ trì, người hỗ trợ tham gia review/pair, không double-work.

---

## Tuần 1 — Chốt miền nghiệp vụ (phần 1)

**Mục tiêu:** Cả nhóm hiểu và thống nhất domain rules trước khi code.
**Deliverable:** Bản nháp domain rules được review chéo.

| Ngày | Thái | Học | Khoa | Bảo |
|---|---|---|---|---|
| Thứ 2 | Đọc `AGENTS.md`, `docs/00-04` cùng cả nhóm, ghi chú thắc mắc | (như Thái) | (như Thái) | (như Thái) |
| Thứ 3 | Vẽ wireframe UI: danh sách plot, luồng thuê lease, mockup digital twin | Soạn chi tiết state machine Lease + CropCycle | Soạn action catalog: danh sách player action request và kết quả policy mong đợi | Khảo sát AI candidate (disease detection), review `packages/contracts/schemas` |
| Thứ 4 | Review chéo bản nháp của Học/Khoa | Review chéo wireframe của Thái | Review chéo state machine của Học | Review chéo action catalog của Khoa |
| Thứ 5 | Hoàn thiện wireframe + luồng trạng thái (accepted/scheduled/rejected/expired/completed) | Định nghĩa ServicePackage + harvest policy | Thiết kế operator workflow (vòng đời work order) | Lên kế hoạch nguồn dữ liệu ảnh bệnh lá (PlantVillage) |
| Thứ 6 | Cùng cả nhóm đối chiếu `01_SCOPE_AND_NON_GOALS.md`, chốt phạm vi MVP | (như Thái) | (như Thái) | (như Thái) |
| Thứ 7 | Demo nội bộ bản thiết kế, ghi nhận góp ý | | | |
| CN | Dự phòng | | | |

---

## Tuần 2 — Chốt miền nghiệp vụ (phần 2) + Contracts

**Mục tiêu:** Chốt contract/schema và ERD trước khi bootstrap code.
**Deliverable:** Domain rules + acceptance test cho vertical slice đã review xong.

| Ngày | Thái | Học | Khoa | Bảo |
|---|---|---|---|---|
| Thứ 2 | Thiết kế cấu trúc component web theo feature folder | Hoàn thiện ERD farms/plots/leases/crop_cycles | Hoàn thiện ERD telemetry/automation/work_orders | Chủ trì hoàn thiện 4 JSON schema trong `packages/contracts` |
| Thứ 3 | Review ERD của Học/Khoa (góc nhìn UI cần field gì) | Review chéo ERD với Khoa | Review chéo ERD với Học | Setup dự thảo CI pipeline (lint + test skeleton) |
| Thứ 4 | Viết README chi tiết cho `apps/web` | Viết README chi tiết cho phần mình phụ trách trong `apps/api` | Viết README cho `apps/gateway`, `apps/simulator` | Review toàn bộ README, đảm bảo nhất quán |
| Thứ 5 | Viết acceptance test (mô tả) cho vertical slice — góc nhìn UI | Viết acceptance test — góc nhìn lease/harvest | Viết acceptance test — góc nhìn telemetry/automation | Tổng hợp acceptance test thành 1 file, review với `01_SCOPE_AND_NON_GOALS.md` |
| Thứ 6 | Cả nhóm chốt roadmap chi tiết theo tuần, tạo board task (Trello/Jira/GitHub Projects) | | | |
| Thứ 7 | Demo/review cuối giai đoạn domain lock, retro | | | |
| CN | Dự phòng | | | |

---

## Tuần 3 — Bootstrap repo & foundation (phần 1)

**Mục tiêu:** Dựng khung chạy được cho cả 4 app.
**Deliverable:** Đăng nhập + xem danh sách plot (demo nội bộ).

| Ngày | Thái | Học | Khoa | Bảo |
|---|---|---|---|---|
| Thứ 2 | Scaffold React + Vite, routing, layout cơ bản | Scaffold FastAPI project + module `auth` | Scaffold MQTT client wrapper + khung `apps/simulator` | Docker Compose skeleton (Postgres+Timescale, MQTT broker, api, web) |
| Thứ 3 | Kết nối web scaffold với API health-check | Model user/roles + JWT auth | Simulator: vòng lặp publish dữ liệu giả lập | Setup CI (lint/test) pipeline |
| Thứ 4 | UI đăng nhập/đăng ký | API CRUD `farms`/`plots` | Khung `apps/gateway` subscribe command topic | Review migration script đầu tiên |
| Thứ 5 | UI danh sách plot, gọi API thật | API CRUD `crop_catalog` + seed dữ liệu cà chua | Stub endpoint ingest telemetry | Stub observability (định dạng log chuẩn) |
| Thứ 6 | Test tích hợp: login → xem danh sách plot (cả nhóm cùng test) | | | |
| Thứ 7 | Demo nội bộ: đăng nhập + xem danh sách plot | | | |
| CN | Dự phòng | | | |

---

## Tuần 4 — Bootstrap repo & foundation (phần 2)

**Mục tiêu:** Player xác thực được và thấy plot khả dụng (deliverable chính thức theo roadmap).
**Deliverable:** "Player can authenticate and view available plots."

| Ngày | Thái | Học | Khoa | Bảo |
|---|---|---|---|---|
| Thứ 2 | UI yêu cầu thuê lease (lease request) | Model Lease + khung state machine (draft→pending→active) | Khung policy engine (chỉ interface) | Middleware validate theo contract schema |
| Thứ 3 | UI chọn giống cây (từ crop_catalog) | Logic activation lease + validate (rule: 1 lease active/plot) | Thiết kế schema automation command + idempotency key | CI: thêm test coverage, test migration |
| Thứ 4 | UI shell cho dashboard (chưa game) | API tạo crop_cycle khi lease active | Tài liệu thiết kế watchdog + khung code | Scaffold `apps/ai-service` (FastAPI, health check) |
| Thứ 5 | Test tích hợp cùng nhóm: login → thuê plot → chọn giống → crop_cycle được tạo | | | |
| Thứ 6 | Viết test tự động (pytest) cho luồng lease + crop_cycle | | | |
| Thứ 7 | Demo tuần 4 — deliverable roadmap | | | |
| CN | Dự phòng | | | |

---

## Tuần 5 — Lease & crop-cycle vertical slice (phần 1)

**Mục tiêu:** Học dẫn dắt hoàn thiện state machine lease/crop-cycle.
**Deliverable:** Kích hoạt lease → chọn giống → operator xác nhận trồng → crop_cycle "planted".

| Ngày | Thái | Học | Khoa | Bảo |
|---|---|---|---|---|
| Thứ 2 | Dashboard hiển thị trạng thái lease/crop-cycle | Hoàn thiện Lease state machine đầy đủ (kể cả cancelled/expired/terminated) | Chuẩn bị cấu trúc MQTT topic cho simulator (song song, không block Học) | Hỗ trợ Học viết migration cho bảng lease/crop_cycle |
| Thứ 3 | UI timeline crop-cycle | Hoàn thiện CropCycle state machine đầy đủ (kể cả failed/cancelled) | Simulator publish 3 cảm biến cơ bản (nhiệt độ, độ ẩm khí, độ ẩm đất) | Hỗ trợ Docker volume/seed script cho test |
| Thứ 4 | Hoàn thiện wireframe dashboard | API operator xác nhận trồng (role check Farm Operator) | Review contract simulator ↔ gateway thật (đảm bảo giống nhau) | Thêm CI test cho module lease |
| Thứ 5 | Kết nối dashboard với API thật | Unit test business rule (1 lease/1 crop-cycle active mỗi plot) | Cấu hình MQTT broker (QoS phù hợp) | Review bảo mật JWT (thời hạn, refresh token) |
| Thứ 6 | Test tích hợp: kích hoạt lease → chọn giống → operator xác nhận → crop_cycle "planted" | | | |
| Thứ 7 | Demo tuần 5 | | | |
| CN | Dự phòng | | | |

---

## Tuần 6 — Lease & crop-cycle vertical slice (phần 2)

**Mục tiêu:** Xử lý edge case + bắt đầu policy engine thật.
**Deliverable:** "Active player plot appears in a basic non-game dashboard."

| Ngày | Thái | Học | Khoa | Bảo |
|---|---|---|---|---|
| Thứ 2 | UI trạng thái pending/rejected cho lease request | Xử lý edge case: activation fail khi plot unavailable/unsafe | Bắt đầu policy engine thật (input: action, output: quyết định) | Hỗ trợ Khoa thiết kế schema policy decision |
| Thứ 3 | Hiển thị lý do (human-readable reason) trên UI | API trả reason string đúng theo `02_BUSINESS_RULES.md` | Policy engine cho 1-2 loại action mẫu (tưới nước) | Viết test cho `ai-service` skeleton |
| Thứ 4 | Hoàn thiện dashboard | API phục vụ dashboard (đọc lease/crop-cycle) | Xử lý idempotency key cho automation command | Chuẩn bị môi trường demo (docker-compose up chạy trọn vẹn) |
| Thứ 5 | Regression test cùng nhóm cho toàn bộ luồng lease→crop-cycle | | | |
| Thứ 6 | Sửa lỗi, code review chéo toàn bộ nhóm | | | |
| Thứ 7 | Demo tuần 6 — deliverable roadmap | | | |
| CN | Dự phòng | | | |

---

## Tuần 7 — Telemetry & automation (phần 1)

**Mục tiêu:** Khoa dẫn dắt telemetry realtime, Bảo hỗ trợ hạ tầng MQTT/Timescale.
**Deliverable:** Simulator gửi dữ liệu → lưu DB → hiển thị realtime trên UI.

| Ngày | Thái | Học | Khoa | Bảo |
|---|---|---|---|---|
| Thứ 2 | Chuẩn bị UI hiển thị số liệu realtime (placeholder chart) | Chuẩn bị endpoint nhận telemetry (liên kết plot/crop_cycle) | Hoàn thiện contract MQTT topic (telemetry + command ack) dùng chung simulator/gateway | Dựng MQTT broker (Mosquitto) trong docker-compose, hỗ trợ Khoa |
| Thứ 3 | Kết nối UI với WebSocket endpoint (stub) | Validate dữ liệu (giá trị bất thường → quarantine, theo `AGENTS.md` mục 8) | Tạo TimescaleDB hypertable cho measurement | Hỗ trợ cấu hình TimescaleDB extension trong Docker |
| Thứ 4 | Chart hiển thị nhiệt độ/độ ẩm realtime | Review liên kết telemetry–plot | Rule engine v1 (nhiệt độ > ngưỡng → bật quạt) | Hỗ trợ containerize gateway service |
| Thứ 5 | UI cảnh báo khi vượt ngưỡng | Hỗ trợ đảm bảo automation gắn đúng crop_cycle đang active | Watchdog logic (ngắt khi vượt thời gian an toàn) | Viết test tích hợp MQTT (publish → ingest → lưu DB) |
| Thứ 6 | Test tích hợp: simulator → DB → UI realtime | | | |
| Thứ 7 | Demo tuần 7 | | | |
| CN | Dự phòng | | | |

---

## Tuần 8 — Telemetry & automation (phần 2)

**Mục tiêu:** Nối policy engine thật với automation, có ack từ gateway.
**Deliverable:** "Safe watering request works end to end."

| Ngày | Thái | Học | Khoa | Bảo |
|---|---|---|---|---|
| Thứ 2 | Form gửi yêu cầu tưới nước (player action request UI) | API endpoint submit action request | Automation command publish qua MQTT + nhận ack từ gateway | Hỗ trợ debug network Docker giữa api/gateway/broker |
| Thứ 3 | UI hiển thị trạng thái action (accepted/scheduled/rejected) | Validate action request theo policy (business rule) | Policy engine kết nối thật với automation (`accepted_for_automation` → publish command) | Log/observability cho MQTT messages |
| Thứ 4 | UI hiển thị lịch sử action request | Liên kết action request với crop_cycle | Xử lý command timeout/failed (không báo completed sai) | Hỗ trợ viết test cho watchdog |
| Thứ 5 | Cả nhóm: end-to-end test "safe watering request" | | | |
| Thứ 6 | Sửa lỗi, code review | | | |
| Thứ 7 | Demo tuần 8 — deliverable roadmap | | | |
| CN | Dự phòng | | | |

---

## Tuần 9 — Human work orchestration (phần 1)

**Mục tiêu:** Khoa dẫn dắt work order; Bảo bắt đầu chuyển sang thu thập dữ liệu AI (Khoa hỗ trợ camera/gateway).
**Deliverable:** Nhà vận hành nhận work order → hoàn thành → upload evidence.

| Ngày | Thái | Học | Khoa | Bảo |
|---|---|---|---|---|
| Thứ 2 | Wireframe operator portal | Hỗ trợ liên kết work_order–crop_cycle | Model work_order + state machine (draft→assigned→accepted→in_progress→completed→verified) | Bắt đầu thu thập ảnh mẫu bệnh lá (tải subset PlantVillage); Khoa hỗ trợ setup camera/gateway chụp ảnh mẫu |
| Thứ 3 | Operator portal — danh sách work order | Model care_log | Logic assignment + priority cho work order | Tiền xử lý ảnh (resize, augment) |
| Thứ 4 | Operator portal — chi tiết 1 work order + upload evidence | Liên kết care_log với action request tự động | API upload evidence (before/after) | Chọn kiến trúc baseline model (transfer learning) |
| Thứ 5 | UI xem lịch sử care | Validate business rule cho care_log | Xử lý exception thiếu evidence cần review | Setup script training v0 (chưa train thật) |
| Thứ 6 | Test tích hợp: nhận work order → hoàn thành → upload evidence | | | |
| Thứ 7 | Demo tuần 9 | | | |
| CN | Dự phòng | | | |

---

## Tuần 10 — Human work orchestration (phần 2)

**Mục tiêu:** Hoàn thiện operator portal; Bảo train baseline model lần đầu.
**Deliverable:** "Manual inspection request works end to end."

| Ngày | Thái | Học | Khoa | Bảo |
|---|---|---|---|---|
| Thứ 2 | Hoàn thiện operator portal | Hỗ trợ review incident model liên quan | Work order batching (gộp request cùng lô) | Train baseline model lần 1, ghi nhận accuracy/F1 |
| Thứ 3 | Timeline chăm sóc trên UI player | Liên kết incident–lease (customer notification) | Model incident + API reporting | Đánh giá model, xác định ngưỡng confidence cho manual-review |
| Thứ 4 | UI work order timeline cho player (customer-safe status) | Notification service cơ bản | Hoàn thiện API work_order cho operator portal | Viết API inference endpoint (model version, confidence, timestamp) |
| Thứ 5 | Cả nhóm: end-to-end "manual inspection request" | | | |
| Thứ 6 | Sửa lỗi, review | | | |
| Thứ 7 | Demo tuần 10 — deliverable roadmap | | | |
| CN | Dự phòng | | | |

---

## Tuần 11 — Game-like Digital Twin (phần 1)

**Mục tiêu:** Thái dẫn dắt Phaser UI; Học hỗ trợ nối state thật.
**Deliverable:** Chơi thử được luồng game từ đầu đến cuối.

| Ngày | Thái | Học | Khoa | Bảo |
|---|---|---|---|---|
| Thứ 2 | Setup Phaser scene trong React (canvas cơ bản) | Chuẩn bị API tổng hợp dữ liệu cho digital twin (plot + crop_cycle + health) | Ổn định lại IoT (fix bug tồn đọng từ tuần 7-10) | Tiếp tục cải thiện model / hỗ trợ Thái nếu cần xử lý ảnh |
| Thứ 3 | Vẽ sprite lô đất + trạng thái theo giai đoạn cây | API growth stage/health summary | Hỗ trợ Thái nếu Phaser cần dữ liệu telemetry realtime | Chuẩn bị demo kết quả model |
| Thứ 4 | Tương tác click chọn lô → mở camera snapshot | Hỗ trợ Thái wiring state (lease/crop-cycle status → sprite) | Đảm bảo camera endpoint ổn định | Tinh chỉnh model |
| Thứ 5 | Hiển thị action request trực tiếp từ Phaser scene | Review cùng Thái toàn bộ luồng player action từ UI game | Fix bug automation nếu phát sinh | Viết test cho `ai-service` |
| Thứ 6 | Test tích hợp: chơi thử luồng game (login → xem plot → request action) | | | |
| Thứ 7 | Demo tuần 11 | | | |
| CN | Dự phòng | | | |

---

## Tuần 12 — Game-like Digital Twin (phần 2)

**Mục tiêu:** Hoàn thiện UI game, tích hợp thử AI baseline.
**Deliverable:** "MVP vertical slice in game-like UI."

| Ngày | Thái | Học | Khoa | Bảo |
|---|---|---|---|---|
| Thứ 2 | Notification feedback trên UI game (toast/banner) | Hỗ trợ cuối cho state sync | Buffer sửa lỗi IoT | Buffer AI, chuẩn bị tích hợp |
| Thứ 3 | Timeline + camera snapshot hoàn thiện trong Phaser | Kiểm tra lại toàn bộ business rule hiển thị đúng | Kiểm tra watchdog/automation ổn định | Tích hợp thử AI baseline hiển thị demo (chưa nối luồng chính thức) |
| Thứ 4 | Polish UI/UX, kiểm tra responsive | Test lại toàn bộ API liên quan UI | Test lại toàn bộ luồng MQTT | Viết docs cho model (version, metrics, baseline) |
| Thứ 5 | Cả nhóm: end-to-end test toàn bộ vertical slice UI game | | | |
| Thứ 6 | Sửa lỗi, review chéo | | | |
| Thứ 7 | Demo tuần 12 — deliverable roadmap | | | |
| CN | Dự phòng | | | |

---

## Tuần 13 — Harvest & traceability (phần 1)

**Mục tiêu:** Học + Bảo phối hợp nối AI baseline vào luồng harvest chính thức.
**Deliverable:** Thu hoạch → entitlement → yêu cầu nhận hàng.

| Ngày | Thái | Học | Khoa | Bảo |
|---|---|---|---|---|
| Thứ 2 | UI ghi nhận/hiển thị harvest summary | Model HarvestBatch + API ghi nhận thu hoạch (weight, quality) | Hỗ trợ evidence/incident cho harvest nếu cần | Chuẩn bị tích hợp AI baseline vào luồng disease alert chính thức |
| Thứ 3 | UI hiển thị harvest entitlement cho player | HarvestEntitlement (liên kết harvest–lease) | Review incident liên quan tới harvest thất bại | API inference thật nối vào crop_cycle (ghi model version/confidence) |
| Thứ 4 | UI cảnh báo bệnh trên digital twin | Logic accepted/rejected quantity (rule: sản phẩm không an toàn không giao) | Hỗ trợ notification khi có cảnh báo bệnh | Luồng manual-review khi confidence thấp |
| Thứ 5 | UI pickup/delivery request | API pickup/delivery request | Buffer | Đánh giá lại metrics, viết tài liệu failure case |
| Thứ 6 | Test tích hợp: thu hoạch → entitlement → yêu cầu nhận hàng | | | |
| Thứ 7 | Demo tuần 13 | | | |
| CN | Dự phòng | | | |

---

## Tuần 14 — Harvest & traceability (phần 2)

**Mục tiêu:** Hoàn thiện truy xuất nguồn gốc off-chain + QR.
**Deliverable:** "Complete lease-to-harvest demonstration."

| Ngày | Thái | Học | Khoa | Bảo |
|---|---|---|---|---|
| Thứ 2 | UI QR/timeline read-only | API traceability off-chain timeline | Hỗ trợ QA luồng automation trước khi hardening | Tính integrity hash (SHA-256) cho traceability record |
| Thứ 3 | Hoàn thiện UI QR timeline | API generate QR + endpoint tra cứu | Buffer sửa lỗi | (Tuỳ chọn) stub blockchain adapter theo ADR-0004 — **không bật mặc định** |
| Thứ 4 | Polish UI | Test toàn bộ luồng harvest-to-traceability | Buffer | Viết test cho hash integrity |
| Thứ 5 | Cả nhóm: end-to-end "complete lease-to-harvest demonstration" | | | |
| Thứ 6 | Sửa lỗi, review chéo toàn bộ | | | |
| Thứ 7 | Demo tuần 14 — deliverable roadmap | | | |
| CN | Dự phòng | | | |

---

## Tuần 15 — Hardening (phần 1)

**Mục tiêu:** Kiểm thử toàn diện, bảo mật, hiệu năng.
**Deliverable:** Hệ thống ổn định, sẵn sàng rehearsal.

| Ngày | Cả nhóm |
|---|---|
| Thứ 2 | Viết e2e test (Cypress/Playwright) cho toàn bộ user journey chính |
| Thứ 3 | Khoa + Bảo: security & authorization review (theo `12_SECURITY_AND_PRIVACY.md`); Thái + Học: viết thêm test case còn thiếu |
| Thứ 4 | Khoa: real hardware substitution test (nếu có phần cứng) — thay simulator bằng gateway thật, kiểm tra contract không đổi |
| Thứ 5 | Cả nhóm: performance check (API latency, độ trễ MQTT < 2 giây theo business rule) |
| Thứ 6 | Viết báo cáo/tài liệu, chuẩn bị slide |
| Thứ 7 | Rehearsal demo lần 1 |
| CN | Dự phòng / nghỉ |

---

## Tuần 16 — Hardening & Bảo vệ

**Mục tiêu:** Hoàn thiện, tổng duyệt, bảo vệ đồ án.
**Deliverable:** "Defendable, repeatable demonstration."

| Ngày | Cả nhóm |
|---|---|
| Thứ 2 | Sửa lỗi phát hiện từ rehearsal lần 1 |
| Thứ 3 | Chuẩn bị backup demo (video quay sẵn phòng khi demo trực tiếp lỗi) |
| Thứ 4 | Hoàn thiện slide + báo cáo cuối |
| Thứ 5 | Rehearsal demo lần 2 (cả nhóm phản biện chéo) |
| Thứ 6 | Buffer cuối cùng, kiểm tra checklist bảo vệ |
| Thứ 7 | Bảo vệ / nộp đồ án |
| CN | Dự phòng |

---

## Ghi chú áp dụng

- Đây là bản kế hoạch **quy hoạch**, cần hiệu chỉnh sau mỗi tuần theo tiến độ thực tế (giống cách `10_ROADMAP_16_WEEKS.md` đã nêu).
- Không đổi hướng sản phẩm giữa chừng theo tài liệu docx cũ (xem memory "docx vs repo pivot") — mọi task ở trên bám theo mô hình Player thuê plot, blockchain optional, AI tối giản đã chốt trong `docs/`.
- Nếu một người bị chậm tiến độ ở tuần "nặng" của họ (Học: 5-6, Khoa: 7-8, Thái: 11-12, Bảo: 9-10 & 13-14), người hỗ trợ đã được chỉ định ở bảng trên nên chủ động lấn sang giúp thay vì chờ được yêu cầu.
