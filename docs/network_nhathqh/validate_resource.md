# Validate Network Resource Docs

## Mục đích
- Kiểm tra qouta của resource trước khi resource thực hiện action tương tác với cloud theo request của người dùng
- Kiểm tra điều kiện liên thông giữa các network và cloud theo request của người dùng

## Điều kiện
- Sau khi đã pass qua bước validate driver

## Kiểm tra qouta
### Ý tưởng
#### Theo ý kiến Nhật HQH
- Qouta nằm trong driver

1. Resource gọi đến validate_driver theo action_name
2. Cập nhật qouta của driver nếu driver chưa có qouta hoặc thời gian lần cập nhật gần nhất vượt quá thời gian quy định
3. Kiểm tra các điều kiện qouta tương ứng với action và trả lại kết quả cho resource
4. Cập nhật các thay đổi của qouta (nếu có) vào driver

![validate_resource_nhathqh] (https://github.com/cloudcomputinghust/CAL/blob/resource/docs/network_nhathqh/images/validate_resource.png)

#### Theo ý kiến Đại ĐV
(updating)

### Cấu trúc qouta
- Biểu đồ lớp:

![] (https://github.com/cloudcomputinghust/CAL/blob/resource/docs/network_nhathqh/images/Qouta.png)

- Dict format cho Networks Qouta:

```
//Networks: list cách network hiện có trên cloud này

networks = 
{
  "network_id":
  {
    "cidr": 1.0.0.0/24,
    "usedIPs": [1.0.0.1, 1.0.0.2 ...],
    "firewalls": [firewall_id_1, firewall_id_2 ...]  //list các firewall đang áp dụng cho network này
    "internet_gateway": internet_gateway_id,
    "connect_igw": True/False,
    "vpn_gateway": vpn_gateway_id,
    "connect_vpngw": True/False
  }
}


// FloatingIPs: list các floating IP đã sử dụng trên cloud này 

floatingIPs = [192.168.50.100, 192.168.50.101 ...]


// Firewalls: list các fire đang có trên cloud này

firewalls =
{
  "firewalls_id":
  {
    "rule_id":
    {
      ... (protocol, direction, port_ranger, ...)
    }
  }
}
```

### Điều kiện kiểm tra qouta cho từng action
(updating)

## Kiểm tra liên thông network và cloud
(updating)

## Vướng mắc và hạn chế
