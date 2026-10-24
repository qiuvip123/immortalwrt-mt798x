p = 'target/linux/mediatek/mt7981/base-files/lib/upgrade/platform.sh'
s = open(p).read()
old_up = """\t*snand*)
\t\tubi_do_upgrade "$1"
\t\t;;"""
new_up = """\t*konka,komi-a31*)
\t\tnand_do_upgrade "$1"
\t\t;;
\t*snand*)
\t\tubi_do_upgrade "$1"
\t\t;;"""
assert old_up in s, 'upgrade anchor missing'
s = s.replace(old_up, new_up)
old_ck = """\t*snand* |\\
\t*emmc*)"""
new_ck = """\t*konka,komi-a31* |\\
\t*snand* |\\
\t*emmc*)"""
assert old_ck in s, 'check anchor missing'
s = s.replace(old_ck, new_ck)
open(p, 'w').write(s)
print('platform.sh patched')
