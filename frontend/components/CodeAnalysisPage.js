import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import CodeEditor from './CodeEditor'

const CodeAnalysisPage = ({ darkMode }) => {
  const [code, setCode] = useState('')
  const [analysis, setAnalysis] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  const analyzeCode = async () => {
    if (!code.trim()) {
      setError('Please enter some code to analyze')
      return
    }

    setIsLoading(true)
    setError(null)
    setAnalysis(null)

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code: code.trim(),
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      if (data.error) {
        throw new Error(data.error)
      }

      setAnalysis(data)
    } catch (err) {
      console.error('Analysis error:', err)
      setError(err.message || 'Failed to analyze code. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const getComplexityColor = (value, max = 10) => {
    const ratio = Math.min(value / max, 1)
    if (ratio < 0.3) return 'text-green-600 dark:text-green-400'
    if (ratio < 0.7) return 'text-yellow-600 dark:text-yellow-400'
    return 'text-red-600 dark:text-red-400'
  }

  const getAIConfidenceColor = (confidence) => {
    // Handle numeric confidence (percentage)
    if (typeof confidence === 'number') {
      if (confidence >= 70) return 'text-red-600 dark:text-red-400'
      if (confidence >= 40) return 'text-yellow-600 dark:text-yellow-400'
      return 'text-green-600 dark:text-green-400'
    }
    
    // Handle string confidence (legacy)
    switch (confidence) {
      case 'high': return 'text-red-600 dark:text-red-400'
      case 'medium': return 'text-yellow-600 dark:text-yellow-400'
      default: return 'text-green-600 dark:text-green-400'
    }
  }

  const loadSample = () => {
    const sampleCode = `def fibonacci_sequence(n):
    """
    Generate Fibonacci sequence up to n terms.
    
    Args:
        n (int): Number of terms to generate
        
    Returns:
        list: Fibonacci sequence
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n):
        next_num = sequence[i-1] + sequence[i-2]
        sequence.append(next_num)
    
    return sequence

def main():
    # Get user input
    try:
        num_terms = int(input("Enter number of terms: "))
        result = fibonacci_sequence(num_terms)
        print(f"Fibonacci sequence: {result}")
    except ValueError:
        print("Please enter a valid number")

if __name__ == "__main__":
    main()`
    
    setCode(sampleCode)
    setAnalysis(null)
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-secondary-50 to-primary-50 dark:from-secondary-900 dark:to-secondary-800 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          className="text-center mb-8"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="text-4xl font-bold gradient-text mb-4">
            🔬 Code Analysis Lab
          </h1>
          <p className="text-xl text-secondary-600 dark:text-secondary-400">
            Advanced Code Structure Analysis & AI Detection
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Code Input Section */}
          <motion.div
            className="space-y-6"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <div className="card p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-semibold text-secondary-900 dark:text-secondary-100">
                  Code Input
                </h2>
                <button
                  onClick={loadSample}
                  className="btn-secondary text-sm"
                >
                  Load Sample
                </button>
              </div>
              
              <CodeEditor
                value={code}
                onChange={setCode}
                label=""
                placeholder="Paste your code here for analysis..."
                darkMode={darkMode}
                language="python"
              />
              
              <div className="mt-4 flex justify-center">
                <motion.button
                  onClick={analyzeCode}
                  disabled={isLoading || !code.trim()}
                  className={`btn-primary px-8 py-3 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2 ${
                    isLoading ? 'cursor-wait' : ''
                  }`}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  {isLoading ? (
                    <>
                      <motion.svg
                        className="w-5 h-5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                        animate={{ rotate: 360 }}
                        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </motion.svg>
                      <span>Analyzing...</span>
                    </>
                  ) : (
                    <>
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                      <span>Analyze Code</span>
                    </>
                  )}
                </motion.button>
              </div>
            </div>
          </motion.div>

          {/* Analysis Results Section */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
          >
            <AnimatePresence mode="wait">
              {error && (
                <motion.div
                  className="mb-6 p-4 bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-600 text-red-700 dark:text-red-300 rounded-lg"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                >
                  <div className="flex items-center">
                    <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    {error}
                  </div>
                </motion.div>
              )}

              {isLoading ? (
                <motion.div
                  className="card p-8"
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  key="loading"
                >
                  <div className="text-center">
                    <motion.div
                      className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary-100 dark:bg-primary-900 mb-4"
                      animate={{ rotate: 360 }}
                      transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                    >
                      <svg className="w-8 h-8 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                    </motion.div>
                    <h3 className="text-lg font-semibold text-secondary-900 dark:text-secondary-100 mb-2">
                      Analyzing Code Structure
                    </h3>
                    <p className="text-secondary-600 dark:text-secondary-400">
                      Performing deep analysis with AI detection...
                    </p>
                  </div>
                </motion.div>
              ) : analysis ? (
                <motion.div
                  className="space-y-6"
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  key="results"
                >
                  {/* AI Detection Results */}
                  <div className="card p-6">
                    <h3 className="text-xl font-bold text-secondary-900 dark:text-secondary-100 mb-4 flex items-center">
                      <span className="mr-2">🤖</span>
                      AI Detection Results
                    </h3>
                    
                    {analysis.ai_detection && !analysis.ai_detection.error ? (
                      <div className="space-y-4">
                        <div className="flex items-center justify-between p-4 rounded-lg bg-secondary-50 dark:bg-secondary-700">
                          <div>
                            <p className="font-semibold text-secondary-900 dark:text-secondary-100">
                              AI Probability: {Math.round(analysis.ai_detection.confidence)}%
                            </p>
                            <p className={`text-sm ${getAIConfidenceColor(analysis.ai_detection.confidence)}`}>
                              Confidence: {typeof analysis.ai_detection.confidence === 'number' 
                                ? `${analysis.ai_detection.confidence.toFixed(1)}%`
                                : analysis.ai_detection.confidence.toUpperCase()}
                            </p>
                          </div>
                          <div className="text-2xl font-bold">
                            {analysis.ai_detection.confidence >= 70 ? '🚨' : 
                             analysis.ai_detection.confidence >= 40 ? '⚠️' : '✅'}
                          </div>
                        </div>
                        
                        <div className="p-4 rounded-lg bg-blue-50 dark:bg-blue-900">
                          <p className="font-medium text-blue-900 dark:text-blue-100 mb-2">
                            Verdict: {analysis.ai_detection.verdict}
                          </p>
                          
                          {analysis.ai_detection.pattern_analysis?.indicators?.length > 0 && (
                            <div>
                              <p className="text-sm text-blue-700 dark:text-blue-300 mb-2">
                                Detected patterns:
                              </p>
                              <ul className="text-xs text-blue-600 dark:text-blue-400 space-y-1">
                                {analysis.ai_detection.pattern_analysis.indicators.map((indicator, index) => (
                                  <li key={index} className="flex items-center">
                                    <span className="w-1 h-1 bg-blue-500 rounded-full mr-2"></span>
                                    {indicator}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      </div>
                    ) : (
                      <p className="text-red-600 dark:text-red-400">
                        AI detection failed: {analysis.ai_detection?.error}
                      </p>
                    )}
                  </div>

                  {/* Structure Analysis */}
                  {analysis.code_analysis && !analysis.code_analysis.error && (
                    <div className="card p-6">
                      <h3 className="text-xl font-bold text-secondary-900 dark:text-secondary-100 mb-4 flex items-center">
                        <span className="mr-2">📊</span>
                        Code Structure Analysis
                      </h3>
                      
                      <div className="grid md:grid-cols-2 gap-4">
                        <div className="space-y-3">
                          <div className="flex justify-between">
                            <span className="text-secondary-600 dark:text-secondary-400">Lines of Code:</span>
                            <span className="font-semibold">{analysis.code_analysis.lines_of_code}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-secondary-600 dark:text-secondary-400">Functions:</span>
                            <span className="font-semibold">{analysis.code_analysis.functions?.length || 0}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-secondary-600 dark:text-secondary-400">Classes:</span>
                            <span className="font-semibold">{analysis.code_analysis.classes?.length || 0}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-secondary-600 dark:text-secondary-400">Imports:</span>
                            <span className="font-semibold">{analysis.code_analysis.imports?.length || 0}</span>
                          </div>
                        </div>
                        
                        {analysis.code_analysis.complexity_metrics && (
                          <div className="space-y-3">
                            <h4 className="font-semibold text-secondary-900 dark:text-secondary-100">
                              Complexity Metrics
                            </h4>
                            <div className="flex justify-between">
                              <span className="text-secondary-600 dark:text-secondary-400">Cyclomatic:</span>
                              <span className={`font-semibold ${getComplexityColor(analysis.code_analysis.complexity_metrics.cyclomatic_complexity)}`}>
                                {analysis.code_analysis.complexity_metrics.cyclomatic_complexity}
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-secondary-600 dark:text-secondary-400">Nesting Depth:</span>
                              <span className={`font-semibold ${getComplexityColor(analysis.code_analysis.complexity_metrics.nesting_depth, 5)}`}>
                                {analysis.code_analysis.complexity_metrics.nesting_depth}
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-secondary-600 dark:text-secondary-400">Maintainability:</span>
                              <span className={`font-semibold ${analysis.code_analysis.complexity_metrics.maintainability_index >= 60 ? 'text-green-600 dark:text-green-400' : 'text-yellow-600 dark:text-yellow-400'}`}>
                                {Math.round(analysis.code_analysis.complexity_metrics.maintainability_index)}
                              </span>
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Functions and Classes Details */}
                  {analysis.code_analysis && (analysis.code_analysis.functions?.length > 0 || analysis.code_analysis.classes?.length > 0) && (
                    <div className="card p-6">
                      <h3 className="text-xl font-bold text-secondary-900 dark:text-secondary-100 mb-4 flex items-center">
                        <span className="mr-2">🔧</span>
                        Code Components
                      </h3>
                      
                      {analysis.code_analysis.functions?.length > 0 && (
                        <div className="mb-4">
                          <h4 className="font-semibold text-secondary-900 dark:text-secondary-100 mb-2">
                            Functions ({analysis.code_analysis.functions.length})
                          </h4>
                          <div className="space-y-2">
                            {analysis.code_analysis.functions.map((func, index) => (
                              <div key={index} className="flex justify-between items-center p-2 rounded bg-secondary-50 dark:bg-secondary-700">
                                <span className="font-mono text-sm">{func.name}()</span>
                                <div className="flex space-x-2 text-xs text-secondary-600 dark:text-secondary-400">
                                  <span>{func.args} args</span>
                                  <span>Line {func.line}</span>
                                  {func.docstring && <span className="text-green-600 dark:text-green-400">📝</span>}
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                      
                      {analysis.code_analysis.classes?.length > 0 && (
                        <div>
                          <h4 className="font-semibold text-secondary-900 dark:text-secondary-100 mb-2">
                            Classes ({analysis.code_analysis.classes.length})
                          </h4>
                          <div className="space-y-2">
                            {analysis.code_analysis.classes.map((cls, index) => (
                              <div key={index} className="flex justify-between items-center p-2 rounded bg-secondary-50 dark:bg-secondary-700">
                                <span className="font-mono text-sm">{cls.name}</span>
                                <div className="flex space-x-2 text-xs text-secondary-600 dark:text-secondary-400">
                                  <span>{cls.methods} methods</span>
                                  <span>Line {cls.line}</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Code Insights */}
                  {analysis.insights && analysis.insights.length > 0 && (
                    <div className="card p-6">
                      <h3 className="text-xl font-bold text-secondary-900 dark:text-secondary-100 mb-4 flex items-center">
                        <span className="mr-2">💡</span>
                        Code Insights & Recommendations
                      </h3>
                      
                      <div className="space-y-3">
                        {analysis.insights.map((insight, index) => (
                          <div key={index} className="flex items-start space-x-3 p-3 rounded-lg bg-blue-50 dark:bg-blue-900">
                            <div className="flex-shrink-0 mt-0.5">
                              <span className="text-lg">
                                {insight.includes('🟢') ? '🟢' :
                                 insight.includes('🟡') ? '🟡' :
                                 insight.includes('🟠') ? '🟠' :
                                 insight.includes('🔴') ? '🔴' :
                                 insight.includes('📄') ? '📄' :
                                 insight.includes('🔧') ? '🔧' :
                                 insight.includes('🏗️') ? '🏗️' :
                                 insight.includes('✨') ? '✨' :
                                 insight.includes('👍') ? '👍' :
                                 insight.includes('⚠️') ? '⚠️' :
                                 insight.includes('📏') ? '📏' :
                                 insight.includes('✅') ? '✅' :
                                 insight.includes('📝') ? '📝' :
                                 insight.includes('🤖') ? '🤖' :
                                 insight.includes('👨‍💻') ? '👨‍💻' : '💡'}
                              </span>
                            </div>
                            <p className="text-sm text-blue-900 dark:text-blue-100 leading-relaxed">
                              {insight.replace(/[🟢🟡🟠🔴📄🔧🏗️✨👍⚠️📏✅📝🤖👨‍💻💡]\s*/, '')}
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </motion.div>
              ) : null}
            </AnimatePresence>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default CodeAnalysisPage
