// Shared Markdown to HTML renderer — used by ArticleDetail and Articles preview
export function markdownToHtml(md) {
  if (!md) return ''
  const lines = md.split('\n')
  const result = []
  let i = 0
  let inCodeBlock = false
  let codeLang = ''
  let codeLines = []
  let inTable = false
  let tableRows = []
  let tableHeader = []
  let inBlockquote = false
  let blockquoteLines = []
  let listBuffer = []     // [{ indent, prefix, content, ordered }]
  let paraBuffer = []    // lines of a pending paragraph

  const flushParagraph = () => {
    if (paraBuffer.length === 0) return
    result.push(`<p class="md-p">${inlineFormat(paraBuffer.join('<br>'))}</p>`)
    paraBuffer = []
  }

  const flushList = () => {
    if (listBuffer.length === 0) return
    const isOrdered = listBuffer[0].ordered
    const tag = isOrdered ? 'ol' : 'ul'
    const cls = isOrdered ? 'md-ol' : 'md-ul'
    const items = renderListItems(listBuffer)
    result.push(`<${tag} class="${cls}">${items}</${tag}>`)
    listBuffer = []
  }

  const renderListItems = (buf) => {
    let out = ''
    let j = 0
    while (j < buf.length) {
      const item = buf[j]
      const indent = item.indent
      const children = []
      let k = j + 1
      while (k < buf.length && buf[k].indent > indent) {
        children.push(buf[k])
        k++
      }
      const body = inlineFormat(item.content)
      const childHtml = children.length > 0 ? renderListItems(children) : ''
      out += `<li>${body}${childHtml}</li>`
      j = k
    }
    return out
  }

  const flushBlockquote = () => {
    if (blockquoteLines.length === 0) return
    result.push(`<blockquote class="md-blockquote">${inlineFormat(blockquoteLines.join('<br>'))}</blockquote>`)
    blockquoteLines = []
    inBlockquote = false
  }

  const endCodeBlock = () => {
    inCodeBlock = false
    const escaped = codeLines.join('\n').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    result.push(`<pre class="md-code"><code${codeLang ? ` class="language-${codeLang}"` : ''}>${escaped}</code></pre>`)
    codeLines = []
    codeLang = ''
  }

  const endTable = () => {
    inTable = false
    if (tableHeader.length === 0) { tableRows = []; return }
    const headerHtml = tableHeader.map(h => `<th>${inlineFormat(h.trim())}</th>`).join('')
    const rowsHtml = tableRows.map(row => {
      const cells = row.map(c => `<td>${inlineFormat(c.trim())}</td>`).join('')
      return `<tr>${cells}</tr>`
    }).join('')
    result.push(`<div class="md-table-wrap"><table class="md-table"><thead><tr>${headerHtml}</tr></thead><tbody>${rowsHtml}</tbody></table></div>`)
    tableRows = []
    tableHeader = []
  }

  const isListItem = (line) => /^(\s*)([-*]|\d+\.)\s+(.*)/.test(line)

  const parseListItem = (line) => {
    const m = line.match(/^(\s*)([-*]|\d+\.)\s+(.*)/)
    if (!m) return null
    return {
      indent: m[1].length,
      prefix: m[2],
      ordered: /^\d+\.$/.test(m[2]),
      content: m[3]
    }
  }

  const isTableSep = (line) => /^\|[\s\-:|]+\|/.test(line)
  const isTableRow = (line) => line.includes('|')

  // ---- MAIN LOOP ----
  while (i < lines.length) {
    const raw = lines[i]
    const line = raw

    // Inside code block
    if (inCodeBlock) {
      if (line.startsWith('```')) {
        endCodeBlock()
      } else {
        codeLines.push(raw)
      }
      i++
      continue
    }

    // Start code block
    if (line.startsWith('```')) {
      flushParagraph()
      flushList()
      flushBlockquote()
      if (inTable) endTable()
      inCodeBlock = true
      codeLang = line.slice(3).trim()
      i++
      continue
    }

    // Inside table
    if (inTable) {
      if (line.trim() === '') {
        endTable()
        i++
        continue
      }
      if (isTableSep(line)) { i++; continue }
      if (isTableRow(line)) {
        tableRows.push(line.split('|').filter(c => c !== ''))
      } else {
        endTable()
        continue
      }
      i++
      continue
    }

    // Table start
    if (i + 1 < lines.length && isTableRow(line) && isTableSep(lines[i + 1])) {
      flushParagraph()
      flushList()
      flushBlockquote()
      inTable = true
      tableHeader = line.split('|').filter(c => c !== '')
      i += 2
      continue
    }

    // Blockquote
    if (line.startsWith('>')) {
      flushParagraph()
      flushList()
      if (inTable) endTable()
      inBlockquote = true
      blockquoteLines.push(line.replace(/^>\s?/, ''))
      i++
      continue
    }
    if (inBlockquote && line.trim() === '') {
      flushBlockquote()
      i++
      continue
    }
    if (inBlockquote && line.startsWith('>')) {
      blockquoteLines.push(line.replace(/^>\s?/, ''))
      i++
      continue
    }

    // Horizontal rule
    if (/^[-*]{3,}$/.test(line.trim())) {
      flushParagraph()
      flushList()
      flushBlockquote()
      if (inTable) endTable()
      result.push('<hr class="md-hr" />')
      i++
      continue
    }

    // Header
    const headerMatch = line.match(/^(#{1,4})\s+(.+)$/)
    if (headerMatch) {
      flushParagraph()
      flushList()
      flushBlockquote()
      if (inTable) endTable()
      const level = headerMatch[1].length
      const text = inlineFormat(headerMatch[2])
      result.push(`<h${level} class="md-h md-h${level}">${text}</h${level}>`)
      i++
      continue
    }

    // Blank line
    if (line.trim() === '') {
      flushParagraph()
      flushList()
      flushBlockquote()
      if (inTable) endTable()
      i++
      continue
    }

    // List item
    const li = parseListItem(line)
    if (li) {
      flushParagraph()
      flushBlockquote()
      if (inTable) endTable()
      // If list type or indent changes, flush previous list
      if (listBuffer.length > 0) {
        const prev = listBuffer[listBuffer.length - 1]
        if (li.ordered !== prev.ordered || li.indent < prev.indent) {
          flushList()
        }
      }
      listBuffer.push(li)
      i++
      continue
    }

    // Regular paragraph line
    if (listBuffer.length > 0) {
      flushList()
    }
    if (inBlockquote) {
      flushBlockquote()
    }
    paraBuffer.push(line)
    i++
  }

  // End-of-input flushes
  if (inCodeBlock) endCodeBlock()
  if (inTable) endTable()
  flushList()
  flushBlockquote()
  flushParagraph()

  return result.join('\n')
}

// Inline formatting: bold, italic, code
export function inlineFormat(text) {
  return text
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`(.+?)`/g, '<code class="md-inline-code">$1</code>')
}

// Strip HTML tags, decode entities, collapse whitespace — for plain-text previews
export function htmlToPlainText(html) {
  return html
    .replace(/<[^>]*>/g, ' ')           // strip tags
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&nbsp;/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
}
