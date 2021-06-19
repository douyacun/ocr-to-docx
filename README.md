# 图片文件识别，格式化导出为word

网站地址：[https://www.douyacun.com/image/ocr-to-docx](https://www.douyacun.com/image/ocr-to-docx)

**功能特点：**

1. 识别图片上的文字
2. 按照图片文字样式进行格式化
3. 导出为word文档
4. 2算法实现：googel-tesseract-ocr / easyocr
5. 借助开源库实现，功能免费

**使用：**

tesseract 导出为word

```shell
python tesseract.py hocr_to_docx a.png a.docx
```

easyocr 导出为word

```shell
python easy.py  ocr_to_docx a.png a.docx
```
