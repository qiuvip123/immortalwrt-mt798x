# -*- coding: utf-8 -*-
"""GitHub Actions 内执行：给 mt_wifi tarball 打 pChipCap EMI 补丁后重打包"""
import os, tarfile, shutil

src = 'dl/mt79xx_20220907-8b55f5.tar.xz'
tmp = '/tmp/mtwifi_patch'
shutil.rmtree(tmp, ignore_errors=True)
os.makedirs(tmp)
with tarfile.open(src) as tf:
    tf.extractall(tmp)

path = os.path.join(tmp, 'mt_wifi', 'chips', 'mt7981.c')
s = open(path, encoding='utf-8', errors='replace').read()
old = '\tMTWF_DBG(pAd, DBG_CAT_FW, DBG_SUBCAT_ALL, DBG_LVL_DEBUG,\n\t\t\t"emi physical base: 0x%08x, size: 0x%08x\\n",\n\t\t\tpChipCap->emi_phy_addr, pChipCap->emi_phy_addr_size);'
new = '#ifdef CONFIG_CONNINFRA_SUPPORT\n' + old + '\n#endif /* CONFIG_CONNINFRA_SUPPORT */'
assert old in s, 'mt7981.c EMI anchor not found'
open(path, 'w', encoding='utf-8', newline='\n').write(s.replace(old, new))
print('patched mt7981.c: EMI MTWF_DBG now guarded by CONFIG_CONNINFRA_SUPPORT')

with tarfile.open(src, 'w:xz') as tf:
    for name in sorted(os.listdir(tmp)):
        p = os.path.join(tmp, name)
        tf.add(p, arcname=name)
print('repacked', src, os.path.getsize(src))
