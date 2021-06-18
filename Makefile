#inFile="/Users/admin/Desktop/image-ocr/c.png"
#inFile="/Users/admin/Desktop/image-ocr/c.png"
inFile="/Users/admin/Desktop/image-ocr/f.png"

#inFile="/Users/liuning/Desktop/image-ocr/e.png"
outFile=$(shell echo ${inFile}|sed 's!.png!.docx!g'|sed 's!.jpg!.docx!g'|sed 's!.jpeg!.docx!g')

easyocr:
	python easy.py ocr_to_docx ${inFile} ${outFile}

easyocr-debug:
	python main.py debug ${inFile}

tessract:
	python tessract.py hocr_to_docx ${inFile} ${outFile}

tessract-debug:
	python tessract.py hocr_to_docx -debug=true ${inFile} ${outFile}