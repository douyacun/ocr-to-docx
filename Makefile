#inFile="/Users/admin/Desktop/image-ocr/c.png"
#inFile="/Users/admin/Desktop/image-ocr/c.png"
inFile="/Users/admin/Desktop/image-ocr/b.png"

#inFile="/Users/liuning/Desktop/image-ocr/c.png"
outFile=$(shell echo ${inFile}|sed 's!.png!.docx!g'|sed 's!.jpg!.docx!g'|sed 's!.jpeg!.docx!g')

docx:
	#echo ${outFile}
	python main.py docx ${inFile} ${outFile}

debug:
	python main.py debug ${inFile}
