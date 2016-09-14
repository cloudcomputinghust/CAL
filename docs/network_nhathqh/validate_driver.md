# Validate Driver Docs

## Mục đích
- Chọn cloud driver tương ứng theo request người dùng
- Kiểm tra trạng thái hoạt động của cloud driver

## Điều kiện áp dụng
- Với những request của người dùng tương tác trên 1 cloud

## Ý tưởng
1. Lấy list các driver từ Broker
2. Filter các driver trong list theo trạng thái hiện tại của cloud (cloud_enable = true, cloud_state = active) và theo request người dùng (name,id,cloud_type)
3. Kiểm tra trạng thái hoạt động (cloud_state) của những cloud phù hợp theo token/user-pass, endpoint
4. Cập nhật trạng thái hoạt động (cloud_state) của những cloud bị lỗi (error)
5. Trả về driver phù hợp

![Biểu đồ luồng hoạt động] (https://github.com/cloudcomputinghust/CAL/blob/resource/docs/network_nhathqh/images/validate_driver_workflow.png)

## Vướng mắc và hạn chế hiện tại
- Hiện tại chỉ áp dụng với trường hợp request của người dùng tương tác trên 1 cloud, chưa xét đến trường hợp tương tác giữa 2 cloud khác nhau.
- Nếu cloud_state = error thì khi nào và ở đâu sẽ cho phép cập nhật lại cloud_state = active ???
