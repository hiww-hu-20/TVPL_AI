import os
import re
import json
from docx import Document


def clean_text(text):
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        line_clean = re.sub(r'[^\w\s\.,;:\-\(\)áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỹđĐ]', ' ', line)
       
        line_clean = re.sub(r'\s+', ' ', line_clean).strip()
        
        def convert_money(match):
            num = match.group(1).replace(',', '.')
            try:
                val = float(num)
                val_int = int(val * 1_000_000)
                return f"{val_int:,} VNĐ".replace(',', '.')
            except:
                return match.group(0)
        line_clean = re.sub(r'(\d+[\.,]?\d*)m\b', convert_money, line_clean, flags=re.IGNORECASE)
        cleaned_lines.append(line_clean)
   
    return '\n'.join(cleaned_lines)


def split_into_dieu(text):
    lines = text.split('\n')
    dieu_indices = []
    pattern_title = re.compile(r'^Điều\s+(\d+)(\.|$)')

   
    for i, line in enumerate(lines):
        if pattern_title.match(line.strip()):
            dieu_indices.append(i)
    dieu_indices.append(len(lines))  

    dieu_dict = {}
    for idx in range(len(dieu_indices) - 1):
        start = dieu_indices[idx]
        end = dieu_indices[idx + 1]
        header_line = lines[start].strip()

        dieu_num_match = pattern_title.match(header_line)
        dieu_num = f"Điều {dieu_num_match.group(1)}"

        title = header_line[dieu_num_match.end():].strip()

        content_lines = lines[start + 1:end]
        content = '\n'.join(content_lines).strip()

        title = clean_text(title)
        content = clean_text(content)  

        dieu_key = dieu_num.lower().replace(' ', '_')
        dieu_dict[dieu_key] = {
            "title": title,
            "text": content
        }
    return dieu_dict

def process_docx(filepath):
    doc = Document(filepath)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    text = '\n'.join(full_text)
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    dieu_dict = split_into_dieu(text)
    return dieu_dict

def main():
    data_dir = os.path.join(os.getcwd(), 'data')
    output_dir = os.path.join(os.getcwd(), 'output')
    os.makedirs(output_dir, exist_ok=True)

    print("List all files in data:", os.listdir(data_dir))

    for filename in os.listdir(data_dir):
        if filename.endswith('.docx'):
            print(f"Processing {filename} ...")
            filepath = os.path.join(data_dir, filename)
            dieu_data = process_docx(filepath)
           
            out_filename = filename.replace('.docx', '.json')
            outpath = os.path.join(output_dir, out_filename)
            with open(outpath, 'w', encoding='utf-8') as f:
                json.dump(dieu_data, f, ensure_ascii=False, indent=2)
            print(f"Saved processed data to {outpath}")

if __name__ == "__main__":
    main()
