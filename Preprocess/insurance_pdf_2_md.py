import os
import sys
import subprocess
import psutil  # 用於設置 CPU 核心親和力

def set_cpu_affinity(cores=[0, 1, 2, 3]):
    """
    設置程式的 CPU 親和性，只允許使用指定的核心。
    :param cores: 要分配的 CPU 核心列表，默認為核心 0 和 1
    """
    p = psutil.Process()
    p.cpu_affinity(cores)  # 設置多個核心的親和性
    print(f"已設置 CPU 親和性到核心: {cores}")

def set_gpu_device(device="cuda"):
    """
    設置 GPU 設備環境變量以使用 GPU。
    :param device: 設置為 "cuda" 以使用 GPU，或者 "cpu" 以使用 CPU
    """
    os.environ["TORCH_DEVICE"] = device
    print(f"已設置 GPU 設備為: {device}")

def convert_pdf_to_markdown(input_path, output_path, batch_multiplier=2, max_pages=None, ocr_all_pages=False):
    """
    將單個 PDF 文件轉換為 Markdown 文件，並保存到指定的輸出路徑。
    
    :param input_path: PDF 文件的路徑
    :param output_path: 保存轉換後的 Markdown 文件的路徑
    :param batch_multiplier: 用於提高速度的批量處理大小（默認為 2）
    :param max_pages: 最大處理頁數，如果不設置則轉換整個文檔
    :param ocr_all_pages: 是否對所有頁面強制執行 OCR
    """
    # 檢查是否已經生成了 Markdown 文件，避免重複處理
    markdown_file = os.path.join(output_path, os.path.splitext(os.path.basename(input_path))[0] + ".md")
    if os.path.exists(markdown_file):
        print(f"已存在: {markdown_file}，跳過該文件")
        return

    command = [
        "marker_single", 
        input_path, 
        output_path,
        "--batch_multiplier", str(batch_multiplier)
    ]

    if max_pages:
        command += ["--max_pages", str(max_pages)]
    
    if ocr_all_pages:
        command.append("--ocr_all_pages")
    
    # 設置使用的 GPU 設備（由 set_gpu_device 設置）
    # 執行命令，並檢查是否成功
    try:
        result = subprocess.run(command, check=True)
        print(f"成功處理: {input_path}")
    except subprocess.CalledProcessError as e:
        print(f"處理失敗: {input_path}，錯誤: {e}")
    except Exception as e:
        print(f"其他錯誤: {input_path}，錯誤: {e}")

def convert_multiple_pdfs(input_folder, output_folder, max_files=None):
    """
    將指定文件夾內的多個 PDF 文件逐個轉換為 Markdown 文件，並保存到指定的輸出文件夾。
    
    :param input_folder: PDF 文件的來源文件夾
    :param output_folder: 保存轉換後 Markdown 文件的目標文件夾
    :param max_files: 最大處理文件數量（可選）
    """
    # 設置 CPU 親和性到指定的單個核心
    set_cpu_affinity([0, 1, 2, 3])

    # 設置 GPU 設備（此處設置為 "cuda" 使用 GPU）
    set_gpu_device(device="cuda")

    # 確保輸出文件夾存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 獲取文件夾內的所有 PDF 文件
    pdf_files = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]

    # 限制最大處理的文件數量（如果設置了 max_files）
    if max_files:
        pdf_files = pdf_files[:max_files]

    # 逐個處理每個 PDF 文件
    for pdf_file in pdf_files:
        input_path = os.path.join(input_folder, pdf_file)

        # 獲取文件名（不含擴展名）
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        # 創建以文件名命名的子文件夾
        file_folder = os.path.join(output_path, file_name)

        # 定義 Markdown 文件的完整路徑
        markdown_file = os.path.join(file_folder, file_name + ".md")
        print(markdown_file)
        # 檢查對應的 Markdown 文件是否已經存在
        if os.path.exists(markdown_file):
            print(f"文件已經處理過: {markdown_file}，跳過該文件")
            continue

        print(f"正在處理文件: {input_path}")
        convert_pdf_to_markdown(input_path, output_folder)

    print("所有 PDF 文件已處理完畢！")

if __name__ == "__main__":
    
    input_path = r"C:\Users\Lockdream\Desktop\AI_CUP_2024\AI_CUP_2024\reference\insurance"
    output_path = r"C:\Users\Lockdream\Desktop\AI_CUP_2024\AI_CUP_2024\insurance_markdown"
    input_path='./1.pdf'
    output_path='./'
    # 判斷是否提供了命令行參數，如果有則覆蓋預設的路徑
    if len(sys.argv) >= 3:
        input_path = sys.argv[1]
        output_path = sys.argv[2]

    if os.path.isfile(input_path):
        # 單個文件處理
        convert_pdf_to_markdown(input_path, output_path)
    elif os.path.isdir(input_path):
        # 逐個處理文件夾中的所有 PDF 文件
        convert_multiple_pdfs(input_path, output_path)
    else:
        print(f"無效的路徑: {input_path}")
        sys.exit(1)