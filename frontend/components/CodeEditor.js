import { useState, useRef } from 'react'
import Editor from '@monaco-editor/react'
import { motion } from 'framer-motion'

const CodeEditor = ({ 
  value, 
  onChange, 
  placeholder, 
  label, 
  darkMode,
  language = 'python'
}) => {
  const [isLoading, setIsLoading] = useState(true)
  const editorRef = useRef(null)

  const handleEditorDidMount = (editor, monaco) => {
    editorRef.current = editor
    setIsLoading(false)
    
    // Configure editor options
    editor.updateOptions({
      minimap: { enabled: false },
      fontSize: 14,
      lineNumbers: 'on',
      roundedSelection: false,
      scrollBeyondLastLine: false,
      automaticLayout: true,
      wordWrap: 'on',
      theme: darkMode ? 'vs-dark' : 'vs-light'
    })
  }

  const defaultCode = `# Example Python code
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Test the function
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
`

  return (
    <motion.div
      className="w-full"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="mb-2">
        <label className="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-2">
          {label}
        </label>
      </div>
      
      <div className="relative border border-secondary-300 dark:border-secondary-600 rounded-lg overflow-hidden bg-white dark:bg-secondary-800">
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-white dark:bg-secondary-800 z-10">
            <motion.div
              className="flex space-x-2"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
              <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            </motion.div>
          </div>
        )}
        
        <Editor
          height="400px"
          language={language}
          value={value || (placeholder ? '' : defaultCode)}
          onChange={onChange}
          onMount={handleEditorDidMount}
          theme={darkMode ? 'vs-dark' : 'vs-light'}
          options={{
            minimap: { enabled: false },
            fontSize: 14,
            lineNumbers: 'on',
            roundedSelection: false,
            scrollBeyondLastLine: false,
            automaticLayout: true,
            wordWrap: 'on',
            padding: { top: 16, bottom: 16 },
            renderLineHighlight: 'gutter',
            selectOnLineNumbers: true,
            matchBrackets: 'always',
            contextmenu: true,
            cursorBlinking: 'smooth',
            cursorSmoothCaretAnimation: true,
          }}
        />
        
        {(!value && placeholder) && (
          <div className="absolute top-4 left-4 text-secondary-400 dark:text-secondary-500 pointer-events-none">
            {placeholder}
          </div>
        )}
      </div>
      
      <div className="mt-2 flex justify-between items-center text-xs text-secondary-500 dark:text-secondary-400">
        <span>Language: {language.charAt(0).toUpperCase() + language.slice(1)}</span>
        <span>{value ? value.split('\n').length : 0} lines</span>
      </div>
    </motion.div>
  )
}

export default CodeEditor
