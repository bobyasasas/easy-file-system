# app.py
import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 用于flash消息

# 配置上传文件夹
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """允许所有文件类型"""
    return True

def get_files_and_folders(path):
    """获取指定路径下的文件和文件夹列表"""
    items = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        relative_path = os.path.relpath(item_path, app.config['UPLOAD_FOLDER'])
        # 标准化路径分隔符为正斜杠
        relative_path = relative_path.replace('\\', '/')
        items.append({
            'name': item,
            'is_dir': os.path.isdir(item_path),
            'path': relative_path
        })
    return sorted(items, key=lambda x: (not x['is_dir'], x['name'].lower()))

@app.route('/')
@app.route('/folder/<path:folder_path>')
def index(folder_path=''):
    """主页路由"""
    # 确保路径在上传文件夹内
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_path)

    # 安全检查：确保路径在上传文件夹内
    if not os.path.abspath(full_path).startswith(os.path.abspath(app.config['UPLOAD_FOLDER'])):
        flash('非法路径访问')
        return redirect(url_for('index'))

    if not os.path.exists(full_path):
        flash('文件夹不存在')
        return redirect(url_for('index'))

    items = get_files_and_folders(full_path)

    # 获取当前文件夹的父路径
    parent_path = os.path.dirname(folder_path) if folder_path else None
    current_folder = folder_path if folder_path else ''

    return render_template('index.html',
                         items=items,
                         current_folder=current_folder,
                         parent_path=parent_path)

@app.route('/upload', methods=['POST'])
def upload_file():
    """文件上传路由"""
    # 获取目标文件夹路径
    folder_path = request.form.get('folder_path', '')
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_path)

    # 检查是否有文件被上传
    if 'file' not in request.files:
        flash('没有选择文件')
        return redirect(request.referrer or url_for('index'))

    file = request.files['file']

    # 检查文件名是否为空
    if file.filename == '':
        flash('没有选择文件')
        return redirect(request.referrer or url_for('index'))

    # 移除文件类型检查，直接保存文件
    if file:
        filename = file.filename
        file.save(os.path.join(full_path, filename))
        flash('文件上传成功')

    return redirect(url_for('index', folder_path=folder_path))

@app.route('/download/<path:filename>')
def download_file(filename):
    """文件下载路由"""
    # 安全检查：确保路径在上传文件夹内
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.abspath(full_path).startswith(os.path.abspath(app.config['UPLOAD_FOLDER'])):
        flash('非法路径访问')
        return redirect(url_for('index'))

    # 检查是否是文件夹
    if os.path.isdir(full_path):
        flash('无法下载文件夹')
        return redirect(url_for('index', folder_path=os.path.dirname(filename)))

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/create_folder', methods=['POST'])
def create_folder():
    """创建文件夹路由"""
    folder_name = request.form.get('folder_name', '').strip()
    parent_path = request.form.get('folder_path', '')
    # 处理根目录情况
    if parent_path == '':
        parent_path = ''

    if not folder_name:
        flash('文件夹名称不能为空')
        return redirect(url_for('index', folder_path=parent_path if parent_path else None))

    # 防止路径遍历攻击
    if '..' in folder_name or '/' in folder_name or '\\' in folder_name:
        flash('文件夹名称包含非法字符')
        return redirect(url_for('index', folder_path=parent_path if parent_path else None))

    full_path = os.path.join(app.config['UPLOAD_FOLDER'], parent_path, folder_name)

    try:
        os.makedirs(full_path, exist_ok=False)
        flash(f'文件夹 "{folder_name}" 创建成功')
    except FileExistsError:
        flash(f'文件夹 "{folder_name}" 已存在')
    except Exception as e:
        flash(f'创建文件夹失败: {str(e)}')

    return redirect(url_for('index', folder_path=parent_path if parent_path else None))
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
