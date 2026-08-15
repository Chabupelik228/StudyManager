import { marked } from 'marked';
import katex from 'katex';
import DOMPurify from 'dompurify';

// Configure marked renderer
const renderer = new marked.Renderer();

// Custom code block renderer with wrapper for styling
renderer.code = function ({ text, lang }: { text: string; lang?: string }) {
  const cleanLang = (lang || '').trim();
  const escapedCode = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
  return `
    <div class="code-block-wrapper my-2">
      ${cleanLang ? `<div class="text-[10px] uppercase font-mono px-3 py-1 bg-black/5 text-gray-500 border-b border-black/5 dark:border-white/5">${cleanLang}</div>` : ''}
      <pre><code class="language-${cleanLang}">${escapedCode}</code></pre>
    </div>
  `;
};

// Custom table renderer to ensure responsive container
renderer.table = function (token: any) {
  // Let default table generator or custom html wrap it
  let headerHtml = '';
  if (token.header) {
    headerHtml = '<thead><tr>' + token.header.map((cell: any) => `<th>${cell.text}</th>`).join('') + '</tr></thead>';
  }
  let bodyHtml = '';
  if (token.rows) {
    bodyHtml = '<tbody>' + token.rows.map((row: any) => '<tr>' + row.map((cell: any) => `<td>${cell.text}</td>`).join('') + '</tr>').join('') + '</tbody>';
  }
  return `
    <div class="overflow-x-auto my-2 rounded-lg border border-black/10 dark:border-white/10 max-w-full">
      <table class="min-w-full text-xs">${headerHtml}${bodyHtml}</table>
    </div>
  `;
};

marked.setOptions({
  renderer,
  gfm: true,
  breaks: true,
});

/**
 * Render LaTeX math equations in text using KaTeX.
 * Handles both block math $$...$$ and inline math $...$
 */
function renderMath(text: string): string {
  // 1. Block math: $$...$$
  let processed = text.replace(/\$\$([\s\S]+?)\$\$/g, (_match, math) => {
    try {
      return `<div class="katex-display my-2 overflow-x-auto text-center">${katex.renderToString(math.trim(), {
        displayMode: true,
        throwOnError: false,
      })}</div>`;
    } catch {
      return `$$${math}$$`;
    }
  });

  // 2. Inline math: $...$ (ignoring escaped \$ or numbers like $10)
  processed = processed.replace(/(^|[^\\])\$([^\$\n]+?)\$/g, (_match, prefix, math) => {
    try {
      const rendered = katex.renderToString(math.trim(), {
        displayMode: false,
        throwOnError: false,
      });
      return `${prefix}${rendered}`;
    } catch {
      return `${prefix}$${math}$`;
    }
  });

  return processed;
}

/**
 * Safely render Markdown with KaTeX math and DOMPurify XSS sanitization.
 */
export function renderSafeMarkdown(content: string): string {
  if (!content) return '';

  // 1. Render LaTeX formulas
  const withMath = renderMath(content);

  // 2. Parse Markdown
  const rawHtml = marked.parse(withMath) as string;

  // 3. Sanitize HTML with DOMPurify (prevent XSS)
  const cleanHtml = DOMPurify.sanitize(rawHtml, {
    ADD_TAGS: [
      'math', 'mrow', 'mi', 'mo', 'mn', 'msup', 'msub', 'mfrac', 'mroot', 'msqrt',
      'mtable', 'mtr', 'mtd', 'span', 'div', 'pre', 'code', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
    ],
    ADD_ATTR: [
      'class', 'style', 'aria-hidden', 'role', 'mathvariant', 'xmlns', 'viewBox', 'loading',
    ],
  });

  return cleanHtml;
}
