# Livp文件转jpg

`python livp2img.py`

> 直接把livp里的图片文件二进制提取出来了
> 会查找文件夹下所有livp文件并将图片提取后，使用相同文件名保存
> 通过逐个获取文件头的方式来拉zip中的文件。
> 速度快些，并且除了 heic2jpg 的过程，不需要其他库，代码量很小
> 顺序为 jpeg -> heic -> jpg
> 文件头可以参考 livp2img.FileEofs


- 支持 heic 类型的图片，当时需要 pillow & pillow_heif 库以将 heic 转换为jpg
  - 无 pillow 会跳过转换，当时同名的 heic 还是会提取的
- 对 jpeg 有简单的兼容性……
  - 是指会提前查找是不是有 ff d8 ff e0(e1是jpg,e0是jpeg)
  - 否则可能出现提取出来的 jpg 是黑白的

之前因为时间和需求问题，一直没有更新，并且存档.
现在已将部分问题解决。