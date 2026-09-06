const fs = require('fs');
const path = require('path');

/**
 * 文档模板管理
 *
 * 模板以 .tex 文件形式存放在 src/config/templates/ 下，由 manifest.json 索引。
 * 用户可以直接编辑这些 .tex 文件自定义模板，重启应用后生效 —— 这正是
 * README 的 FAQ 里承诺的行为（此前该目录根本不存在，模板硬编码在 Vue 组件里）。
 *
 * 支持四种占位符：{{TITLE}} {{AUTHOR}} {{DATE}} {{MAJOR_PACKAGES}}
 */

const TEMPLATE_DIR = path.join(__dirname, '../config/templates');

// 内存缓存：模板文件不常变，避免每次打开向导都读盘
let cache = null;
let cacheMtime = 0;

function readManifest() {
  const manifestPath = path.join(TEMPLATE_DIR, 'manifest.json');
  const stat = fs.statSync(manifestPath);

  if (cache && stat.mtimeMs === cacheMtime) {
    return cache;
  }

  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
  cache = manifest;
  cacheMtime = stat.mtimeMs;
  return manifest;
}

function formatDate(date) {
  const d = date || new Date();
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

/**
 * 列出全部模板与专业，供文档向导渲染卡片。
 */
function listTemplates() {
  const manifest = readManifest();

  const templates = manifest.templates.map((t) => {
    let available = true;
    let size = 0;
    try {
      size = fs.statSync(path.join(TEMPLATE_DIR, t.file)).size;
    } catch (e) {
      available = false;
    }
    return {
      id: t.id,
      label: t.label,
      icon: t.icon,
      description: t.description,
      defaultTitle: t.defaultTitle || t.label,
      defaultAuthor: t.defaultAuthor || '',
      file: t.file,
      available,
      size,
    };
  });

  const majors = Object.keys(manifest.majors || {}).map((key) => ({
    value: key,
    label: manifest.majors[key].label,
    icon: manifest.majors[key].icon,
    description: manifest.majors[key].description,
  }));

  return { success: true, templates, majors };
}

/**
 * 渲染指定模板。
 * @param {string} templateId  manifest 里的模板 id
 * @param {string} major       manifest 里的专业 key
 * @param {object} fields      覆盖默认值的字段（title / author / date）
 */
function renderTemplate(templateId, major, fields) {
  try {
    const manifest = readManifest();
    const meta = (manifest.templates || []).find((t) => t.id === templateId);
    if (!meta) {
      return { success: false, error: `未知模板: ${templateId}` };
    }

    const filePath = path.join(TEMPLATE_DIR, meta.file);
    if (!fs.existsSync(filePath)) {
      return {
        success: false,
        error: `模板文件缺失: ${meta.file}（请检查 src/config/templates/ 目录）`,
      };
    }

    const f = fields || {};
    const title = f.title || meta.defaultTitle || '';
    const author = f.author || meta.defaultAuthor || '';
    const date = f.date || formatDate();
    const majorPackages = (manifest.majors || {})[major]
      ? (manifest.majors[major].packages || '')
      : '';

    let content = fs.readFileSync(filePath, 'utf-8');
    content = content
      .split('{{TITLE}}').join(title)
      .split('{{AUTHOR}}').join(author)
      .split('{{DATE}}').join(date)
      .split('{{MAJOR_PACKAGES}}').join(majorPackages);

    // 专业宏包为空时会留下空行，清理掉避免文档里出现莫名空白
    content = content.replace(/\n{3,}/g, '\n\n');

    return { success: true, content, template: templateId, major };
  } catch (e) {
    return { success: false, error: `模板渲染失败: ${e.message}` };
  }
}

module.exports = {
  TEMPLATE_DIR,
  listTemplates,
  renderTemplate,
  formatDate,
};
