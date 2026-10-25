#!/bin/sh
# KOMI A31: LAN IP=192.168.2.1, root 无密码, WiFi 开放
# 仅对 KOMI A31 生效，其他设备（如 JCG Q30）自动跳过
grep -q "KONKA KOMI A31" /proc/device-tree/model 2>/dev/null || exit 0

# LAN IP -> 192.168.2.1
uci set network.lan.ipaddr='192.168.2.1'

# WiFi 开放（加密 none + 清除 key）
for iface in default_MT7981_1_1 default_MT7981_1_2; do
	uci -q delete wireless.$iface.key
	uci set wireless.$iface.encryption='none'
done

# root 登录无密码
sed -i 's/^root:[^:]*:/root::/' /etc/shadow

uci commit network
uci commit wireless
exit 0