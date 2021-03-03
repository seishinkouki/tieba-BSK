# tieba-BSK
>纯python native生成百度贴吧回帖BSK参数(WIP)

## 思路?

本人根据[8qwe24657913](https://github.com/8qwe24657913)大佬的[记录分析百度"BSK"脚本的过程](https://github.com/8qwe24657913/Analyze_baidu_BSK)仓库里生成工具生成了贴吧的新版BSK加密js代码,并用python对主要加解密逻辑进行了重写, 在调试js的过程中也大概知道了所有参数的含义, 均已注释在python代码中.同时感谢[bigtrace](https://github.com/bigtrace)大佬的[在线工具](http://www.baidubsk.site)的便利


## BSK加密大概原理

简单来说百度记录了浏览器中的34个参数, 将这些参数的键值对字符串与 tbs 进行XOR运算后用base64编码就是我们在F12里面看到的_BSK参数, 这些参数可以用来识别用户行为,进而反spam.

## 可以直接用?
抱歉目前不行,虽然个人认为逆向出来的BSK算法应该没有问题(用真实的BSK和tbs计算过一个字节不差), 但是实际使用中依然会百分百被百度认定为机器人,所以可能百度对参数中轨迹有更加深层的判断,简单的随机没用
