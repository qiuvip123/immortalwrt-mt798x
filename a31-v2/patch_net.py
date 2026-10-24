p = 'target/linux/mediatek/mt7981/base-files/etc/board.d/02_network'
s = open(p).read()
net_case = """\t*konka,komi-a31*)
\t\tucidef_set_interfaces_lan_wan "lan1 lan2 lan3" wan
\t\t;;
"""
anchor = "\t*)"
idx = s.find(anchor)
assert idx > 0, 'default case not found'
s = s[:idx] + net_case + s[idx:]
open(p, 'w').write(s)
print('02_network patched')
