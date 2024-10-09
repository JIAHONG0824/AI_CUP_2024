import fitz  # PyMuPDF
import os

# PDF 文件路径
pdf_path="reference/finance"
for file in os.listdir(pdf_path):
    path=pdf_path+"/"+file
    pdf_document = fitz.open(path)

    # 输出图像的目录
    output_dir = f"finance_images/{file}"
    os.makedirs(output_dir, exist_ok=True)

    # 遍历每一页
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)  # 获取页面
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 渲染页面为图片
        
        # 保存图片为 PNG 格式
        image_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
        pix.save(image_path)
        print(f"保存图片: {image_path}")

    # 关闭 PDF 文件
    pdf_document.close()
