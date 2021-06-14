inFile="/Users/admin/Desktop/image-ocr/c.png"
outFile=$(shell echo ${inFile}|sed 's!.png!.docx!g'|sed 's!.jpg!.docx!g'|sed 's!.jpeg!.docx!g')

main:
	#echo ${outFile}
	python main.py ${inFile} ${outFile}